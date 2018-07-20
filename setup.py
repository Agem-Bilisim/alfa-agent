from io import open

from setuptools import find_packages, setup

with open('alfa_agent/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = [
    'pywin32 >= 1.0;platform_system=="Windows"',
    'comtypes >= 1.1;platform_system=="Windows"',
    'py-cpuinfo >= 4.0.0',
    'pywebview >= 2.0.3',
    'psutil >= 5.4.6',
    'requests >= 2.19.1',
    'elevate >= 0.1.3',
    'PyYAML >= 3.13',
]

PLATFORM_REQUIRES = {
    'win32': '',
    'debian': ['lshw', 'python-gi', 'gir1.2-webkit-3.0']
}

# See https://blog.ionelmc.ro/presentations/packaging for more info about packaging.
setup(
    name='alfa-agent',
    version=version,
    description='',
    long_description=readme,
    author='Emre Akkaya',
    author_email='emre.akkaya@agem.com.tr',
    maintainer='Emre Akkaya',
    maintainer_email='emre.akkaya@agem.com.tr',
    url='https://github.com/_/alfa-agent',
    license='MIT',

    keywords=[
        'Migration management and information system',
        'Migration agent',
        'Pardus',
        'Migrating from Windows to Linux',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'alfa-agent = alfa_agent.cli:agent',
        ],
    },
)
