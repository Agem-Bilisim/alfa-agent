from io import open

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install
from subprocess import check_output, CalledProcessError
import sys
import os

with open('alfa_agent/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

try:
    is_admin = os.getuid() == 0
except AttributeError:
    import ctypes
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

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
    'win32-pip': ['pywin32', 'comtypes'],
    'debian': ['lshw', 'python3-gi', 'gir1.2-webkit-3.0']
}


def is_gtk_based():
    try:
        output = check_output("apt-cache policy libgtk-3-0 | grep Installed".split(), universal_newlines=True)
        return "Installed" in output
    except CalledProcessError as e:
        pass
    return False


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        if is_admin:
            if sys.platform == "win32":
                try:
                    check_output("pip.exe install --no-input {}".format(" ".join(PLATFORM_REQUIRES['win32-pip']))
                                 .split(), universal_newlines=True)
                except CalledProcessError as e:
                    print("[ERROR] Error occurred during installation of PyWebView/Win32 dependencies: {}"
                          .format(str(e)))
            # Should also check for debian here...
            elif is_gtk_based():
                try:
                    check_output("apt-get install -y {}".format(" ".join(PLATFORM_REQUIRES['debian'])).split(),
                                 universal_newlines=True)
                except CalledProcessError as e:
                    print("[ERROR] Error occurred during installation of PyWebView/GTK3.0 dependencies: {}"
                          .format(str(e)))
        else:
            print("[WARN] Install command invoked without elevated privileges! Cannot install 3rd party dependencies.\n"
                  + "If you are installing (not building) the agent, please install following dependencies manually: {}"
                  .format(", ".join(PLATFORM_REQUIRES["win32-pip" if sys.platform == "win32" else "debian"])))
        install.run(self)


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
    url='https://github.com/Agem-Bilisim/alfa-agent',
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

    cmdclass={
        'install': PostInstallCommand,
    },
)
