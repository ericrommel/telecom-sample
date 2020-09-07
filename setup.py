from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="app",
    version="1.0.0",
    author="Eric Dantas",
    author_email="ericrommel@gmail.com",
    description="Telecom Sample project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericrommel/telecom-sample",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=[
        "flask",
    ],
)
