# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from bgetem.medienshop.testing import BGETEM_MEDIENSHOP_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that bgetem.medienshop is properly installed."""

    layer = BGETEM_MEDIENSHOP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if bgetem.medienshop is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'bgetem.medienshop'))

    def test_browserlayer(self):
        """Test that IBgetemMedienshopLayer is registered."""
        from bgetem.medienshop.interfaces import (
            IBgetemMedienshopLayer)
        from plone.browserlayer import utils
        self.assertIn(IBgetemMedienshopLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BGETEM_MEDIENSHOP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['bgetem.medienshop'])

    def test_product_uninstalled(self):
        """Test if bgetem.medienshop is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'bgetem.medienshop'))

    def test_browserlayer_removed(self):
        """Test that IBgetemMedienshopLayer is removed."""
        from bgetem.medienshop.interfaces import \
            IBgetemMedienshopLayer
        from plone.browserlayer import utils
        self.assertNotIn(IBgetemMedienshopLayer, utils.registered_layers())
