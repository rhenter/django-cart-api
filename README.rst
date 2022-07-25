========
Cart API
========

STILL IN DEVELOPMENT

Requirements
============

This project requires:
    * Python 3.9.1 or earlier
    * PostgreSQL 9.3+
    * Git
    * virtualenvwrapper, pyenv virtualenv or virtualenv for local development


Installation
============

1. Install system requirements:

.. code-block:: shell

    $ sudo apt-get install postgresql-client postgresql postgresql-server-dev

2. Create an user and a database in local PostgreSQL for local development:

.. code-block:: shell

    $ sudo -u postgres createuser --createdb cart_api -sP
    $ sudo -u postgres createdb cart_api_1.0 -O cart_api

3. Create a Python environment and clone project repository:

Pyenv Configuration:
~~~~~~~~~~~~~~~~~~~~

- Install

.. code-block:: shell

    $ curl https://pyenv.run | bash
    $ export PATH="$HOME/.pyenv/bin:$PATH"
    $ eval "$(pyenv init -)"
    $ eval "$(pyenv virtualenv-init -)"

- Restart the terminal or exec:

.. code-block:: shell

    $ exec "$SHELL"

- Install the python 3.8 version and set as default

.. code-block:: shell

    $ pyenv install 3.9.0 -v
    $ pyenv global 3.9.0

Add you SSH Key to GitLab

.. code-block:: shell

    $ git clone git@gitlab.gerdaugln.tech:gln-industrial/hydrostats-api.git hydrostats-api
    $ cd hydrostats-api
    $ mkvirtualenv -p $(which python) cart_api
    $ workon cart_api

Or using pyenv virtualenv

    $ git clone git@gitlab.gerdaugln.tech:gln-industrial/hydrostats-api.git
    $ cd hydrostats-api
    $ pyenv virtualenv cart_api
    $ pyenv activate cart_api

4. Create your local settings file (use local.env as a template):

.. code-block:: shell

    $ cp local.env .env

    Edit .env file to use your settings


5. Install the project requirements:

.. code-block:: shell

    $ pip install -r requirements/local.txt


Database migrations
===================

All migrations SHOULD have a description, so, always use the following command to apply all database migrations:

.. code-block:: shell

    $ python manage.py migrate


Tests
=====

We use ``pytest`` with some nice plugins instead of the default test runner provided by Django.

.. code-block:: shell

    $ pytest -vv -s


Database Creation
=================

The default ``pytest`` settings (``pytest.ini``) enables the option of database reutilization (``--reuse-db``) to make
tests run faster.

.. hint:: Force database creation

    Sometimes it's required that you recreate the local database. In this cases use the option ``--create-db`` on
    command line.

For further info take look in `thanks rst database`.
