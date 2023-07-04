from setuptools import setup, find_packages

setup(
    name='DebugGPT',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dotenv',
        'openai',
        'backoff',
        'rich',
        'inquirer',
        'pathspec',
        'pyfiglet'
    ],
    entry_points={
        'console_scripts': [
            'dgpt=dgpt.cli:main',
        ],
    },
)

