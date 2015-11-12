.. contents::

Introduction
============

This product is currently just a working stub.

Use at your own risk.



Purpose
=======

You want a downloadable PDF for some Plone page.
After installing this product you can have it appending `/@@wkpdf` to the url.

You can get a pdf view in a script using `restrictedTraverse('@@wkpdf').get_pdf_file()`


Prerequisites
=============

You need to install phantomjs somewhere in PATH.

Alternatively you can provide the path to phantomjs
in the PHANTOMJS_PATH environment variable.

You can download it in a buildout this way::

    [phantomjs]
    recipe = hexagonit.recipe.download
    url = https://phantomjs.googlecode.com/files/phantomjs-1.8.1-linux-x86_64.tar.bz2
    ignore-existing = true

This will download phantomjs for a linux amd64 architecture.
Change x86_64 to i386 if you run a 32 bit kernel.

To tell collective.wkpdfview the location of your binary use::

    environment-vars =
        PHANTOMJS_PATH ${buildout:directory}/parts/phantomjs/phantomjs-1.7.0-linux-i686/bin/phantomjs


Caveat
======

phantomjs will issue http requests to Plone, keeping one of its threads busy
in the meantime. Some care must be taken to avoid deadlocks.
By default it will try to connect to the same url used by the end user.
This will lead to a deadlock, sooner or later.
You can override the host/port with the environment variable WKHTMLTOPDF_BASE::

    WKHTMLTOPDF_BASE localhost:8080

Virtualhosts will be preserved so that links in the PDFs will be the same seen by users.
