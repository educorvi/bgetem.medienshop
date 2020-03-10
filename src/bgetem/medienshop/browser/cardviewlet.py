from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.viewlets.interfaces import IBelowContentBody
from plone.app.layout.viewlets.interfaces import IPortalHeader
from plone.app.layout.viewlets.interfaces import IAboveContentTitle
from plone.app.layout.viewlets.interfaces import IBelowContentTitle
from plone.app.layout.viewlets.interfaces import IPortalFooter
from bgetem.medienshop.browser.card import getCartCookie
from bgetem.medienshop.persistance import getSessionData

api.templatedir('templates')

class SearchViewlet(api.Viewlet):
    api.context(Interface)
    api.viewletmanager(IBelowContentTitle)

    def update(self):
        self.shop = ploneapi.portal.get().absolute_url() + '/medienportal'


class CardViewlet(api.Viewlet):
    api.context(Interface)
    api.viewletmanager(IAboveContentTitle)

    #def available(self):
    #    korb = len(getCartCookie(self.request).keys())
    #    if korb == 0:
    #        return False
    #    return False
        
    def _available(self):
        if 'medienportal' in self.context.absolute_url():
            return True
        return False

    def update(self):
        shop = ploneapi.portal.get().absolute_url() + '/medienportal'
        self.available = self._available()
        self.shopbutton = True
        if self.request.get('URL').endswith('vuecart'):
            self.shopbutton = False
        if self.context.absolute_url().endswith('vuecart'):
            self.shopbutton = False
        artikel = getCartCookie(self.request)
        print artikel
        menge = 0
        for i in artikel:
            menge += int(artikel[i].get('menge'))
        #self.artikel = len(getCartCookie(self.request).keys())
        self.artikel = menge
        self.shop_url = shop + '/vuecart'
        self.del_link = shop + '/@@delcard?redirect=%s' % shop
        self.login_link = shop + '/@@loginform'
        self.userdel_link = shop + '/@@deleteuserform'
        self.changepw_link = shop + '/@@changepassword'
        self.changeadr_link = shop + '/@@changeanschrift'
        self.logout_link = shop + '/@@userlogout'
        self.email = getSessionData(self.request).get('email', '')
        self.card = getCartCookie(self.request) 
