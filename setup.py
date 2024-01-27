from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='datahound',
    version='3.0.1',
    packages=find_packages(),
    url='https://python.dbcombs.com/simple/datahound',
    license='MIT',
    author='Techi-Freki',
    author_email='techifreki@proton.me',
    description='sqlite3 data access layer',
    long_description_content_type='text/markdown',
    long_description=readme(),
    install_requires=[],
    entry_points={
        'datahound.connectors': ['datahound_sqlite=datahound.connectors:SqLite3Connector']
    },
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: MIT License',
        'Operating System :: OS Independent'
    ],
    include_package_data=True
)
