# -*- coding: utf-8 -*-

import os
import json
import jsonlib2
import decimal
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from . import get_vue_url
from uvc.api import api
from plone import api as ploneapi
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from bgetem.medienshop.persistance import getSessionData
from profilehooks import profile
from plone.memoize import ram
from time import time

from bgetem.medienshop.interfaces import (
    BRANCHEN, themenabisz, bgetembranchen, bgetemzielgruppen, bgetemmedienart)


try:
    from collective.solr.parser import SolrResponse
    Solr = True
except:
    Solr = False


api.templatedir('templates')


def getPlaceholder(medienart, artikelnummer):
    if medienart == 'K07':
        return 'azubipaket.jpg'
    if medienart in ['P01', 'P02', 'P03', 'P04', 'P05', 'P08']:
        return 'regelwerk.jpg'
    if artikelnummer.startswith('BZ'):
        return 'betriebsanweisungen.jpg'
    if artikelnummer in ['SZ019', 'SZ020', 'SZ021', 'SZ022', 'SZ023']:
        return 'gbo.jpg'
    if artikelnummer.startswith('SZ'):
        return 'checklisten.jpg'
    return 'shopping-cart.png'

class servicePlaceholder(api.View):
    api.context(Interface)

    def render(self):
        ret = {'imageid':''}
        medienart = self.request.get('medienart')
        artikelnummer = self.request.get('artikelnummer')
        if artikelnummer and medienart:
            ret['imageid'] = getPlaceholder(medienart, artikelnummer)
            print getPlaceholder(medienart, artikelnummer)
        payload = jsonlib2.write(ret)
        return payload


def formatMoney(price):
    cents = decimal.Decimal('.01')
    money = price.quantize(cents, decimal.ROUND_HALF_UP)
    money = str(money).replace('.', ',')
    return money


def getVersandkosten():
    return '3,50'


def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)


class Artikelliste(api.View):
    api.context(Interface)

    def getFiles(self, folder):
        return [] #Die Dateiliste wird bei Anzeige der Artikelliste nicht benötigt
        brains = folder.getFolderContents()
        return [obj.getObject() for obj in brains if obj.portal_type == "File"]

    def getShopUrl(self):
        return self.context.absolute_url_path()

    def isCollection(self):
        if self.context.portal_type == 'Collection':
            return '1'
        return '0'

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

    def checkWebcode(self, suchtext):
        suchtext = suchtext.strip()
        pcat = getToolByName(self.context, 'portal_catalog')
        brains = []
        brains = pcat(Webcode=suchtext)
        url = ''
        if len(brains) == 1:
            url = brains[0].getURL()
        return url    

    def getArtikel(self):
        if self.context.portal_type == 'Collection':
            print 'Artikel aus Kollektion'
            fc = self.context.queryCatalog(batch=False)
            allarts = [i for i in fc if i.portal_type == 'Artikel' and i.review_state == 'published']
            return allarts
        allarts = ploneapi.content.find(
            portal_type='Artikel',
            sort_on='Artikelnummer',
            review_state='published')

        if self.request.get('suchtext'):
            webcodeurl = self.checkWebcode(self.request.get('suchtext'))
            if webcodeurl:
                self.request.response.redirect(webcodeurl)
            solrdicts = ploneapi.content.find(
                portal_type='Artikel', batch=True, b_size=50,
                SearchableText=self.request.get('suchtext'),
                sort_on='Artikelnummer')

            if Solr and isinstance(solrdicts, SolrResponse):
                allarts = []
                for i in solrdicts:
                    try:
                        allarts.append(ploneapi.content.find(UID = i.get('UID'))[0])
                    except:
                        print 'error'
            else:
                allarts = solrdicts

        elif self.request.get('crit'):
            crit = self.request.get('crit')
            wert = self.request.get('wert')
            catquery = {'portal_type':'Artikel',
                        'batch':True,
                        'b_size':50,
                        crit:wert}
            allarts = ploneapi.content.find(**catquery)
        return allarts

    def getArticleJSON(self):
        lo = self.worker()
        return json.dumps(lo)

    @staticmethod
    def theme2dict(theme):
        obj = {}
        for category, subcategories in theme.items():
            vocab = obj[category] = [term.title for term in subcategories]
        return obj

    @staticmethod
    def theme2array(theme):
        obj = [term.title for term in theme]
        return obj

    def getArtikelSelects(self):
        vocabs = {
            'themen': self.theme2array(themenabisz),
            'zielgruppen': self.theme2array(bgetemzielgruppen),
            'medienarten': self.theme2array(bgetemmedienart),
            'branchen': self.theme2dict(BRANCHEN),
        }
        return json.dumps(vocabs)

    def update(self):
        registry = getUtility(IRegistry)
        wartung = registry['bgetem.medienshop.settings.IMedienportalSettings.wartung']
        if wartung:
            print "Wartung"
            url = self.context.absolute_url() + '/wartungsseite'
            return self.request.response.redirect(url)

        self.dev_vue_url = get_vue_url()

        self.medienarten = bgetemmedienart
        self.themen = themenabisz
        self.branchen = bgetembranchen
        self.zielgruppen = bgetemzielgruppen

    #@ram.cache(lambda *args: time() // (60 * 60))
    def worker(self):
        listingobjects = []
        print "WORKER"
        self.formurl = (
            ploneapi.portal.get().absolute_url() +
            '/medienportal/artikelliste')

        allarts = self.getArtikel()
        for art in allarts:
            entry = {}
            obj = art.getObject()
            imagename = getPlaceholder(obj.medienart, obj.artikelnummer)
            placeholderurl = (
                ploneapi.portal.get().absolute_url() + '/' + imagename)

            entry['titelbild'] = placeholderurl
            if obj.titelbild:
                img = "%s/@@images/titelbild/mini" % obj.absolute_url()
                entry['titelbild'] = img
            entry['bildunterschrift'] = ''
            if obj.bildunterschrift:
                entry['bildunterschrift'] = obj.bildunterschrift
            entry['title'] = obj.Title()
            entry['artnr'] = obj.artikelnummer
            entry['desc'] = obj.Description()
            entry['downloads'] = False
            entry['bestand'] = False
            if obj.bestand > 0:
                entry['bestand'] = True
            if obj.medienart in [u'K11', u'P08']:
                entry['downloads'] = True
            if hasattr(obj, 'download_only'):
                if obj.download_only:
                    entry['downloads'] = True
            freimenge = int(obj.freimenge)
            preis_mem = formatMoney(obj.preis_mem)
            preis = formatMoney(obj.preis)
            entry['artbestand'] = float(obj.bestand)
            entry['textversicherte'] = u'Versicherte Unternehmen:<br class="mp-only-bigscreen">%s Freiexemplare, jedes weitere Exemplar %s €' % (freimenge, preis_mem)
            if self.is_user() == 'mitglied':
                entry['textversicherte'] = u'%s Freiexemplare, jedes weitere Exemplar %s €' % (freimenge, preis_mem)

            if self.is_user() == 'notmitglied':
                entry['textversicherte'] = '%s € zzgl. %s € Versandkosten</p>' % (preis, getVersandkosten())
            entry['textbesteller'] = u'Andere Besteller:<br class="mp-only-bigscreen">%s € zzgl. %s € Versandkosten</p>' % (preis, getVersandkosten())
            entry['medienart'] = bgetemmedienart.getTerm(obj.medienart).title
            entry['themen'] = []
            if obj.abisz:
                meinethemen = obj.abisz
                if 'gesundheitsmanagement' in meinethemen:
                    meinethemen.remove('gesundheitsmanagement')
                    meinethemen.append('bgm')
                entry['themen'] = [themenabisz.getTerm(i).title for i in meinethemen]
            entry['zielgruppen'] = []
            if obj.zielgruppen:
                entry['zielgruppen'] = [bgetemzielgruppen.getTerm(i).title for i in obj.zielgruppen]
            entry['branchen'] = []
            if obj.branchen:
                entry['branchen'] = [bgetembranchen.getTerm(i).title for i in obj.branchen]
            entry['downloadurl'] = ''
            entry['filename'] = ''
            entry['downloadclass'] = ''
            if obj.download:
                entry['downloadurl'] = '%s/@@download/download' %obj.absolute_url()
                entry['filetitle'] = obj.download.filename
                filename = 'Datei'
                if obj.filetitle:
                    filename = obj.filetitle
                entry['filename'] = "%s (%s / %s)" % (filename, 
                                                  obj.download.contentType.split('/')[1], 
                                                  sizeof_fmt(obj.download.size))
                entry['downloadclass'] = 'download-link'
            if self.getFiles(obj):
                entry['downloadurl'] = obj.absolute_url()
                entry['filename'] = 'zu den Downloads'
                entry['filetitle'] = 'Downloads'
                entry['downloadclass'] = 'internal-link'
            entry['files_available'] = False    
            if entry.get('downloadurl'):
                entry['files_available'] = True
            entry['artikel'] = obj.absolute_url()
            entry['warenkorb'] = obj.absolute_url()+'/@@tocard?redirect=' + self.context.absolute_url()
            listingobjects.append(entry)
        return listingobjects
        self.listingobjects = listingobjects
        self.listingnumber = "Gefundene Artikel: %s" % len(self.listingobjects)
        print self.listingnumber
