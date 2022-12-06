from setuptools import setup

setup(
    name='cyclebars',
    version='0.1',
    description='A package containing four plotting functions for (potentially) cyclic time series with anomalies.',
    url='https://github.com/klavere/cyclebars',
    author='Verena Klasen',
    author_email='verena.klasen@uni-a.de',
    license='to be announced',
    packages=['cyclebars'],
    install_requires=[
        'numpy>=1.21.2',
        'pandas>=1.3.3',
        'matplotlib>=3.4.2',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research/Visualization',
        'Programming Language :: Python :: 3.9',
    ],
)