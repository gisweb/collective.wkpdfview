import unittest2 as unittest
import transaction

from Products.CMFCore.utils import getToolByName

from plone.app.testing import login, setRoles, TEST_USER_NAME
from plone.app.testing import TEST_USER_ID, TEST_USER_PASSWORD

from urllib2 import urlopen, build_opener
from urllib import quote
from base64 import encodestring

from collective.wkpdfview.testing import\
    COLLECTIVE_WKPDFVIEW_FUNCTIONAL


class TestWkPdfView(unittest.TestCase):

    layer = COLLECTIVE_WKPDFVIEW_FUNCTIONAL

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.wkpdfview'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_download_anonymous_homepage_as_pdf(self):
        portal = self.portal
        path = '/'.join(portal.getPhysicalPath())
        host, port = self.layer['zserver_info']
        url = "http://%(host)s:%(port)i%(path)s/@@wkpdf" % locals()
        result = urlopen(url)
        pdf_data = result.read()
        # PDFs have magic byte %PDF
        self.assertEqual('%PDF', pdf_data[:4])

    def test_download_logged_in_page_as_pdf(self):
        # We create a (private) page
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Document', id='doc')
        transaction.commit() # We're on a different ZODB connection than urllib
        doc = self.portal.doc
        path = '/'.join(doc.getPhysicalPath())
        host, port = self.layer['zserver_info']
        url = "http://%(host)s:%(port)i%(path)s/@@wkpdf" % locals()
        # Build login cookie
        cookie = quote(encodestring(
            '%s:%s' % (TEST_USER_NAME.encode('hex'), TEST_USER_PASSWORD.encode('hex'))
        ).rstrip())
        opener = build_opener()
        opener.addheaders.append(('Cookie', "__ac=%s" % cookie))


        result = opener.open(url)
        pdf_data = result.read()
        # PDFs have magic byte %PDF
        self.assertEqual('%PDF', pdf_data[:4])
        # XXX TODO Check (probably with pdfquery)
        # that our real content is in the PDF, not just an error page

    def test_from_script(self):
        pass # XXX Test that a script like this works:
        # data = context.restrictedTraverse('@@wkpdf')()
        # return data
