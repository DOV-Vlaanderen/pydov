# Contributing to pydov

## Introduction

The pydov package is a community effort and everyone is welcome to contribute. It is hosted on [GitHub](https://github.com/DOV-Vlaanderen/pydov) and development is coordinated by [Databank Ondergrond Vlaanderen (DOV)](https://dov.vlaanderen.be/dovweb/html/index.html). DOV aggregates data about soil, subsoil and groundwater of Flanders and makes them publicly available. Interactive and human-readable extraction and querying of the data is provided by a [web application](https://www.dov.vlaanderen.be/portaal/?module=verkenner#ModulePage), whereas the focus of this package is to support **machine-based** extraction and conversion of the data. The latter aims to support a set of complementary use cases, for example:

* integrate DOV data in larger data processing pipelines
* support the reproducibility and/or repeatability of research studies
* integrate the data in third-party applications

The machine-based availability of the data can potentially serve a diverse community of researchers, consultants, modelers, and students. As performant and proper functioning of DOV data processing is of interest to the variety of users, we believe that a community-based effort to develop and maintain these functionalities as an open source package provides the optimal development traject.

## Scope of the package

The `pydov` provides in the first place a convenient wrapper around the XML **export** of the [DOV Verkenner](https://www.dov.vlaanderen.be/portaal/?module=verkenner#ModulePage) and related applications, in combination with the available [DOV WMS/WFS webservices](https://dov.vlaanderen.be/dovweb/html/services.html). By combining the information of these web services, different data request use cases can be automated.

The central elements of the package are:

1. `download` class, i.e. extraction part: downloading data based on a single station or a list of stations; this part could be extended towards more powerful `download_****` function, e.g. `download_from_boundingbox`, `download_from_aquifer()`,... These extension functions of the regular `download` will always require some additional service calls, but will end up having a list of stations and reuse the `download` function.
2. `subset_*`, i.e. filter part: this should provide some straightforward functions to filter the downloaded data.
3. `to_***`, i.e. conversion part: the data is stored or exported to a new file-format that could be useful for the user. `to_csv`/ `to_excel` are straight forward examples, but more advanced and domain-specific export functionalities are envisioned, e.g. `to_modflow()`, `to_menyanthes()`, `to_swap()`

## Contribution is not only code implementation!

Even if you don't feel comfortable contributing code, there are still other ways to help! For instance, documentation is also a very important part and often doesn’t get as much attention as it deserves. If you find a typo in the documentation, or have made improvements, do not hesitate to update the documentation and submit a GitHub pull request (see further on how to do this). If you develop a good introduction tutorial or example case, these are typically the most popular sections for a new user!

It also helps us if you spread the word: refer to the package from your blog and in articles, link to it from your website or integrate the package in a bachelor/masters course.

We aspire to treat everybody equally, and value their contributions. Decisions are made based on technical merit and consensus. We abide by the principles of openness, respect, and consideration of others of the Python Software Foundation: https://www.python.org/psf/codeofconduct/

## Contribute to the repository

The preferred workflow for contributing is to fork the [main repository](https://github.com/DOV-Vlaanderen/pydov) on GitHub, clone locally, and develop on a branch. For more information on this workflow, see the [github workflow](https://guides.github.com/introduction/flow/).

The workflow is provided for command line usage and using the [Github for Desktop](https://desktop.github.com/) application. Feel free to use the environment you like the most.

1. Fork the [project repository](https://github.com/DOV-Vlaanderen/pydov) by clicking on the 'Fork' button near the top right of the page. This creates a copy of the code under your personal GitHub user account.

    ![forkrepo](https://github-images.s3.amazonaws.com/help/bootcamp/Bootcamp-Fork.png)

2. You’ve successfully forked the pydov repository, but so far, it only exists on GitHub. To be able to work on the project, you will need to clone it to your computer.

    Clone your fork of the pydov repo from your GitHub account to your local disk:

    ```bash
    $ git clone https://github.com/DOV-Vlaanderen/pydov.git
    $ cd pydov
    ```

    If you’re using the GitHub for Desktop application, navigate over to the bottom on the right hand side bar and click `Clone in Desktop`. Once you've clicked this, it’ll ask you if you want to launch our desktop application to clone the repository, and where you want to save it. Pick a location on your computer that you feel comfortable with creating files and folders.

    ![clonerepo](https://guides.github.com/activities/forking/clone-in-desktop.png)

3. Create a `my-feature` branch (give it the name of the feature you want to develop) to hold your development changes:

    ```bash
    $ git checkout -b my-feature
    ```

    When using Github for Desktop, in the top left corner of the repository view, create a new branch.
    
    ![](https://desktop.github.com/images/screens/windows/branch.png)

    Always use a `my-feature` branch. It's good practice to **never work on the `master` branch**!

4. Develop the feature on your feature branch. Add changed files using `git add` and then `git commit` files:

    ```bash
    $ git add modified_files
    $ git commit
    ```

    which is similar in Github for Desktop, just craft your commit message in the UI.
   
    ![](https://desktop.github.com/images/screens/windows/craft.png)
    
    Make sure you split your contribution in small commits with well-describing names.

5. Right now, you’ve essentially told Git, “Okay, I’ve taken a snapshot of my changes!” You can continue to make more changes, and take more commit snapshots. When you’re ready to push your changes up to GitHub.com, push the changes to your GitHub account with:

    ```bash
    $ git push -u origin my-feature
    ```

    or, using the Github for Desktop, click on the **Sync** button, which is right above your list of changes.

6. Go to the GitHub web page of your fork of the pydov repo.

    Click the 'Pull request' button to send your changes to the project's maintainers for review. This will send an email to the committers.

    ![pullrequestrepo](https://github-images.s3.amazonaws.com/help/pull_requests/recently_pushed_branch.png)

If any of the above seems like magic to you, please look up the [Git documentation](https://git-scm.com/documentation) on the web, or ask a friend or another contributor for help.

## Coding guidelines

The following are some guidelines on how new code should be written. Of course, there are special cases and there will be exceptions to these rules. However, following these rules when submitting new code makes the review easier so new code can be integrated in less time.

Uniformly formatted code makes it easier to share code ownership. The pydov project tries to closely follow the official Python guidelines detailed in [PEP8](https://www.python.org/dev/peps/pep-0008/) which detail how code should be formatted and indented. Please read it and follow it.

In addition, we add the following guidelines:

* Use underscores to separate words in non class names: `n_samples` rather than `nsamples`.
* Avoid multiple statements on one line. Prefer a line return after a control flow statement (`if/for`).
* Please don’t use `import *` in any case. It is considered harmful by the official Python recommendations. It makes the code harder to read as the origin of symbols is no longer explicitly referenced, but most important, it prevents using a static analysis tool like pyflakes to automatically find bugs.
* Use the [numpy docstring standard](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt) in all your docstrings.

## Creating the documentation

We are glad to accept any sort of documentation: function docstrings, markdown/reStructuredText documents, tutorials, etc. Documentation lives in the `doc/` directory.

You can edit the documentation using any text editor and then generate the HTML output by typing `make html` from the `doc/` directory. For building the documentation, you will need [sphinx](http://sphinx.pocoo.org/).
