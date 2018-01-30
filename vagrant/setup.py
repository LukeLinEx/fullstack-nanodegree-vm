from setuptools import setup

setup(
    name='online',
    packages=["flask_exercise"],
    include_package_data=True,
    install_requires=[
        'flask',
        'pymongo',
        'boto3'
    ],
)