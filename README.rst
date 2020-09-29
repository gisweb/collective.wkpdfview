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
    url = https://repo1.maven.org/maven2/com/github/klieber/phantomjs/1.8.1/phantomjs-1.8.1-linux-x86_64.tar.bz2
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

Install PhantomJS (by gw.davide)
================================

First, install or update to the latest system software.

sudo apt-get update
sudo apt-get install build-essential chrpath libssl-dev libxft-dev

Install these packages needed by PhantomJS to work correctly.

sudo apt-get install libfreetype6 libfreetype6-dev
sudo apt-get install libfontconfig1 libfontconfig1-dev

cd ~
export PHANTOM_JS="phantomjs-1.9.8-linux-x86_64"
wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2
sudo tar xvjf $PHANTOM_JS.tar.bz2
Once downloaded, move Phantomjs folder to /usr/local/share/ and create a symlink:

sudo mv $PHANTOM_JS /usr/local/share
sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin
Now, It should have PhantomJS properly on your system.

phantomjs --version


