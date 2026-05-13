from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name='aviation',
    version='1.0.0',
    description='Comprehensive Aviation Management System for ERPNext',
    author='Aviation Team',
    author_email='admin@aviation.org',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
