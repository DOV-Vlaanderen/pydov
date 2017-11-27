
Contributing to pydov
=====================

Contribute to the repository
----------------------------

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

Coding guidelines
-----------------

The following are some guidelines on how new code should be written. Of course, there are special cases and there will be exceptions to these rules. However, following these rules when submitting new code makes the review easier so new code can be integrated in less time.

Uniformly formatted code makes it easier to share code ownership. The pydov project tries to closely follow the official Python guidelines detailed in `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ which detail how code should be formatted and indented. Please read it and follow it.

In addition, we add the following guidelines:


* Use underscores to separate words in non class names: ``n_samples`` rather than ``nsamples``.
* Avoid multiple statements on one line. Prefer a line return after a control flow statement (\ ``if/for``\ ).
* Please don’t use ``import *`` in any case. It is considered harmful by the official Python recommendations. It makes the code harder to read as the origin of symbols is no longer explicitly referenced, but most important, it prevents using a static analysis tool like pyflakes to automatically find bugs.
* Use the `numpy docstring standard <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_ in all your docstrings.
* The attributes for specific classes are Pandas data.frames, please use lowercase names (eventually with `_`) as column names.


Contribution is not only code implementation!
---------------------------------------------

Even if you don't feel comfortable contributing code, there are still other ways to help! For instance, documentation is also a very important part and often doesn’t get as much attention as it deserves. If you find a typo in the documentation, or have made improvements, do not hesitate to update the documentation and submit a GitHub pull request (see further on how to do this). If you develop a good introduction tutorial or example case, these are typically the most popular sections for a new user!

It also helps us if you spread the word: refer to the package from your blog and in articles, link to it from your website or integrate the package in a bachelor/masters course.

We aspire to treat everybody equally, and value their contributions. Decisions are made based on technical merit and consensus. We abide by the principles of openness, respect, and consideration of others of the Python Software Foundation: https://www.python.org/psf/codeofconduct/


Creating the documentation
--------------------------

We are glad to accept any sort of documentation: function docstrings, reStructuredText documents, tutorials, etc. Documentation lives in the ``docs/`` directory.

You can edit the documentation using any text editor and then generate the HTML output by typing ``make html`` from the ``doc/`` directory. For building the documentation, you will need `sphinx <http://sphinx.pocoo.org/>`_.


Note for maintainers
--------------------

The repo uses the `bumpversion` package to keep track of the package version. use the following commands to switch the version:

#. ``bumpversion patch`` to increase version from 1.0.0 to 1.0.1.
#. ``bumpversion minor`` to increase version from 1.0.0 to 1.1.0.
#. ``bumpversion major`` to increase version from 1.0.0 to 2.0.0.
