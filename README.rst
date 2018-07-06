alfa-agent
==========

-----

.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

alfa-agent is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 2.7/3.5+ and PyPy.

.. code-block:: bash

    $ pip install alfa-agent


Development Environment
------------

Make sure you have at least Python 3.5.x installed, cd into project directory then type the following commands:

.. code-block:: bash

    $ pip3 install --upgrade virtualenv hatch
    $ hatch env alfa && hatch shell alfa
    $ pip3 install -r requirements.txt


That's it.

Now you can start development, or run the project by typing:

.. code-block:: bash

    # if you have NOT already activated alfa virtual environment.
    $ hatch shell alfa
    # we should type full path here in order to elevate virtual environment successfully!
    $ python3 /home/USER/git/alfa-agent/alfa_agent/cli.py _start


Versioning
------------
We use hatch for versioning as well, here are a few examples:

.. code-block:: bash

    $ hatch grow build
    Updated /home/emre/git/alfa-agent/alfa_agent/__init__.py
    0.0.1 -> 0.0.1+build.1
    $ hatch grow fix
    Updated /home/emre/git/alfa-agent/alfa_agent/__init__.py
    0.0.1+build.1 -> 0.0.2
    $ hatch grow minor
    Updated /home/emre/git/alfa-agent/alfa_agent/__init__.py
    0.0.2 -> 0.1.0
    $ hatch grow major
    Updated /home/emre/git/alfa-agent/alfa_agent/__init__.py
    0.1.0 -> 1.0.0


Requirement Management
------------
Requirements are managed either by PIP or during setup thanks to setup.py. So there are basicly two places we need to look:

* setup.py REQUIRES array and
* requirements.txt


License
-------

alfa-agent is distributed under the terms of the
`MIT License <https://choosealicense.com/licenses/mit>`_.