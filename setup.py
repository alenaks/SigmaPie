import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="SigmaPie",
    version="0.5",
    author="Alëna Aksënova",
    author_email="loisetoil@gmail.com",
    description="A package for subregular and subsequential grammar induction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alenaks/SigmaPie",
    package_dir={"": "src"},
    #packages=setuptools.find_packages(where='src'),
    packages=["sigmapie"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="language grammar subregular subsequential transducer induction",
)