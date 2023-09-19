from setuptools import setup, find_packages
setup(
    name='ubbc',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points="""
    [
    console_scripts]
    command = ubbc.main:main
    """,
)
