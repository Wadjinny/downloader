import asyncio
from tqdm import tqdm
from pathlib import Path
import httpx


# %%
async def maybe_coro(coro, *args, **kwargs):
    loop = asyncio.get_running_loop()

    if asyncio.iscoroutinefunction(coro):
        return await coro(*args, **kwargs)
    else:
        return await loop.run_in_executor(None, coro, *args, **kwargs)


class MultiConnectionDownloader:
    MINIMUM_PART_SIZE = 1024**2

    def __init__(
        self,
        session,
        *args,
        loop=None,
        progress_bar=None,
        **kwargs,
    ):
        self.session = session

        self.args = args
        self.kwargs = kwargs

        self.loop = loop or asyncio.new_event_loop()
        self.io_lock = asyncio.Lock()

        self.progress_bar = progress_bar

    async def download_part(
        self,
        io,
        start: int,
        end: int,
        progress_bar=None,
        future=None,
        pause_event=None,
    ):
        headers = self.kwargs.pop("headers", {})
        content_length = end
        position = start or 0

        is_incomplete = lambda: content_length is None or position < content_length
        is_downloading = lambda: (pause_event is None or not pause_event.is_set())

        while is_downloading() and is_incomplete():
            if content_length is None:
                if start is not None:
                    headers["Range"] = f"bytes={position}-"
            else:
                headers["Range"] = f"bytes={position}-{content_length}"

            try:
                async with self.session.stream(
                    *self.args, **self.kwargs, headers=headers
                ) as response:
                    content_length = (
                        int(response.headers.get("Content-Length", 0)) or None
                    )

                    if progress_bar is not None:
                        if content_length > 0:
                            progress_bar.total = content_length

                    async for chunk in response.aiter_bytes(8192):
                        chunk_size = len(chunk)

                        if self.progress_bar is not None:
                            self.progress_bar.update(chunk_size)

                        if progress_bar is not None:
                            progress_bar.update(chunk_size)

                        await self.write_to_file(
                            self.io_lock,
                            io,
                            position,
                            chunk,
                        )
                        position += chunk_size

                        if not is_downloading():
                            break

                    if content_length is None:
                        content_length = position

            except httpx.HTTPError as e:
                locks = ()

                if progress_bar is not None:
                    locks += (progress_bar.get_lock(),)
                if self.progress_bar is not None:
                    locks += (self.progress_bar.get_lock(),)

                # TODO: Warn user about the error.

        if future is not None:
            future.set_result((start, position))

        return (start, position)

    @staticmethod
    async def write_to_file(
        lock: asyncio.Lock,
        io,
        position: int,
        data: bytes,
    ):
        async with lock:
            await maybe_coro(io.seek, position)
            await maybe_coro(io.write, data)
            await maybe_coro(io.flush)

    async def allocate_downloads(
        self,
        io,
        content_length: int = None,
        connections: int = 8,
        allocate_content_on_disk=False,
        pause_event=None,
    ):
        def iter_allocations():
            if content_length is None or content_length < self.MINIMUM_PART_SIZE:
                yield None, None
            else:
                chunk_size = content_length // connections
                for i in range(connections - 1):
                    yield i * chunk_size, (i + 1) * chunk_size - 1

                yield (connections - 1) * chunk_size, None

        if allocate_content_on_disk:
            async with self.io_lock:
                await maybe_coro(io.truncate, content_length)

        return await asyncio.gather(
            *(
                self.download_part(io, start, end, pause_event=pause_event)
                for start, end in iter_allocations()
            )
        )

    @staticmethod
    async def is_resumable(
        session,
        method,
        *args,
        **kwargs,
    ):
        headers = kwargs.pop("headers", {})

        headers["Range"] = "bytes=0-0"

        async with session.stream(method, *args, **kwargs) as response:
            return {
                "status_code": response.status_code,
                "headers": response.headers,
                "url": response.url,
            }


# %%


def dowload_from_url(url, headers=None, output_dir: Path = None, filename=None):
    if headers is None:
        headers = {}

    """
    Connection rating
    >1 - Normal download
    >4 - Quite good
    >8 - Good
    >16 - Good but probably will be throttled
    >32 - Will be throttled
    """

    CONNECTIONS = 32

    async def __main__(filename=filename, output_dir=output_dir):
        session = httpx.AsyncClient(
            timeout=30.0,
            # follow_redirects=True,
            headers=headers,
            verify=False,
        )

        progress_bar = tqdm(
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        head_response = await session.head(url)

        qualified_filename = head_response.url.path.split("/")[-1]
        if filename is None:
            filename = qualified_filename
        if output_dir is None:
            output_dir = Path.cwd()
        content_length = int(head_response.headers.get("Content-Length", 0))

        progress_bar.total = content_length
        progress_bar.set_description(f"<= {qualified_filename!r}")

        with open(output_dir / filename, "wb") as io:
            downloader = MultiConnectionDownloader(
                session,
                "GET",
                url,
                progress_bar=progress_bar,
            )

            downloaded_positions = await downloader.allocate_downloads(
                io, content_length, connections=CONNECTIONS
            )

        await session.aclose()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(__main__())


if __name__ == "__main__":
    URL = "https://old-releases.ubuntu.com/releases/22.04.1/ubuntu-22.04.1-desktop-amd64.iso"
    dowload_from_url(URL)
