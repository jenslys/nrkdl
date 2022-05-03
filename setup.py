import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nrkdl",
    version="1.0.5",
    author="jenlys",
    description="Download movies/tv-shows from nrk.no",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    project_urls={
        "Source": "https://github.com/jenslys/nrkdl/",
        "Tracker": "https://github.com/jenslys/nrkdl/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["nrkdl"],
    install_requires=["yt-dlp"],
    entry_points={
        "console_scripts": [
            "nrkdl=nrkdl.nrkdl:main",
        ],
    },
)
