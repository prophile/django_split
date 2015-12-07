from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='django_split',
    version='0.1.0',
    author='Thread Tech',
    author_email='tech@thread.com',
    description='Split testing for Django',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'Django >=1.8',
        'numpy >=1.10, <2',
        'scipy >=0.16, <1',
        'inflection >=0.3, <1',
    ],
    setup_requires=[
        'nose >=1.3, <2',
    ],
)
