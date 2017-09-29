"""
Yarnplot - Gather YARN application statistics as timeline
"""
from setuptools import find_packages, setup

setup(
    name='yarnplot',
    version='0.1.0',
    url='https://github.com/test/yarnplot',
    license='MIT',
    author='Tim Taschke',
    description='YarnPlot - Tool to collect timeline-based YARN application statistics',
    long_description=__doc__,
    packages=["yarnplot"],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['matplotlib','pandas','requests','seaborn'],
    entry_points={
        'console_scripts': [
            'yarnplot = yarnplot.cli:main',
        ],
    }
)
