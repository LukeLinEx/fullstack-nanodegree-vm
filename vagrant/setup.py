from setuptools import setup

setup(
    name='flask_project',
    packages=["flask_project"],
    include_package_data=True,
    install_requires=[
        'flask',
        'pymongo',
        'boto3'
    ],
)