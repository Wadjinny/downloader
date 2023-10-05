from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

long_description = "Download anime from witanime and anime-sanka"

setup(
    name="witanime",
    version="1.0.0",
    author="ilyas wadjinny",
    description="Download anime from witanime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "witanime = witanime.witanime_main:main",
            "animesanka = witanime.animesanka_main:main",
            "zimabadk = witanime.zimabadk_main:main",
        ]
    },
    install_requires=requirements,
    zip_safe=False,
)
