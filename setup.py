from setuptools import setup

setup(
    name='autopipinstall',
    version='0.1.0',
    description='A Python CLI tool to auto-install missing modules on the fly.',
    author='Your Name',
    py_modules=['autopipinstall.cli'],
    entry_points={
        'console_scripts': [
            'autopipinstall=autopipinstall.cli:main',
        ],
    },
)
