============
WIP: This project is in work in progress!
============

============
Image Header
============


.. image:: https://img.shields.io/pypi/v/imageh.svg
        :target: https://pypi.python.org/pypi/imageh

.. image:: https://img.shields.io/travis/ProvoK/imageh.svg
        :target: https://travis-ci.org/ProvoK/imageh

.. image:: https://readthedocs.org/projects/imageh-header/badge/?version=latest
        :target: https://imageh-header.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ProvoK/imageh/shield.svg
     :target: https://pyup.io/repos/github/ProvoK/imageh/
     :alt: Updates


Lightweight library for reading images metadata.


* Free software: MIT license
* Documentation: https://image-header.readthedocs.io/en/latest/.


Why Imageh? Why not PIL?
------------------------

Imageh (Image Header) is lightweight library focused on extracting all possible information from an image header without loading the entire bytes in memory. Only the strict necessary bytes will be read.

I found PIL, despite being a very good library, lacks the possibility to do that. Moreover, PIL has a lot of dependencies.

So, if you are not already using PIL and/or you only need to know basic information about an image, try Imageh!


Features
--------

Imageh let's you retrieve image's metadata from file-like objects or even an URL.

- Supported formats: PNG, GIF. (More coming, please contribute!)
- An easy CLI interface to use Imageh as an utility.
- Multiple output formats (WIP): JSON, XML (More coming, please contribute!)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

