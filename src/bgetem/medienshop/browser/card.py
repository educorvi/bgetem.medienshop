# -*- coding: utf-8 -*-

import os
import json

from . import get_vue_url
from five import grok
from uvc.api import api
from zope import schema
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from zope.schema.vocabulary import SimpleVocabulary
from ukbg.theme.interfaces import IThemeSpecific
from zeam.form.base.widgets import ActionWidget
from zeam.form.base import interfaces
from zeam.form.plone import Form
from zeam.form.base import Fields, action
from zeam.form.base.markers import Marker
from plone.dexterity.content import Container
from plone import api as ploneapi
from zope.component.interfaces import IFactory
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from collective.beaker.interfaces import ISession
from bgetem.medienshop.interfaces import IArtikelListe, IBestellung
from bgetem.medienshop.persistance import getSessionData
#from bghw.mediashop.lib.mailer import createMessage, createOrderMessage
#from bghw.mediashop.lib.service import addToWS
from bgetem.medienshop.browser.artikelliste import formatMoney, getPlaceholder

api.templatedir('templates')


def getCartCookie(request):
    """
    Liest das SessionCookie
    """
    session = ISession(request)
    cart_default = {} #leere Artikelliste
    cookie = session.get('cart', cart_default)
    delkeys = []
    for i in cookie:
        try:
            if int(cookie[i]['menge']) <= 0:
                delkeys.append(i)
        except:
            print i
    for i in delkeys:
        del cookie[i]
    return cookie


def setCartCookie(cookie, request):
    """
    Schreibt das Cookie in die Session
    """
    session = ISession(request)
    session['cart'] = cookie
    session.save()

    
class ToCard(api.View):
    """View-Klasse um Daten in die Session zu schreiben"""
    api.context(Interface)

    def update(self):
        url = self.request.get('redirect')
        teststring = ploneapi.portal.get().absolute_url()
        if not url.startswith(teststring):
            message = u'Bei der Übertragung Ihres Artikels in den Warenkorb ist ein Fehler aufgetreten'
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            errorurl = ploneapi.portal.get().absolute_url() + '/medienportal'
            return self.redirect(errorurl)
        cookie = getCartCookie(self.request)
        img = getPlaceholder(self.context.medienart, self.context.artikelnummer) 
        if self.context.titelbild:
            img = "%s/@@images/titelbild" % self.context.absolute_url()
        if not cookie.has_key(self.context.UID()):
            cookie[self.context.UID()] = {
                'image': img,
                'freimenge': float(self.context.freimenge),
                'preis': float(self.context.preis),
                'preis_mem': float(self.context.preis_mem),
                'artikel': self.context.title,
                'bestellung': self.context.artikelnummer,
                'artbestand': float(self.context.bestand),
                'menge': 1,
                'uri': self.context.absolute_url()
            }
            setCartCookie(cookie, self.request)
        else:
            menge = cookie[self.context.UID()]['menge']
            menge += 1
            cookie[self.context.UID()] = {
                'image': img,
                'preis': float(self.context.preis),
                'preis_mem': float(self.context.preis_mem),
                'artikel': self.context.title,
                'bestellung': self.context.artikelnummer,
                'artbestand': float(self.context.bestand),
                'menge': menge,
                'uri': self.context.absolute_url()
            }
            setCartCookie(cookie, self.request)

    def render(self):
        url = self.request.get('redirect')
        return self.redirect(url)


class DelCard(grok.View):
    """View-Klasse um die Daten des Cookies zu loeschen"""
    grok.context(Interface)

    def update(self):
        session = ISession(self.request)
        del session['cart']
        session.save()

    def render(self):
        url = self.request.get('redirect')
        return self.request.response.redirect(url)


class UpdateCart(grok.View):
    api.context(Interface)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def update(self):
        cart = self.request.form.get('cart')
        if cart is not None:
            cookie = json.loads(cart)
            setCartCookie(cookie, self.request)

    def render(self):
        return 'OK'


class GetCart(grok.View):
    api.context(Interface)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def update(self):
      cookie = getCartCookie(self.request)
      self.cart = json.dumps(cookie)

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return self.cart
    

class VueCart(grok.View):
    api.context(Interface)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getShopUrl(self):
        return self.context.absolute_url_path()


    def is_user(self):
        ret = 'anon'
        userdata = getSessionData(self.request)
        if userdata.get('email'):
            if userdata.get('item')[0].get('MITNR'):
                if userdata.get('item')[0].get('VERIF'):
                    ret = 'mitglied'
            else:
                if userdata.get('item')[0].get('VERIF'):
                    ret = 'notmitglied'
        return ret


    def update(self):
        # Lesen des Cookies aus der Session
        self.dev_vue_url = get_vue_url()
        cookie = getCartCookie(self.request)
        self.cart = json.dumps(cookie)
        print self.cart


class Order(Container):
    """Objekt fuer die Artikelliste der Bestellung"""
    grok.implements(IArtikelListe)


class OrderFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('bgetem.medienshop.interfaces.IArtikelListe')

    def __call__(self, **kw):
        return  Order(**kw)


class medienBestellung(api.Form):
    """Form fuer die Bestellung"""
    api.context(Interface)
    fields = api.Fields(IBestellung)
    fields['bestellung'].allowOrdering = False
    fields['bestellung'].mode = "vue_input_widget"
    grok.implements(IArtikelListe)

    for field in fields:
        field.prefix = ''
    prefix = ''

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def update(self):
        #Lesen des Cookies aus der Session
        cookie = getCartCookie(self.request)
        
        #Loeschen von Artikeln in der Session wenn im Formular geloescht wird
        if self.request.form.get('bestellung.remove'):
            requestkeys = self.request.keys()
            for i in requestkeys:
                if i.startswith('bestellung.checked'):
                    fieldid = i.split('.')[-1]
                    delart = self.request.get(
                        'bestellung.field.%s.field.artikel' % fieldid)
                    del cookie[delart]
            setCartCookie(cookie, self.request)
            if not cookie:
                return self.request.response.redirect(self.context.absolute_url())

        #Default - Belegung des Formularfeldes Bestellung
        mydefault = []
        for i in cookie:
            mydefault.append(Order(artikel = i,
                                   bestellnummer = cookie[i]['bestellung'],
                                   beschreibung = cookie[i]['artikel'],
                                   anzahl = cookie[i]['menge']))
        self.fields.get('bestellung').defaultValue = mydefault
        
    @api.action('Mit der Bestellung fortfahren')
    def handle_send(self):
        data, errors = self.extractData()
        if errors:
            # print "GOT ERRORS " + str(errors)
            return
        bestellcookie = {}
        for i in data.get('bestellung'):
            artdict = {}
            artdict['artikel'] = i.beschreibung
            artdict['bestellung'] = i.bestellnummer
            artdict['menge'] = i.anzahl
            bestellcookie[i.artikel] = artdict
        setCartCookie(bestellcookie, self.request)
        url = self.context.absolute_url() + '/loginform'
        self.response.redirect(url)

        
class ActionWidget(ActionWidget):

    grok.adapts(
        interfaces.IAction,
        interfaces.IFieldExtractionValueSetting,
        IThemeSpecific)

    def htmlClass(self):
        return 'btn btn-primary'


class My_Fields(grok.View):
    grok.context(Interface)


class ThankYouView(api.Page):
    grok.context(Interface)
