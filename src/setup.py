from setuptools import setup, find_packages

setup(
    name='reader',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
        'pyspedas',
        'spacepy',
        'wmi',
    ],
    entry_points={
        'console_scripts': [
            # If you want to create command-line tools
        ],
    },
)
