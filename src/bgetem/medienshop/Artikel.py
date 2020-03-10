from five import grok
from plone.indexer import indexer
from plone.dexterity.content import Container
from five import grok
from bgetem.medienshop.interfaces import IArtikel
from bgetem.medienshop.interfaces import themenabisz, bgetembranchen, bgetemzielgruppen, bgetemmedienart, medienkonzept
from sapshopapi import sapshopapi

class Artikel(Container, sapshopapi.ArticleMixin):
    grok.implements(IArtikel)

    def __before_publishing_traverse__(self, object, request):
        super(Artikel, self).__before_publishing_traverse__(object, request)
        object.load()

    def getSAPContent(self):
        sap = {}
        sap['preismitglied'] = 0.10
        sap['preis'] = 0.15
        sap['freimenge'] = 10
        sap['versandkosten'] = 3.50
        return sap

    def getArticleNumber(self):
        return self.artikelnummer

    def getArticle(self, matnr):
        return sapshopapi.getArticle(matnr)

@indexer(IArtikel)
def myArtikelnummer(obj):
    return obj.artikelnummer
grok.global_adapter(myArtikelnummer, name="Artikelnummer")

@indexer(IArtikel)
def myMedienart(obj):
    return obj.medienart
grok.global_adapter(myMedienart, name="Medienart")

@indexer(IArtikel)
def myThemen(obj):
    return obj.abisz
grok.global_adapter(myThemen, name="Themen")

@indexer(IArtikel)
def myZielgruppen(obj):
    return obj.zielgruppen
grok.global_adapter(myZielgruppen, name="Zielgruppen")

@indexer(IArtikel)
def myBranchen(obj):
    return obj.branchen
grok.global_adapter(myBranchen, name="Branchen")

@indexer(IArtikel)
def myHandlungsebenen(obj):
    return obj.handlungsebenen
grok.global_adapter(myHandlungsebenen, name="Handlungsebenen")

@indexer(IArtikel)
def myMedienkonzept(obj):
    return obj.medienkonzept
grok.global_adapter(myMedienkonzept, name="Medienkonzept")

@indexer(IArtikel)
def SearchableText(obj):
    texte = ' '.join([obj.Title(), obj.Description()])
    if obj.beschreibung:
        texte = ' '.join([obj.Title(), obj.Description(), obj.beschreibung.raw])
    if obj.zielgruppen:
        texte += ' '.join([bgetemzielgruppen.getTerm(i).title for i in obj.zielgruppen])
    if obj.abisz:
        meinethemen = obj.abisz
        if 'gesundheitsmanagement' in meinethemen:
            meinethemen.remove('gesundheitsmanagement')
            if not 'bgm' in meinethemen:
                meinethemen.append('bgm')
        texte += ' '.join([themenabisz.getTerm(i).title for i in meinethemen])
    if obj.medienart:
        texte += ' %s' %bgetemmedienart.getTerm(obj.medienart).title
    if obj.branchen:
        texte += ' '.join([bgetembranchen.getTerm(i).title for i in obj.branchen])
    if obj.medienkonzept:
        texte += ' %s' %medienkonzept.getTerm(obj.medienkonzept).title
    if obj.artikelnummer:
        texte += ' %s %s' %(obj.artikelnummer, obj.artikelnummer.replace(' ', ''))
    return texte

@indexer(IArtikel)
def IndexWebcode(obj):
    return obj.webcode
