import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Map generator",
    version="0.0.1",
    author="Oleh Palka",
    author_email="oleh.palka@ucu.edu.ua",
    descripthion="program, which generates map whith 10 films shoted near you.",
    long_description=long_description,
    long_description_content_type="text",
    url=" ",
    packages=setuptools.find_packages(),
    classfiers=[
        "Programming language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">= 3.8"
)
