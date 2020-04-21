===================
Messaging Consenter
===================
.. image:: https://travis-ci.com/praekeltfoundation/messaging-consenter.svg?branch=develop
    :target: https://travis-ci.com/praekeltfoundation/messaging-consenter
    :alt: Build Passing/Failing on TravisCI.com

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code Style: Black


.. image:: https://codecov.io/gh/praekeltfoundation/messaging-consenter/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/praekeltfoundation/messaging-consenter
  :alt: Code Coverage


.. image:: https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg
    :target: https://hub.docker.com/r/praekeltfoundation/messaging-consenter/tags/
    :alt: Docker Automated build

Messaging-Consenter is a lightweight Django application for serving a consent form to users. Consent is then saved on the RapidPro contact matching the UUID in the URL.
This might get rolled into https://github.com/praekeltfoundation/rp-sidekick at some point.

-----
Usage
-----
Run docker container with the following environment variables set
 * CONSENT_REDIRECT_URL (Optional) - URL to redirect a user to after they have provided consent (default: /consent/success/)
 * RAPIDPRO_URL - URL for the RapidPro instance
 * RAPIDPRO_TOKEN - authentication token for the RapidPro token
 * RAPIDPRO_FLOW_ID (Optional) - the id of the RapidPro flow to start a user on once they have provided consent

The RapidPro Organisation must have two custom fields for Contacts:
 * consent_date (Date and Time field)
 * consent ("true" or "false" Text field)

Build a link for the user using the domain for the application, the word "consent" and their RapidPro UUID. When they provide consent their RapidPro Contact will be updated and they will be redirected to CONSENT_REDIRECT_URL.

------------------
Local installation
------------------
To set up and run ``messaging-consenter`` locally, do the following::

    $ git clone git@github.com:praekeltfoundation/messaging-consenter.git
    $ cd messaging-consenter
    $ virtualenv ve
    $ source ve/bin/activate
    $ pip install -e .
    $ pip install -r requirements-dev.txt

-----
Tools
-----

- `black`_ - this repository uses an opinionated python code formatter. See ``pyproject.toml`` for config.

------------
Contributing
------------

See our `ways of working`_ for a guide on how to contribute to ``messaging-consenter``.

.. _black: https://github.com/ambv/black
.. _ways of working: ./docs/ways-of-working.md

