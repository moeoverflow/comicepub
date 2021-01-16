import setuptools
from comicepub.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="comicepub",
    version=__version__,
    author="ShinCurry",
    author_email="shincurryyang@gmail.com",
    description="Japanese comic EPUB3 generate tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moeoverflow/comicepub",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Jinja2>=2.10.1'
    ],
    entry_points={
        'console_scripts': [
            'comicepub = comicepub.cli:main'
        ]
    }
)