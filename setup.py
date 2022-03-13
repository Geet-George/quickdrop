import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quickdrop",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Geet George",
    author_email="geet.george@mpimet.mpg.de",
    description="Quick work with dropsondes in the field",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Geet-George/quickdrop",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.18.5",
        "xarray>=0.20.0",
        "netCDF4>=1.5.0",
        "MetPy>=0.12.2",
        "cartopy>=0.18.0"
    ],
)