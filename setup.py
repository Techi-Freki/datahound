from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='datahound',
    version='2.0.0',
    packages=find_packages(),
    url='https://python.dbcombs.com/simple/datahound',
    license='WTFPL',
    author='D. Bryan Combs',
    author_email='dbcombs@gmail.com',
    description='sqlite3 data access layer',
    long_description_content_type='text/markdown',
    long_description=readme(),
    install_requires=['mariadb'],
    classifiers=[
        'Programming Language :: Python :: 3.0',
        'License :: WTFPL License',
        'Operating System :: OS Independent'
    ],
	include_package_data=True
)