# -*- coding:utf-8 -*-
import os
import xlrd
import transaction
from zope.interface import Interface
from plone import api as ploneapi
from uvc.api import api
from plone.i18n.normalizer import idnormalizer
import string
import transaction
from random import choice
from bgetem.medienshop.interfaces import abiszdict, zielgruppendict, branchendict, bgetemmedienart, themenabisz, bgetembranchen, bgetemzielgruppen
from bgetem.medienshop.interfaces import medienkonzept, mediendict
from bgetem.medienshop.interfaces import genWebcode
from plone.i18n.normalizer import idnormalizer
import mimetypes
from plone.namedfile.file import NamedBlobImage, NamedBlobFile

api.templatedir('templates')
basepath = '/home/bgetem/TestProd/zeocluster/var/share/excelimport'

class ShopRedaktion(api.Page):
    api.context(Interface)

    def update(self):
        self.artikelliste = []
        self.anzeige = 'Alle Artikel'
        if not self.request.get('medium'):
            allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        else:
            allarts = ploneapi.content.find(portal_type='Artikel', Medienart=self.request.get('medium'), sort_on='Artikelnummer')
            self.anzeige = bgetemmedienart.getTerm(self.request.get('medium')).title
        self.artikelzahl = len(allarts)
        for i in allarts:
            entry = {}
            obj = i.getObject()
            entry['artikelnummer'] = obj.artikelnummer
            entry['title'] = obj.title
            entry['url'] = obj.absolute_url()
            entry['warengruppe'] = u''
            entry['bestand'] = obj.bestand
            if obj.medienart:
                try:
                    entry['warengruppe'] = bgetemmedienart.getTerm(obj.medienart).title
                except:
                    entry['warengruppe'] = obj.medienart
            entry['workflow'] = i.review_state
            entry['warenkorb'] = obj.absolute_url()+'/@@tocard?redirect=' + self.context.absolute_url()
            self.artikelliste.append(entry)


class ThemenImport(api.Page):
    api.context(Interface)
  
    def readAllArticle(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        normids = []
        for i in allarts:
            obj = i.getObject()
            artikelnummer = obj.artikelnummer
            art = artikelnummer.lower().strip()
            art = art.replace(' ', '')
            art = art.replace('-', '')
            art = art.replace('_', '')
            normids.append((art, artikelnummer))
        return normids  

    def update(self):
        normids = self.readAllArticle()
        book = xlrd.open_workbook(basepath+"/themen.xls")
        sh = book.sheet_by_index(0)
        goodlist = []
        falselist = []
        notfound = []
        doublelist = []
        for rx in range(55, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel:
                normartikel = excelartikel.lower().strip()
                normartikel = normartikel.replace(' ', '')
                normartikel = normartikel.replace('-', '')
                normartikel = normartikel.replace('_', '')
                checklist = []
                for normid in normids:
                    if normid[0] == normartikel:
                        values = []
                        for i in range(1, 55):
                            if sh.row(rx)[i].value.strip().lower() == u'x':
                                try:
                                    values.append(abiszdict[i])
                                except:
                                    import pdb;pdb.set_trace()
                        brains = ploneapi.content.find(portal_type='Artikel', Artikelnummer=normid[1])
                        if len(brains) == 1:
                            brain = brains[0]
                            obj = brain.getObject()
                            print obj.artikelnummer, values
                            if self.request.get('action'):
                                obj.abisz = values
                                import transaction
                                transaction.savepoint(optimistic=True)
                            goodlist.append(excelartikel)
        for rx in range(55, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel and excelartikel not in goodlist:
                falselist.append((rx+1, excelartikel))
        self.dataset = sh.nrows - 55
        self.goodlistcount = len(goodlist)
        self.falselistcount = len(falselist)
        self.falselist = falselist


class ZielgruppenImport(api.Page):
    api.context(Interface)

    def readAllArticle(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        normids = []
        for i in allarts:
            obj = i.getObject()
            artikelnummer = obj.artikelnummer
            art = artikelnummer.lower().strip()
            art = art.replace(' ', '')
            art = art.replace('-', '')
            art = art.replace('_', '')
            normids.append((art, artikelnummer))
        return normids

    def update(self):
        normids = self.readAllArticle()
        book = xlrd.open_workbook(basepath+"/zielgruppen.xls")
        sh = book.sheet_by_index(0)
        goodlist = []
        falselist = []
        notfound = []
        doublelist = []
        for rx in range(18, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel:
                normartikel = excelartikel.lower().strip()
                normartikel = normartikel.replace(' ', '')
                normartikel = normartikel.replace('-', '')
                normartikel = normartikel.replace('_', '')
                checklist = []
                for normid in normids:
                    if normid[0] == normartikel:
                        values = []
                        for i in range(1, 9):
                            if sh.row(rx)[i].value.strip().lower() == u'x':
                                values.append(zielgruppendict.get(i))
                        brains = ploneapi.content.find(portal_type='Artikel', Artikelnummer=normid[1])
                        if len(brains) == 1:
                            brain = brains[0]
                            obj = brain.getObject()
                            print obj.artikelnummer, values
                            if self.request.get('action'):
                                obj.zielgruppen = values
                                import transaction
                                transaction.savepoint(optimistic=True)
                            goodlist.append(excelartikel)
        for rx in range(18, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel and excelartikel not in goodlist:
                falselist.append((rx+1, excelartikel))
        self.dataset = sh.nrows - 18
        self.goodlistcount = len(goodlist)
        self.falselistcount = len(falselist)
        self.falselist = falselist
 

class BranchenImport(api.Page):
    api.context(Interface)

    def readAllArticle(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        normids = []
        for i in allarts:
            obj = i.getObject()
            artikelnummer = obj.artikelnummer
            art = artikelnummer.lower().strip()
            art = art.replace(' ', '')
            art = art.replace('-', '')
            art = art.replace('_', '')
            normids.append((art, artikelnummer))
        return normids

    def update(self):
        normids = self.readAllArticle()
        book = xlrd.open_workbook(basepath+"/branchen.xls")
        sh = book.sheet_by_index(0)
        goodlist = []
        falselist = []
        notfound = []
        doublelist = []
        for rx in range(36, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel:
                normartikel = excelartikel.lower().strip()
                normartikel = normartikel.replace(' ', '')
                normartikel = normartikel.replace('-', '')
                normartikel = normartikel.replace('_', '')
                checklist = []
                for normid in normids:
                    if normid[0] == normartikel:
                        values = []
                        for i in range(1, 52):
                            if sh.row(rx)[i].value.strip().lower() == u'x':
                                values.append(branchendict.get(i))
                        brains = ploneapi.content.find(portal_type='Artikel', Artikelnummer=normid[1])
                        if len(brains) == 1:
                            brain = brains[0]
                            obj = brain.getObject()
                            print obj.artikelnummer, values
                            if self.request.get('action'):
                                obj.branchen = values
                                import transaction
                                transaction.savepoint(optimistic=True)
                            goodlist.append(excelartikel)
        for rx in range(36, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel and excelartikel not in goodlist:
                falselist.append((rx+1, excelartikel))
        self.dataset = sh.nrows - 36
        self.goodlistcount = len(goodlist)
        self.falselistcount = len(falselist)
        self.falselist = falselist


class MedienImport(api.Page):
    api.context(Interface)

    def readAllArticle(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        normids = []
        for i in allarts:
            obj = i.getObject()
            artikelnummer = obj.artikelnummer
            art = artikelnummer.lower().strip()
            art = art.replace(' ', '')
            art = art.replace('-', '')
            art = art.replace('_', '')
            normids.append((art, artikelnummer))
        return normids

    def update(self):
        normids = self.readAllArticle()
        book = xlrd.open_workbook(basepath+"/medienkonzept.xls")
        sh = book.sheet_by_index(0)
        goodlist = []
        falselist = []
        notfound = []
        doublelist = []
        for rx in range(1, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel:
                normartikel = excelartikel.lower().strip()
                normartikel = normartikel.replace(' ', '')
                normartikel = normartikel.replace('-', '')
                normartikel = normartikel.replace('_', '')
                checklist = []
                for normid in normids:
                    if normid[0] == normartikel:
                        values = []
                        for i in range(1, 4):
                            if sh.row(rx)[i].value.strip().lower() == u'x':
                                values.append(mediendict.get(i))
                        brains = ploneapi.content.find(portal_type='Artikel', Artikelnummer=normid[1])
                        if len(brains) == 1:
                            brain = brains[0]
                            obj = brain.getObject()
                            print obj.artikelnummer, values
                            if self.request.get('action'):
                                if values:
                                    obj.medienkonzept = values[0]
                                    import transaction
                                    transaction.savepoint(optimistic=True)
                            goodlist.append(excelartikel)
        for rx in range(1, sh.nrows):
            excelartikel = sh.row(rx)[0].value
            if excelartikel and excelartikel not in goodlist:
                falselist.append((rx+1, excelartikel))
        self.dataset = sh.nrows - 1
        self.goodlistcount = len(goodlist)
        self.falselistcount = len(falselist)
        self.falselist = falselist


class FileImport(api.Page):
    api.context(Interface)

    def readAllArticle(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        normids = []
        for i in allarts:
            obj = i.getObject()
            artikelnummer = obj.artikelnummer
            art = artikelnummer.lower().strip()
            art = art.replace(' ', '')
            art = art.replace('-', '')
            art = art.replace('_', '')
            normids.append((art, artikelnummer))
        return normids

    def readAllFiles(self):
        ausgabe = os.listdir('/tmp/medienportal_versand')
        mydict = {}
        for i in ausgabe:
            key = i.lower().strip()
            key = key.replace('_', '')
            key = key.replace('-', '')
            key = key.replace(' ', '')
            mydict[key] = i
        return mydict

    def update(self):
        artikel = self.readAllArticle()
        dateien = self.readAllFiles()
        self.numfiles = len(dateien)
        count = 0
        dupcount = 0
        filelist = []
        found = {}
        dups = []
        for i in artikel:
            nummer = i[0]
            for k in dateien.keys():
                if k.startswith(nummer):
                    if nummer not in filelist:
                        filepath = '/tmp/medienportal_versand/%s' % dateien[k]
                        myfile = open(filepath, 'r')
                        content_type = mimetypes.types_map['.'+k.split('.')[-1]]
                        myfilename = myfile.name.decode('iso-8859-2')
                        artikelbrain = ploneapi.content.find(portal_type='Artikel', Artikelnummer=i[1])
                        artikelobj = artikelbrain[0].getObject()
                        #artikelobj.titelbild = NamedBlobImage(data = myfile.read(), contentType=content_type, filename=dateien[k].decode('utf-8'))
                        #import transaction
                        #transaction.savepoint(optimistic=True)
                        print artikelobj, content_type, myfilename
                        filelist.append(nummer)
                        count += 1
                        found[k] = i[1]
                    elif nummer in filelist:
                        dupcount +=1
                        dups.append(k)
        self.count = count
        self.dupcount = dupcount

        notlist = []
        for i in dateien:
            if i not in found and i not in dups:
                notlist.append(dateien[i])
        self.notlist = notlist

        goodlist = []
        for i in sorted(found.keys()):
            goodlist.append((found[i], dateien[i]))
        self.goodlist = goodlist

        duplist = []
        for i in dateien:
            if i in dups:
                duplist.append(dateien[i])
        self.duplist = duplist

    def render(self):
        message = u'<h2>Ergebnis des Dateiimports</h2>'
        message += u'<p>Es wurden %s Dateien gelesen. Davon wurden %s Dateien direkt zugeordnet.\
                    Für %s Artikel wurden mehrere Dateien gefunden.</p>' % (self.numfiles, self.count, self.dupcount)
        message += u'<h2>Für folgende Artikel wurden Dateien zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>Bestellnummer</th><th>Dateiname</th></thead><tbody>'
        for i in self.goodlist:
            message += u'<tr><td>%s</td><td>%s</td></tr>' % (i[0], i[1])
        message += u'</tbody></table>'
        message += u'<h2>Folgende Dateien müssen noch manuell hochgeladen werden:</h2>'
        message += u'<ul>'
        for i in self.duplist:
            message += u'<li>%s</li>' %i 
        message += u'</ul>'
        message += u'<h2>Folgende Dateien konnten nicht zugeordnet werden:</h2>'
        message += u'<ul>'
        for i in self.notlist:
            message += u'<li>%s</li>' %i
        message += u'</ul>'
        return message

class FileChecker(api.Page):
    api.context(Interface)

    def render(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        artlist = []
        message = u'<h2>Für folgende Artikel wurden Dateien zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Dateiname</th><th>Dateigroesse</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if obj.download:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.download.filename, obj.download.size)
                lfd += 1
        message += u'</tbody></table>'
        message += u'<h2>Für folgende Artikel wurden bislang keine Dateien zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Titel</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if not obj.download:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.title)
                lfd += 1
        message += u'</tbody></table>'
        return message


class ImageChecker(api.Page):
    api.context(Interface)

    def render(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        artlist = []
        message = u'<h2>Für folgende Artikel wurden Bilder zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Dateiname</th><th>Dateigroesse</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if obj.titelbild:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.titelbild.filename, obj.titelbild.size)
                lfd += 1
        message += u'</tbody></table>'

        message += u'<h2>Für folgende Artikel wurden bislang keine Bilder zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Titel</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if not obj.titelbild:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.title)
                lfd += 1
        message += u'</tbody></table>'
        return message


class ThemenChecker(api.Page):
    api.context(Interface)

    def render(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        artlist = []
        message = u'<h2>Für folgende Artikel wurden Themen zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Themen</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if obj.abisz:
                submessage = '<ul>'
                for k in obj.abisz:
                    submessage += '<li>%s</li>' % themenabisz.getTerm(k).title
                submessage += '</ul>'
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, submessage)
                lfd += 1
        message += u'</tbody></table>'

        message += u'<h2>Für folgende Artikel wurden bislang keine Themen zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Titel</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if not obj.abisz:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.title)
                lfd += 1
        message += u'</tbody></table>'
        return message


class BranchenChecker(api.Page):
    api.context(Interface)

    def render(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        artlist = []
        message = u'<h2>Für folgende Artikel wurden Branchen zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Branchen</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if obj.branchen:
                submessage = '<ul>'
                for k in obj.branchen:
                    submessage += '<li>%s</li>' % bgetembranchen.getTerm(k).title
                submessage += '</ul>'
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, submessage)
                lfd += 1
        message += u'</tbody></table>'
        message += u'<h2>Für folgende Artikel wurden bislang noch keine Branchen zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Titel</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if not obj.branchen:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.title)
                lfd += 1
        message += u'</tbody></table>'
        return message


class ZielgruppenChecker(api.Page):
    api.context(Interface)

    def render(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        artlist = []
        message = u'<h2>Für folgende Artikel wurden Zielgruppen zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Zielgruppen</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if obj.zielgruppen:
                submessage = '<ul>'
                for k in obj.zielgruppen:
                    submessage += '<li>%s</li>' % bgetemzielgruppen.getTerm(k).title
                submessage += '</ul>'
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, submessage)
                lfd += 1
        message += u'</tbody></table>'
        message += u'<h2>Für folgende Artikel wurden bislang noch keine Zielgruppen zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Titel</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if not obj.zielgruppen:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.title)
                lfd += 1
        message += u'</tbody></table>'
        return message


class MedienChecker(api.Page):
    api.context(Interface)

    def render(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        artlist = []
        message = u'<h2>Für folgende Artikel wurden Werte des Medienkonzepts zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Medienkonzept</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if obj.medienkonzept:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.medienkonzept)
                lfd += 1
        message += u'</tbody></table>'
        message += u'<h2>Für folgende Artikel wurden bislang noch keine Werte des Medienkonzepts zugeordnet:</h2>'
        message += u'<table class="table table-bordered"><thead><th>#</th><th>Bestellnummer</th><th>Titel</th></thead><tbody>'
        lfd = 1
        for i in allarts:
            obj = i.getObject()
            if not obj.medienkonzept:
                message += '<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td></tr>' % (lfd, obj.absolute_url(), obj.artikelnummer, obj.title)
                lfd += 1
        message += u'</tbody></table>'
        return message


class Cleanup(api.Page):
    api.context(Interface)

    def render(self):
        allarts = ploneapi.content.find(portal_type='Artikel', sort_on='Artikelnummer')
        for i in allarts:
            obj = i.getObject()
            if obj.webcode:
                webcode = genWebcode(self.context)
                obj.webcode = webcode
                import transaction
                transaction.savepoint(optimistic=True)
            #if obj.branchen:
            #    import pdb;pdb.set_trace()
            #    #obj.abisz = []
            #    #obj.reindexObject()
            #    #import transaction
            #    #transaction.commit()
            #print obj.abisz
            obj.reindexObject()
        return 'alles sauber'
