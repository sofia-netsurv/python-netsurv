import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netsurv",
    version="0.1.0",
    author="Eliot Woodrich & Ebraheem AlAtari",
    author_email="eliot@woodrich.com",
    description="Configure IP cameras.",
    long_description="Python library for configuring a wide range of IP cameras which use the NETsurveillance ActiveX plugin (aka DVRIP, Sofia)",
    long_description_content_type="text/markdown",
    url="https://github.com/sofia-client/python-netsurv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
