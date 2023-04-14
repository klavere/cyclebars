from setuptools import setup

setup(
    name='cyclebars',
    version='1.2.0.3',
    description='A package containing four plotting functions for (potentially) cyclic time series with anomalies.',
    url='https://github.com/klavere/cyclebars',
    author='Verena Klasen',
    author_email='verena.klasen@uni-a.de',
    license='MIT',
    packages=['cyclebars'],
    install_requires=[
        'numpy>=1.21.2',
        'pandas>=1.3.3',
        'matplotlib>=3.4.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research/Visualization',
        'Programming Language :: Python :: 3.9',
    ],
)