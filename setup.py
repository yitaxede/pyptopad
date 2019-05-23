from setuptools import setup, find_packages

setup(
    name="pyptopad",
    version="1.0",
    description="Pyptopad: python crypto pad",
    long_description=open("README.md", "rb").read().decode("utf-8"),
    long_description_content_type='text/markdown',
    author="Pyptopad team",
    url="https://github.com/yitaxede/pyptopad",
    license="GPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3" +
        " or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Security :: Cryptography",
    ],
    packages=find_packages(),
    py_modules=["pyptopad"],
    data_files=(
        ('', (
            "README.md",
            "LICENSE",
        )),
    ),
    install_requires=[
        "PyNaCl",
        "cryptography",
        "pygost",
    ],
    setup_require=["mo_installer"],
    locale_src=".",
)
