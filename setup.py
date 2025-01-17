from setuptools import setup, find_packages

setup(
    name="im2vid",
    version="0.1.6",
    packages=find_packages(),
    install_requires=["matplotlib", "moviepy", "tqdm", "einops"],
    author="Julian Tanke",
    author_email="Julian.Tanke@sony.com",
    description="A utility for converting images to videos",
    url="https://github.com/jutanke-sony/im2vid",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
