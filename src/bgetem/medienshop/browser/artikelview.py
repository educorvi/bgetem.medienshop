# -*- coding: utf-8 -*-
import decimal
from zope.interface import Interface
from bgetem.medienshop.browser.artikelliste import getPlaceholder, formatMoney, getVersandkosten
from uvc.api import api
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from bgetem.medienshop.persistance import getSessionData
from bgetem.medienshop.interfaces import themenabisz, bgetembranchen, bgetemzielgruppen, bgetemmedienart

api.templatedir('templates')

def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)

class ArtikelView(api.View):
    api.context(Interface)

    def getImages(self):
        brains = self.context.getFolderContents()
        return [obj.getObject().absolute_url() for obj in brains if obj.portal_type=="Image"]

    def getFiles(self):
        brains = self.context.getFolderContents()
        return [obj.getObject() for obj in brains if obj.portal_type=="File"]

    def getArtikelRefs(self):
        if self.context.artikelreferenzen:
            try:
                return [i.to_object for i in self.context.artikelreferenzen]
            except:
                return []
        return []

        pcat = getToolByName(self.context, 'portal_catalog')
        brains = pcat(id = self.context.artikelreferenzen)
        return brains

    def splitContentBoxes(self, folderobjects, size=5):
        seq = []
        for i in folderobjects:
            box = {}
            obj = i.getObject()
            box['title'] = obj.title
            signalcolor = 'blau'
            box['boxclass'] = 'col-xs-6 col-md-5 panel panel-primary panel-siguv %s' %signalcolor
            box['titleclass'] = signalcolor
            box['imgurl'] = ''
            box['imgcaption'] = ''
            if obj.titelbild:
                img = "%s/@@images/titelbild" % obj.absolute_url()
                box['imgurl'] = '<img src=%s width="%s">' % (img, "100%")
            box['url'] = obj.absolute_url()
            box['desc'] = obj.Description
            seq.append(box)
        return [seq[i:i+size] for i  in range(0, len(seq), size)]

    def update(self):
        registry = getUtility(IRegistry)
        wartung = registry['bgetem.medienshop.settings.IMedienportalSettings.wartung']
        if wartung:
            print "Wartung"
            url = self.context.absolute_url() + '/wartungsseite'
            return self.request.response.redirect(url)
        self.userdata = getSessionData(self.request)
        self.verif = False
        self.notmitglied = False
        if self.userdata.get('email'):
            if self.userdata.get('item')[0].get('MITNR'):
                self.verif = self.userdata.get('item')[0].get('VERIF')
            else:
                if self.userdata.get('item')[0].get('VERIF'):
                    self.notmitglied = True
        self.preis = formatMoney(self.context.preis)
        self.preis_mem = formatMoney(self.context.preis_mem)
        self.download_only = False
        self.bestand = False
        self.bestandsmenge = int(self.context.bestand)
        if self.context.bestand > 0:
            self.bestand = True
        if self.context.medienart in [u'K11', u'P08']:
            self.download_only = True
        if hasattr(self.context, 'download_only'):
            if self.context.download_only:
                self.download_only = True
        self.freimenge = int(self.context.freimenge)
        self.warenkorb = self.context.absolute_url()+'/@@tocard?redirect=' + self.context.absolute_url()
        imagename = getPlaceholder(self.context.medienart, self.context.artikelnummer)
        placeholderurl = ploneapi.portal.get().absolute_url() + '/' + imagename
        self.titleimg = placeholderurl
        self.textversicherte = u"Versicherte Unternehmen:<br/>%s Freiexemplare, jedes weitere Exemplar %s €" % (self.freimenge, self.preis_mem)
        self.textbesteller = u"Andere Besteller:<br>%s € zzgl. %s € Versandkosten</p>" % (self.preis, getVersandkosten())
        if self.download_only:
            self.textversicherte = u"Diesen Artikel können Sie nicht bestellen, sondern nur herunterladen."
            self.textbesteller = u""
        if self.verif:
            self.textversicherte = u"%s Freiexemplare, jedes weitere Exemplar %s €" % (self.freimenge, self.preis_mem)
            self.textbesteller = u""
        if self.notmitglied:
            self.textversicherte = u"%s € zzgl. %s € Versandkosten</p>" % (self.preis, getVersandkosten())
            self.textbesteller = u""
        if self.context.titelbild:
            self.titleimg = '%s/@@images/titelbild' % self.context.absolute_url()
        self.bildunterschrift = ''
        if self.context.bildunterschrift:
            self.bildunterschrift = self.context.bildunterschrift
        self.kurzbeschreibung = self.context.description
        self.beschreibung = ''
        if self.context.beschreibung:
            self.beschreibung = self.context.beschreibung.output
        self.images = []
        if self.titleimg:
            self.images = [self.titleimg]
        images = self.getImages()
        if images:
            self.images = [self.titleimg] + images
        self.downloads = []
        if self.context.download:
            entry = {}
            entry['url'] = '%s/@@download/download' %self.context.absolute_url()
            filename = self.context.download.filename
            if self.context.filetitle:
                filename = self.context.filetitle
            entry['name'] = filename
            entry['werte'] = "%s / %s" % (self.context.download.contentType.split('/')[1], sizeof_fmt(self.context.download.size))
            self.downloads.append(entry)
        for i in self.getFiles():
            entry = {}
            entry['url'] = i.absolute_url()+'/@@download/file'
            entry['name'] = "%s" % i.title
            entry['werte'] = "%s / %s" % (i.content_type.split('/')[1], sizeof_fmt(i.size()))
            self.downloads.append(entry)
        self.abisz = []
        if self.context.abisz:
            for i in self.context.abisz:
                if i == 'gesundheitsmanagement':
                    i = 'bgm'
                self.abisz.append(themenabisz.getTerm(i).title)
            self.abisz = ', '.join(self.abisz)
        self.branchen = []
        if self.context.branchen:
            for i in self.context.branchen:
                self.branchen.append(bgetembranchen.getTerm(i).title)
            self.branchen = ', '.join(self.branchen)
        self.zielgruppen = []
        if self.context.zielgruppen:
            for i in self.context.zielgruppen:
                self.zielgruppen.append(bgetemzielgruppen.getTerm(i).title)
            self.zielgruppen = ', '.join(self.zielgruppen)
        try:
            self.medienart = bgetemmedienart.getTerm(self.context.medienart).title
        except:
            self.medienart = u''
        self.artnr = self.context.artikelnummer
        self.objectlist = []
        if self.context.artikelreferenzen:
            refobjects = self.getArtikelRefs()
            for i in refobjects:
                item = {}
                imagename = getPlaceholder(i.medienart, i.artikelnummer)
                placeholderurl = ploneapi.portal.get().absolute_url() + '/' + imagename
                item['img'] = placeholderurl
                item['title'] = i.title
                item['desc'] = i.description
                item['url'] = i.absolute_url()
                if i.titelbild:
                    item['img'] = '%s/@@images/titelbild' % i.absolute_url()
                self.objectlist.append(item)
