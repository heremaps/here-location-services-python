Contributing to HERE Location Services for Python
=================================================

Thank you for taking the time to contribute.

The following is a set of guidelines for contributing to this package.
These are mostly guidelines, not rules. Use your best judgement and feel free to propose
changes to this document in a pull request.

Coding Guidelines
-----------------
- Lint your code contributions as per `pep8 guidelines`_.

  To help you out, we have included a `Makefile` in the root directory which supports the commands below:
  Autoformat code using black::

    make black

  Check for linting errors::

    make lint

- Sort the imports in each python file as per `pep8 guidelines imports`_.
  Please execute the isort utility to have the imports sorted auto-magically.

.. _pep8 guidelines: https://www.python.org/dev/peps/pep-0008/
.. _pep8 guidelines imports: https://www.python.org/dev/peps/pep-0008/#imports

Notebooks
---------

Example Notebooks are provided in `Notebooks <https://github.com/heremaps/here-location-services-python/-/tree/master/docs/notebooks>`_.

Signing each Commit
-------------------

When you file a pull request, we ask that you sign off the
`Developer Certificate of Origin <https://developercertificate.org/>`_ (DCO) in each commit.
Any Pull Request with commits that are not signed off will be rejected by the
`DCO check <https://probot.github.io/apps/dco/>`_.


A DCO is a lightweight way to confirm that a contributor wrote or otherwise has the right
to submit code or documentation to a project. Simply add ``Signed-off-by`` as shown in the example below
to indicate that you agree with the DCO.


The git flag `-s` can be used to sign a commit::

    git commit -s -m 'README.md: Fix minor spelling mistake'


The result is a signed commit message::

    README.md: Fix minor spelling mistake

    Signed-off-by: John Doe <john.doe@example.com>
