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
    url = http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.11.0_rc1-static-i386.tar.bz2

    [wkhtmltopdf_executable]
    recipe = collective.recipe.cmd
    on_install = true
    on_update = true
    cmds =
         cd ${buildout:directory}/parts/wkhtmltopdf
         chmod +x wkhtmltopdf-i386
         cd ${buildout:directory}/bin
         ln -sf ${buildout:directory}/parts/wkhtmltopdf/wkhtmltopdf-i386 wkhtmltopdf


Purpose
=======

You want a downloadable PDF for some Plone page.
After installing this product you can have it appending `/@@wkpdf` to the url.

You can get a pdf view in a script using `restrictedTraverse('@@wkpdf')()`