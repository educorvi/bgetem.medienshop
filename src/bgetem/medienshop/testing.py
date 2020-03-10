# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import bgetem.medienshop


class BgetemMedienshopLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=bgetem.medienshop)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bgetem.medienshop:default')


BGETEM_MEDIENSHOP_FIXTURE = BgetemMedienshopLayer()


BGETEM_MEDIENSHOP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BGETEM_MEDIENSHOP_FIXTURE,),
    name='BgetemMedienshopLayer:IntegrationTesting'
)


BGETEM_MEDIENSHOP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BGETEM_MEDIENSHOP_FIXTURE,),
    name='BgetemMedienshopLayer:FunctionalTesting'
)


BGETEM_MEDIENSHOP_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BGETEM_MEDIENSHOP_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='BgetemMedienshopLayer:AcceptanceTesting'
)
