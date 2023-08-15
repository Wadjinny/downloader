from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = "Download anime from witanime"
  
setup(
        name ='witanime',
        version ='1.0.0',
        author ='ilyas wadjinny',
        description = 'Download anime from witanime',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'witanime = witanime.main:main'
            ]
        },
        install_requires = requirements,
        zip_safe = False
)