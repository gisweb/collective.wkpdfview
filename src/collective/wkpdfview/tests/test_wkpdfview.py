import unittest2 as unittest
import transaction

from Products.CMFCore.utils import getToolByName
from Products.SiteAccess.VirtualHostMonster import manage_addVirtualHostMonster

from plone.app.testing import login, setRoles, TEST_USER_NAME
from plone.app.testing import TEST_USER_ID, TEST_USER_PASSWORD

from urllib2 import urlopen, build_opener
from urllib import quote
from base64 import encodestring

from pdfquery import PDFQuery
from StringIO import StringIO

from collective.wkpdfview.testing import\
    COLLECTIVE_WKPDFVIEW_FUNCTIONAL


class TestWkPdfView(unittest.TestCase):

    layer = COLLECTIVE_WKPDFVIEW_FUNCTIONAL

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal.setTitle('PdfPortal')
        transaction.commit()
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
        self.pdf_contains(pdf_data, 'PdfPortal')

    def test_with_virtualhost(self):
        manage_addVirtualHostMonster(self.app, 'virtual_hosting')
        transaction.commit()
        path = ("/VirtualHostBase/http/some_host:80/%s/VirtualHostRoot/" %
         self.portal.getId())
        host, port = self.layer['zserver_info']
        url = "http://%(host)s:%(port)i%(path)s/@@wkpdf" % locals()
        result = urlopen(url)
        pdf_data = result.read()
        self.pdf_contains(pdf_data, 'PdfPortal')

    def test_download_logged_in_page_as_pdf(self):
        # We create a (private) page
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Document', id='doc')
        doc = self.portal.doc
        doc.setTitle('A very FOOBAR title')
        doc.reindexObject()
        transaction.commit() # We're on a different ZODB connection than urllib
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
        self.pdf_contains(pdf_data, 'FOOBAR')


    def test_from_script(self):
        # Test that a script like this works:
        # data = context.restrictedTraverse('@@wkpdf').get_pdf_file()
        # return data
        from Products.PythonScripts.PythonScript import manage_addPythonScript
        manage_addPythonScript(self.portal, 'test_script')
        self.portal.test_script.ZPythonScript_edit('', 'return '
            "context.restrictedTraverse('@@wkpdf').get_pdf_file()")
        transaction.commit()
        host, port = self.layer['zserver_info']
        portalid = self.portal.getId()
        url = "http://%(host)s:%(port)i/%(portalid)s/test_script" % locals()
        result = urlopen(url)
        pdf_data = result.read()
        self.pdf_contains(pdf_data, 'PdfPortal')


    def pdf_contains(self, pdf_haystack, needle):
        # PDFs have magic byte %PDF
        self.assertEqual('%PDF', pdf_haystack[:4])
        # Check (with pdfquery)
        # that our real content is in the PDF, not just an error page
        parsed = PDFQuery(StringIO(pdf_haystack))
        # pdfquery chokes on these document attributes.
        # Let's remove NULL bytes from them
        parsed.doc.info[0]['Creator'] = 'test'
        parsed.doc.info[0]['Producer'] = 'Plone and phantomjs'
        parsed.doc.info[0]['Title'] = 'A valid title'
        parsed.load()
        self.assertTrue(parsed.pq(':contains("%s")' % needle))
