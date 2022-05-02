"""
# Upload Package: https://pypi.org/project/web3tools/
python3 setup.py sdist bdist_wheel
twine upload dist/web3tools-0.0.4*
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="web3tools",
    version="0.0.8",
    author="José Pereira",
    author_email="zepcp@hotmail.com",
    description="Web3Py Extender Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zepcp/web3tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
