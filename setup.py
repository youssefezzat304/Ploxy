from setuptools import setup, find_packages

setup(
    name="ploxy",
    version="0.1.0",
    author="Youssef Abdelrahim",
    package_dir={"": "Python"},
    packages=find_packages(where="Python"),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ploxy=Ploxy.__main__:main',
        ],
    },
)
