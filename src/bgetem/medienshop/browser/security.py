from DateTime import DateTime
import random
import jsonlib2
import transaction
from zope.interface import Interface
import zExceptions
from uvc.api import api
from plone import api as ploneapi
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.beaker.interfaces import ISessionConfig
from Products.CMFCore.utils import getToolByName
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

api.templatedir('templates')

class NotFound(api.View):
    api.context(zExceptions.NotFound)
    api.name("index.html")

    def render(self):
        self.request.response.status = 404
        return u"404:Not Found"

class SecTest(api.View):
    api.context(Interface)

    def render(self):
        config = getUtility(ISessionConfig)
        print "config = getUtility(ISessionConfig)"
        print "print config: ", config
        print "print config.keys(): ", config.keys()
        print "print config.get('httponly'): ", config.get('httponly')
        print "print config.get('secure'): ", config.get('secure')
        self.request.response.status = 401
        return '401:Unauthorized'

class ResetView(api.View):
    api.context(Interface)

    def render(self):
        self.context.artikelreferenzen = []
        transaction.commit()
        url = self.context.absolute_url() + '/edit'
        return self.request.redirect(url)

def genWebcode(context):
    aktuell=unicode(DateTime()).split(' ')[0]
    neujahr='%s/01/01' %str(DateTime()).split(' ')[0][:4]
    konstante=unicode(aktuell[2:4])
    zufallszahl=unicode(random.randint(100000, 999999))
    code=konstante+zufallszahl
    pcat=getToolByName(context,'portal_catalog')
    results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
    while results:
        zufallszahl=unicode(random.randint(100000, 999999))
        code=konstante+zufallszahl
        results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
    mediencode = "M%s" %code
    return mediencode


class MedienWebcode(api.View):
    api.context(Interface)

    def render(self):
        brains = ploneapi.content.find(portal_type=['Folder', 'Collection', 'Artikel'])
        menge = len(brains)
        for i in brains:
            obj = i.getObject()
            obj.webcode = "M%s" %obj.webcode
            obj.reindexObject()
            transaction.commit()
        return "%s Objekte reindexiert" %menge

class RenewWebcode(api.Page):
    api.context(Interface)

    def render(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        brains = ploneapi.content.find(Webcode = self.request.get('webcode'))
        for i in brains:
            obj = i.getObject()
            newcode = genWebcode(self.context)
            obj.webcode = newcode
            obj.reindexObject()
        return u"Fertig"

class Medienwartung(api.View):
    api.context(Interface)

    def render(self):
        registry = getUtility(IRegistry)
        wartung = registry['bgetem.medienshop.settings.IMedienportalSettings.wartung']
        data = {'wartung':False}
        if wartung:
            data = {'wartung':True}
        payload = jsonlib2.write(data)
        return payload
            
class Wartungsseite(api.Page):
    api.context(Interface)

 
class setWartung(api.View):
    api.context(Interface)

    def render(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        ret = {u'wartung':u'es ist ein Fehler aufgetreten'}
        if not ploneapi.user.is_anonymous():
            user = ploneapi.user.get_current()
            if user:
                roles = ploneapi.user.get_roles(user = user)
                if not 'Manager' in roles:
                    self.request.response.status = 403
                    return u"403:Forbidden"
        else:
            self.request.response.status = 401
            return u"401:Unauthorized"

        registry = getUtility(IRegistry)
        registry['bgetem.medienshop.settings.IMedienportalSettings.wartung'] = True
        ret = {'wartung':True}
        payload = jsonlib2.write(ret)
        return payload


class unsetWartung(api.View):
    api.context(Interface)

    def render(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        ret = {u'wartung':u'es ist ein Fehler aufgetreten'}
        if not ploneapi.user.is_anonymous():
            user = ploneapi.user.get_current()
            if user:
                roles = ploneapi.user.get_roles(user = user)
                if not 'Manager' in roles:
                    self.request.response.status = 403
                    return u"403:Forbidden"
        else:
            self.request.response.status = 401
            return u"401:Unauthorized"

        registry = getUtility(IRegistry)
        registry['bgetem.medienshop.settings.IMedienportalSettings.wartung'] = False
        ret = {'wartung':False}
        payload = jsonlib2.write(ret)
        return payload


class getWartung(api.View):
    api.context(Interface)

    def render(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        ret = {u'wartung':u'es ist ein Fehler aufgetreten'}
        if not ploneapi.user.is_anonymous():
            user = ploneapi.user.get_current()
            if user:
                roles = ploneapi.user.get_roles(user = user)
                if not 'Manager' in roles:
                    self.request.response.status = 403
                    return u"403:Forbidden"
        else:
            self.request.response.status = 401
            return u"401:Unauthorized"

        registry = getUtility(IRegistry)
        wartung = registry['bgetem.medienshop.settings.IMedienportalSettings.wartung']
        if not wartung:
            wartung = False
        ret = {'wartung':wartung}
        payload = jsonlib2.write(ret)
        return payload
