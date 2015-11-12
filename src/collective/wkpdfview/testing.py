from Testing.ZopeTestCase.utils import startZServer

from plone.testing import z2
from plone.testing import Layer

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FUNCTIONAL_TESTING
import collective.wkpdfview


class ExternalZServer(Layer):
    defaultBases = (PLONE_FUNCTIONAL_TESTING,)
    def setUp(self):
        # Start two-threaded zserver
        # One will start the phantomjs binary, the other will respond to it
        self['zserver_info'] = startZServer(number_of_threads=2)
    def tearDown(self):
        "Empty: I don't know how to tell the thread to stop"

COLLECTIVE_WKPDFVIEW_EXTERNAL_ZSERVER_FIXTURE = ExternalZServer()


COLLECTIVE_WKPDFVIEW = PloneWithPackageLayer(
    zcml_package=collective.wkpdfview,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.wkpdfview:testing',
    name="COLLECTIVE_WKPDFVIEW")

COLLECTIVE_WKPDFVIEW_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_WKPDFVIEW, ),
    name="COLLECTIVE_WKPDFVIEW_INTEGRATION")

COLLECTIVE_WKPDFVIEW_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_WKPDFVIEW,
           COLLECTIVE_WKPDFVIEW_EXTERNAL_ZSERVER_FIXTURE),
    name="COLLECTIVE_WKPDFVIEW_FUNCTIONAL")