from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.wkpdfview


COLLECTIVE_WKPDFVIEW = PloneWithPackageLayer(
    zcml_package=collective.wkpdfview,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.wkpdfview:testing',
    name="COLLECTIVE_WKPDFVIEW")

COLLECTIVE_WKPDFVIEW_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_WKPDFVIEW, ),
    name="COLLECTIVE_WKPDFVIEW_INTEGRATION")

COLLECTIVE_WKPDFVIEW_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_WKPDFVIEW, ),
    name="COLLECTIVE_WKPDFVIEW_FUNCTIONAL")
