.. contents::

Introduction
============

This product is currently just a working stub.

Use at your own risk.


Prerequisites
=============

You need to install wkhtmltopdf somewhere in PATH.

Alternatively you can provide the path to wkhtmltopdf
in the WKHTMLTOPDF_PATH environment variable.

You can download it in a buildout this way::

    [wkhtmltopdf]
    recipe = hexagonit.recipe.download
    url = http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.11.0_rc1-static-amd64.tar.bz2

    [wkhtmltopdf_executable]
    recipe = collective.recipe.cmd
    on_install = true
    on_update = true
    cmds =
         cd ${buildout:directory}/parts/wkhtmltopdf
         chmod +x wkhtmltopdf-amd64
         cd ${buildout:directory}/bin
         ln -sf ${buildout:directory}/parts/wkhtmltopdf/wkhtmltopdf-amd64 wkhtmltopdf

This will give you bin/wkhtmltopdf for a linux amd64 architecture.
Change amd64 to i386 if you run a 32 bit kernel.

To tell collective.wkhtmltopdf the location of your binary use::

    environment-vars =
        WKHTMLTOPDF_PATH ${buildout:directory}/bin/wkhtmltopdf


Caveat
======

wkhtmltopdf will issue http requests to Plone, keeping one of its threads busy
in the meantime. Some care must be taken to avoid deadlocks.
By default it will try to connect to the same url used by the end user.
You can override the host/port with the environment variable WKHTMLTOPDF_BASE::

    WKHTMLTOPDF_BASE localhost:8080

Virtualhosts will be preserved so that links in the PDFs will be the same seen by users.



Purpose
=======

You want a downloadable PDF for some Plone page.
After installing this product you can have it appending `/@@wkpdf` to the url.

You can get a pdf view in a script using `restrictedTraverse('@@wkpdf')()`