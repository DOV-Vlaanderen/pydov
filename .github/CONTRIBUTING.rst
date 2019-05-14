
Contributing to pydov
=====================

First of all, thanks for considering contributing to pydov! It's people like you that make it
rewarding for us - the project :ref:`authors` - to work on pydov.

.. _maintainers: .

pydov is an open source project, maintained by people who care. We are not directly funded to do so.


Code of conduct
---------------

Please note that this project is released with a :ref:`code_conduct`.
By participating in this project you agree to abide by its terms.

How you can contribute?
-----------------------

There are several ways you can contribute to this project. If you want to know
more about why and how to contribute to open source projects like this one,
see this `Open Source Guide`_.

.. _Open Source Guide: https://opensource.guide/how-to-contribute/

Share the love
^^^^^^^^^^^^^^

Think pydov is useful? Let others discover it, by telling them in person, via Twitter_ or a blog post.

.. _Twitter: https://twitter.com/DOVdovVO

Using pydov for a paper you are writing? Consider citing it:

    Roel Huybrechts, Stijn Van Hoey, Pieter Jan Haest, Johan Van de Wauw, & Peter Desmet. (2019). DOV-Vlaanderen/pydov. Zenodo. http://doi.org/10.5281/zenodo.2788681

Ask a question ⁉️
^^^^^^^^^^^^^^^^^

Using pydov and got stuck? Browse the documentation_ to see if you
can find a solution. Still stuck? Post your question as a `new issue`_ on GitHub.
While we cannot offer user support, we'll try to do our best to address it,
as questions often lead to better documentation or the discovery of bugs.

Want to ask a question in private? Contact DOV directly by `email`_.

.. _documentation: https://pydov.readthedocs.io/en/latest/index.html
.. _new issue: https://github.com/DOV-Vlaanderen/pydov/issues/new
.. _email: dov@vlaanderen.be

Propose an idea
^^^^^^^^^^^^^^^^

Have an idea for a new pydov feature? Take a look at the documentation_ and
`issue list`_ to see if it isn't included or suggested yet. If not, suggest
your idea as a `new issue`_ on GitHub. While we can't promise to implement
your idea, it helps to:

.. _documentation: https://pydov.readthedocs.io/en/latest/index.html
.. _issue list: https://github.com/DOV-Vlaanderen/pydov/issues
.. _new issue: https://github.com/DOV-Vlaanderen/pydov/issues/new

* Explain in detail how it would work.
* Keep the scope as narrow as possible.

See below, :ref:`docs-technical`,  if you want to contribute code for your idea as well.

Report a bug
^^^^^^^^^^^^

Using pydov and discovered a bug? That's annoying! Don't let others have the
same experience and report it as a `new issue`_ so we can fix it. A good bug
report makes it easier for us to do so, so please include:

.. _new issue: https://github.com/DOV-Vlaanderen/pydov/issues/new

* Your operating system name and version (e.g. Mac OS 10.13.6).
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Improve the documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

Noticed a typo on the website? Think a function could use a better example?
Good documentation makes all the difference, so your help to improve it is very welcome! Maybe you've written a good
introduction tutorial or example case, these are typically very popular sections for new users.

**The website**

`This website`_ is generated with Sphinx_. That means we don't have to
write any html. Content is pulled together from documentation in the code,
notebooks, reStructuredText_ files and the package ``conf.py`` settings. If you
know your way around *Sphinx*, you can `propose a file change`_ to improve
documentation. If not, `report an issue`_ and we can point you in the right direction.

.. _This website: https://pydov.readthedocs.io/en/latest/index.html
.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _propose a file change: https://help.github.com/articles/editing-files-in-another-user-s-repository/
.. _report an issue: https://github.com/DOV-Vlaanderen/pydov/issues/new

For more technical details about the Sphinx setup of the pydov project, See the :ref:`docs-technical` section.

**Function documentation**

Functions are described as comments near their code and translated to
documentation using the  `numpy docstring standard`_. If you want to improve a
function description:

.. _numpy docstring standard: https://numpydoc.readthedocs.io/en/latest/format.html

1. Go to ``pydov/`` directory in the `code repository`_.
2. Look for the file with the name of the function.
3. `Propose a file change`_ to update the function documentation in the docstring (in between the triple quotes).

.. _code repository: https://github.com/DOV-Vlaanderen/pydov
.. _Propose a file change: https://help.github.com/articles/editing-files-in-another-user-s-repository/


Contribute code
^^^^^^^^^^^^^^^

Care to fix bugs or implement new functionality for pydov? Awesome! Have a
look at the `issue list`_ and leave a comment on the things you want
to work on. See also the development guidelines below.

.. _dev-guidelines:

Development guidelines
-----------------------

Coding guidelines
^^^^^^^^^^^^^^^^^^

The following are some guidelines on how new code should be written. Of course,
there are special cases and there will be exceptions to these rules. However,
following these rules when submitting new code makes the review easier so new
code can be integrated in less time.

Uniformly formatted code makes it easier to share code ownership. The
pydov project tries to closely follow the official Python guidelines
detailed in `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ which detail
how code should be formatted and indented. Please read it and follow it.

In addition, we add the following guidelines:

* Use underscores to separate words in non class names: ``n_samples`` rather than ``nsamples``.
* Avoid multiple statements on one line. Prefer a line return after a control flow statement (\ ``if/for``\ ).
* Please don’t use ``import *`` in any case. It is considered harmful by the official Python recommendations. It makes the code harder to read as the origin of symbols is no longer explicitly referenced, but most important, it prevents using a static analysis tool like pyflakes to automatically find bugs.
* Use the `numpy docstring standard`_ in all your docstrings.
* The attributes for specific classes are Pandas data.frames, please use lowercase names (eventually with `_`) as column names.


Contribute to the repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The preferred workflow for contributing is to fork the `main repository <https://github.com/DOV-Vlaanderen/pydov>`_ on GitHub, clone locally, and develop on a branch. For more information on this workflow, see the `github workflow <https://guides.github.com/introduction/flow/>`_.

The workflow is provided for command line usage and using the `Github for Desktop <https://desktop.github.com/>`_ application. Feel free to use the environment you like the most.


#.
   Fork the `project repository <https://github.com/DOV-Vlaanderen/pydov>`_ by clicking on the 'Fork' button near the top right of the page. This creates a copy of the code under your personal GitHub user account.


   .. image:: https://github-images.s3.amazonaws.com/help/bootcamp/Bootcamp-Fork.png
      :target: https://github-images.s3.amazonaws.com/help/bootcamp/Bootcamp-Fork.png
      :alt: forkrepo
      :height: 200px


#.
   You’ve successfully forked the pydov repository, but so far, it only exists on GitHub. To be able to work on the project, you will need to clone it to your computer.

    Clone your fork of the pydov repo from your GitHub account to your local disk:

   .. code-block:: bash

       $ git clone https://github.com/DOV-Vlaanderen/pydov.git
       $ cd pydov

   If you’re using the GitHub for Desktop application, navigate over to the bottom on the right hand side bar and click ``Clone in Desktop``. Once you've clicked this, it’ll ask you if you want to launch our desktop application to clone the repository, and where you want to save it. Pick a location on your computer that you feel comfortable with creating files and folders.


   .. image:: https://guides.github.com/activities/forking/clone-in-desktop.png
      :target: https://guides.github.com/activities/forking/clone-in-desktop.png
      :alt: clonerepo
      :height: 200px


#.
   Create a ``my-feature`` branch (give it the name of the feature you want to develop) to hold your development changes:

   .. code-block:: bash

       $ git checkout -b my-feature

   When using Github for Desktop, in the top left corner of the repository view, create a new branch.


   .. image:: https://desktop.github.com/images/screens/windows/branch.png
      :target: https://desktop.github.com/images/screens/windows/branch.png
      :alt:
      :height: 200px

   Always use a ``my-feature`` branch. It's good practice to **never work on the ``master`` branch**\ !

#.
   Develop the feature on your feature branch. Add changed files using ``git add`` and then ``git commit`` files:

   .. code-block:: bash

       $ git add modified_files
       $ git commit

   which is similar in Github for Desktop, just craft your commit message in the UI.


   .. image:: https://desktop.github.com/images/screens/windows/craft.png
      :target: https://desktop.github.com/images/screens/windows/craft.png
      :alt:
      :height: 200px


   Make sure you split your contribution in small commits with well-describing names.

#.
   Right now, you’ve essentially told Git, “Okay, I’ve taken a snapshot of my changes!” You can continue to make more changes, and take more commit snapshots. When you’re ready to push your changes up to GitHub.com, push the changes to your GitHub account with:

   .. code-block:: bash

       $ git push -u origin my-feature

   or, using the Github for Desktop, click on the **Sync** button, which is right above your list of changes.

#.
   Go to the GitHub web page of your fork of the pydov repo.

    Click the 'Pull request' button to send your changes to the project's maintainers for review. This will send an email to the committers.


   .. image:: https://github-images.s3.amazonaws.com/help/pull_requests/recently_pushed_branch.png
      :target: https://github-images.s3.amazonaws.com/help/pull_requests/recently_pushed_branch.png
      :alt: pullrequestrepo
      :height: 200px


If any of the above seems like magic to you, please look up the `Git documentation <https://git-scm.com/documentation>`_ on the web, or ask a friend or another contributor for help.

.. _docs-technical:

Creating the documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

We are glad to accept any sort of documentation: function docstrings, reStructuredText
documents, tutorials, etc. Documentation lives in the ``docs/`` directory.

You can edit the documentation using any text editor and then generate the HTML
output by typing ``make html`` from the ``doc/`` directory. For building the
documentation, you will need `Sphinx`_. The ``_build``
directory is not included in the repository as we rely on CI tooling for the
documentation building. The documentation is checked on Travis_ and build
by `Read the docs`_.

.. _Travis: https://travis-ci.org/DOV-Vlaanderen/pydov
.. _Read the docs: https://readthedocs.org/

For the notebooks in :ref:`tutorials`, the default is to *always* run the code of the notebooks
when the documentation is created. This is defined by the ``nbsphinx_execute = 'always'`` option
in the ``conf.py`` file.

However, when appropriate, this behavior can be undone on the individual level of the
notebook as explained in the `nbsphinx documentation`_.

.. _nbsphinx documentation: https://nbsphinx.readthedocs.io/en/0.3.4/never-execute.html

In short, to make sure a notebook is not rerun, but the content used as such, add the following
to the notebook(!) metadata:

::

  "nbsphinx": {
   "execute": "never"
  }


Release new version
^^^^^^^^^^^^^^^^^^^

In order to create a new release, the following steps need to be done ( on ``master`` branch):

1. Update the :ref:`history` file with the changes compared to the previous version. You could take into account the following sections: ``New features``, ``Minor improvements``, ``Major improvements``, ``Documentation fixes``. Commit the edits (``git commit``).

2. Adjust the version of the code. The repo uses the `bumpversion` package to keep track
of the package version. use the following commands to switch the version:

    - ``bumpversion patch`` to increase version from 1.0.0 to 1.0.1.
    - ``bumpversion minor`` to increase version from 1.0.0 to 1.1.0.
    - ``bumpversion major`` to increase version from 1.0.0 to 2.0.0.

3. Push the code to GitHub, `git push origin master`
4. Push the tags to GitHub, ``git push --tags`` to create the release in Github
5. `Travis.ci`_ is used to push the distribution archives to pypi_. Make sure to have a look at the pypi_ pydov page to verify this. If not, check the `packaging instructions`_ to do it manually, it basically boils down to ``python3 setup.py sdist bdist_wheel`` and ``twine upload dist/*``.

The new release can be installed using ``pip``, ``pip install --upgrade pydov``.

.. _Travis.ci: https://travis-ci.org/DOV-Vlaanderen/pydov
.. _pypi: https://pypi.org/project/pydov/
.. _packaging instructions: https://packaging.python.org/tutorials/packaging-projects/
