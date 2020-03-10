# -*- coding:utf-8 -*-
import re
import decimal
from zope.interface import Interface
from zope.schema import ValidationError
from uvc.api import api
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collective.beaker.interfaces import ISession
from bgetem.medienshop.userinterfaces import IUser, ILogin, ISearchUser, IChangePassword, IForgotPassword, IChangeAnschrift, ICheckOrder, INewPassword
from bgetem.medienshop.userinterfaces import IDeleteUser, ICreateValidPw
from bgetem.medienshop.persistance import getSessionData, setSessionData, delSessionData, saveMongoUser, getMongoUser
from bgetem.medienshop.persistance import saveMongoUserForDel, readMongoUserForDel 
from bgetem.medienshop.persistance import saveMongoUserForPwReset, readMongoUserForPwReset
from bgetem.medienshop.messages import createBodyMessage, createOrderMessage, createResetMessage, createDelMessage
from bgetem.medienshop.browser.card import getCartCookie, setCartCookie
from bgetem.medienshop.browser.artikelliste import formatMoney
from zeam.form.base import DictDataManager, Error
from sapshopapi import sapshopapi
from plone import api as ploneapi


api.templatedir('templates')


class AnredeValidator(object):

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields
        self.errors = []

    def validate(self, data):
        if not data.has_key('versand'):
            data['versand'] = True
        if not data.get('versand'):
            return self.errors
        if data.get('versand'):
            if not data.get('anrede_v') in [u'Herr', u'Frau']:
                self.errors.append(
                    Error(
                        u'Bitte wählen Sie eine Anrede aus.',
                        identifier="form.field.anrede_v",
                    ),
                )
        return self.errors


class VersandValidator(object):

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields
        self.errors = []

    def validate(self, data):
        if not data.has_key('versand'):
            data['versand'] = True
        if not data.get('versand'):
            return self.errors
        if data.get('versand') and data.get('name1_v') and data.get('strasse_v') and data.get('plz_v') and data.get('ort_v') and data.get('land_v'):
            return self.errors
        if not data.get('name1_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden oder deaktivieren Sie das Auswahlfeld "Abweichende Versandanschrift".',
                    identifier="form.field.name1_v",
                ),
            )
        if not data.get('strasse_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden oder deaktivieren Sie das Auswahlfeld "Abweichende Versandanschrift".',
                    identifier="form.field.strasse_v",
                ),
            )
        if not data.get('plz_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden oder deaktivieren Sie das Auswahlfeld "Abweichende Versandanschrift".',
                    identifier="form.field.plz_v",
                ),
            )
        if not data.get('ort_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden oder deaktivieren Sie das Auswahlfeld "Abweichende Versandanschrift".',
                    identifier="form.field.ort_v",
                ),
            )
        return self.errors


class ChangeVersandValidator(object):

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields
        self.errors = []

    def validate(self, data):
        if not data.has_key('versand'):
            data['versand'] = True
        if not data.get('versand'):
            return self.errors
        if data.get('versand') and data.get('name1_v') and data.get('strasse_v') and data.get('plz_v') and data.get('ort_v') and data.get('land_v'):
            return self.errors
        if not data.get('name1_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden. Bei gleicher Rechnungs- und Versandanschrift übernehmen Sie bitte die Daten der Rechnungsadresse.',
                    identifier="form.field.name1_v",
                ),
            )
        if not data.get('strasse_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden. Bei gleicher Rechnungs- und Versandanschrift übernehmen Sie bitte die Daten der Rechnungsadresse.',
                    identifier="form.field.strasse_v",
                ),
            )
        if not data.get('plz_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden. Bei gleicher Rechnungs- und Versandanschrift übernehmen Sie bitte die Daten der Rechnungsadresse.',
                    identifier="form.field.plz_v",
                ),
            )
        if not data.get('ort_v'):
            self.errors.append(
                Error(
                    'Dieses Feld muss ausgefüllt werden. Bei gleicher Rechnungs- und Versandanschrift übernehmen Sie bitte die Daten der Rechnungsadresse.',
                    identifier="form.field.ort_v",
                ),
            )
        return self.errors


class SamePasswordValidator(object):

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields
        self.errors = []

    def validate(self, data):
        if data.get('passwort') == data.get('passwort2'):
            return self.errors
        self.errors.append(
            Error(
                u'Die eingegebenen Passwörter stimmen nicht überein.',
                identifier="form.field.passwort",
            ),
        )
        return self.errors

class NewSamePasswordValidator(object):

    def __init__(self, form, fields):
        self.form = form
        self.fields = fields
        self.errors = []

    def validate(self, data):
        if data.get('new_password') == data.get('new_password2'):
            return self.errors
        self.errors.append(
            Error(
                u'Die eingegebenen Passwörter stimmen nicht überein.',
                identifier="form.field.new_password",
            ),
        )
        return self.errors


def formatdata(data):
    mongodata = {}
    itemlist = []
    for i in data.item:
        item = {}
        item['ANRED']=i.ANRED.encode('utf-8')
        item['NAME1']=i.NAME1.encode('utf-8')
        if i.NAME2:
            item['NAME2']=i.NAME2.encode('utf-8')
        else:
            item['NAME2'] = u''
        if i.NAME3:
            item['NAME3']=i.NAME3.encode('utf-8')
        else:
            item['NAME3']=u''
        if i.NAME4:
            item['NAME4']=i.NAME4.encode('utf-8')
        else:
            item['NAME4']=u''
        item['STRAS']=i.STRAS.encode('utf-8')
        item['PSTLZ']=i.PSTLZ.encode('utf-8')
        item['ORT01']=i.ORT01.encode('utf-8')
        item['LAND1']=i.LAND1.encode('utf-8')
        if i.TELF1:
            item['TELF1']=i.TELF1.encode('utf-8')
        else:
            item['TELF1']=u''
        if i.MITNR:
            item['MITNR']=i.MITNR.encode('utf-8')
        else:
            item['MITNR']=u''
        item['ART']=i.ART.encode('utf-8')
        item['VERIF'] = False
        if i.VERIF:
            item['VERIF'] = True
        itemlist.append(item)
    mongodata['item'] = itemlist
    return mongodata

def changeformdata(userdata):
    adresse = userdata.get('item')[0]
    versand = userdata.get('item')[1]

    formdata = {}
    formdata['anrede'] = adresse.get('ANRED')
    formdata['name1'] = adresse.get('NAME1')
    formdata['name2'] = adresse.get('NAME2')
    formdata['name3'] = adresse.get('NAME3')
    formdata['name4'] = adresse.get('NAME4')
    formdata['strasse'] = adresse.get('STRAS')
    formdata['plz'] = adresse.get('PSTLZ')
    formdata['meinort'] = adresse.get('ORT01')
    formdata['land'] = adresse.get('LAND1')
    formdata['telefon'] = adresse.get('TELF1')
    formdata['anrede_v'] = versand.get('ANRED')
    formdata['name1_v'] = versand.get('NAME1')
    formdata['name2_v'] = versand.get('NAME2')
    formdata['name3_v'] = versand.get('NAME3')
    formdata['name4_v'] = versand.get('NAME4')
    formdata['strasse_v'] = versand.get('STRAS')
    formdata['plz_v'] = versand.get('PSTLZ')
    formdata['ort_v'] = versand.get('ORT01')
    formdata['land_v'] = versand.get('LAND1')
    return formdata

class CreateUser(api.Form):
    api.context(Interface)
    fields = api.Fields(IUser)
    fields['name1'].htmlAttributes['maxlength'] = 40
    fields['name2'].htmlAttributes['maxlength'] = 40
    fields['name3'].htmlAttributes['maxlength'] = 40
    fields['name4'].htmlAttributes['maxlength'] = 40
    fields['strasse'].htmlAttributes['maxlength'] = 35
    fields['plz'].htmlAttributes['maxlength'] = 10
    fields['mitnr'].htmlAttributes['maxlength'] = 8
    fields['telefon'].htmlAttributes['maxlength'] = 20
    fields['meinort'].htmlAttributes['maxlength'] = 25
    fields['name1_v'].htmlAttributes['maxlength'] = 40
    fields['name2_v'].htmlAttributes['maxlength'] = 40
    fields['name3_v'].htmlAttributes['maxlength'] = 40
    fields['name4_v'].htmlAttributes['maxlength'] = 40
    fields['strasse_v'].htmlAttributes['maxlength'] = 35
    fields['plz_v'].htmlAttributes['maxlength'] = 10
    fields['ort_v'].htmlAttributes['maxlength'] = 25

    dataValidators = [SamePasswordValidator, VersandValidator, AnredeValidator]

    def update(self):
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/createuser'

    @api.action('Speichern')
    def create_user(self):
        data, errors = self.extractData()
        if errors:
            message = u'Bitte beachten Sie die angezeigen Fehler'
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return
        data['ort'] = data.pop('meinort')
        url = ploneapi.portal.get().absolute_url() + '/medienportal'

        sapapi = sapshopapi.getAPI()
        userdata = sapapi.getUser(data.get('email'))

        if userdata:
            message = u'Leider ist bei der Registrierung ein Fehler aufgetreten: Die eingegebene E-Mail-Adresse ist bereits\
                        bei uns registriert. Falls Sie Ihr Passwort vergessen haben, verwenden Sie bitte die Funktion "Passwort vergessen".'
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)

        try:
            validkey = saveMongoUser(data)
            ploneapi.portal.send_email(
                recipient=data.get('email'),
                sender=u"medien@bgetem.de",
                subject=u"Ihre Registrierung für das Medienportal der BG ETEM.",
                body=createBodyMessage(data, validkey),
            )
        except:
            message = u'Leider ist beim Anlegen Ihres Benutzerkontos ein Fehler aufgetreten. Bitte versuchen Sie es zu\
                        einem späteren Zeitpunkt noch einmal'
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)
        message = u'Wir haben Ihnen soeben eine Nachricht zur Bestätigung Ihrer E-Mail-Adresse gesendet. Bitte prüfen Sie\
                    ihr E-Mail-Postfach. Ihr Benutzerkonto kann erst aktiviert werden, wenn Sie auf den in der E-Mail\
                    enthaltenen Link klicken. Wir bitten um Ihr Verständnis, dass es gelegentlich beim Versand der Bestätigungsmail\
                    prozessbedingt zu Verzögerungen von bis zu einer Stunde kommen kann.'
        ploneapi.portal.show_message(message=message, request=self.request, type='info')
        return self.response.redirect(url)

    @api.action('Abbrechen')
    def cancel_user(self):
         url = ploneapi.portal.get().absolute_url() + '/medienportal'
         return self.response.redirect(url)


class ValidUser(api.Page):
    api.context(Interface)

    def render(self):
        key = self.request.get('code')
        if not key:
            return u"<h2>Unberechtigter Zugriff</h2><p>Sie sind nicht für den Aufruf dieser Seite berechtigt.</p>"
        data = getMongoUser(key)
        if not data:
            return u"<h2>Fehler</h2><p>Beim Lesen Ihrer Daten ist ein Fehler aufgetreten, bitte versuchen Sie es zu einem späteren Zeitpunkt erneut.</p>"
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.addUser(**data)
        if retcode.EX_RETURN == 0:
            mongodata = formatdata(sapapi.getUser(data.get('email')))
            mongodata['email'] = data.get('email')
            key = setSessionData(self.request, mongodata)
            url = self.context.absolute_url() + '/changeanschrift'
            return self.response.redirect(url)
        return u"<h2>Fehler</h2><p>Beim Anlegen Ihres Benutzerkontos ist ein Fehler aufgetreten, bitte versuchen Sie es zu einem späteren Zeitpunkt erneut.(%s)</p>" % retcode.EX_MESSAGE


class LoginForm(api.Form):
    api.context(Interface)
    fields = api.Fields(ILogin)


    def update(self):
        self.registerurl = ploneapi.portal.get().absolute_url() + '/medienportal/createuser'
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/loginform'
        #Redirect if user is already logged in
        if getSessionData(self.request):
            if getSessionData(self.request).get('email'):
                url = ploneapi.portal.get().absolute_url() + '/medienportal/changeanschrift'
                return self.response.redirect(url)

    @api.action('Anmelden')
    def get_user(self):
        data, errors = self.extractData()
        if errors:
            return
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.getPassword(data.get('email'), data.get('passwort'))
        if retcode:
            mongodata = formatdata(sapapi.getUser(data.get('email')))
            mongodata['email'] = data.get('email')
            #mongodata['passwort'] = data.get('passwort')
            key = setSessionData(self.request, mongodata)
            url = self.context.absolute_url() + '/changeanschrift'
            return self.response.redirect(url)
        message = u'Benutzername oder Kennwort falsch'
        ploneapi.portal.show_message(message=message, request=self.request, type='error')
        return

    @api.action('Passwort vergessen')
    def go_passwort(self):
        url = self.context.absolute_url() + '/resetpassword'
        return self.response.redirect(url)

class UserLogout(api.View):
    api.context(Interface)

    def update(self):
        cookie = {}
        key = setSessionData(self.request, cookie)

    def render(self):
        message = u'Sie wurden erfolgreich vom Medienportal der BG ETEM abgemeldet.'
        url = ploneapi.portal.get().absolute_url() + '/medienportal'
        ploneapi.portal.show_message(message=message, request=self.request, type='info')
        return self.response.redirect(url)


class ChangeAnschrift(api.Form):
    api.context(Interface)
    fields = api.Fields(IChangeAnschrift)

    ignoreContent = False

    dataValidators = [ChangeVersandValidator, AnredeValidator]

    def update(self):
        if not hasattr(self, 'collapse'):
            self.collapse = "panel-collapse collapse"
        self.userdata = getSessionData(self.request)
        formdata = changeformdata(self.userdata)
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/changeanschrift'
        self.homeurl = ploneapi.portal.get().absolute_url() + '/medienportal'
        self.weiterurl = ploneapi.portal.get().absolute_url() + '/medienportal/checkorder'
        self.card = getCartCookie(self.request)

        self.setContentData(
            DictDataManager(formdata))

    @api.action(u'Kontaktdaten ändern')
    def change_anschrift(self):
        data, errors = self.extractData()
        if errors:
            message = u'Bitte beachten Sie die angezeigen Fehler'
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            self.collapse = "panel-collapse collapse in"
            return
        data['ort'] = data.pop('meinort')
        data['email'] = self.userdata.get('email')
        data['mitnr'] = self.userdata.get('item')[0].get('MITNR')
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.updateUser(**data)
        if retcode.EX_RETURN == 0:
            mongodata = formatdata(sapapi.getUser(data.get('email')))
            mongodata['email'] = data.get('email')
            key = setSessionData(self.request, mongodata)
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Ihre Adressdaten wurden erfolgreich geändert.'
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
            return self.response.redirect(url)
        else:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Fehler beim Ändern Ihrer Adressdaten (%s)' % retcode.EX_MESSAGE
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
            return self.response.redirect(url)


class ChangePassword(api.Form):
    api.context(Interface)
    fields = api.Fields(IChangePassword)

    dataValidators = [NewSamePasswordValidator]

    def update(self):
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/changepassword'

    @api.action(u'Passwort ändern')
    def change_pw(self):
        data, errors = self.extractData()
        if errors:
            return
        del data['new_password2']
        data['email'] = getSessionData(self.request).get('email', '')
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.updatePassword(**data)
        if retcode.EX_RETURN == 0:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Ihr Passwort wurde erfolgreich geändert.'
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
            return self.response.redirect(url)
        else:
            url = ploneapi.portal.get().absolute_url() + '/medienportal/changepassword'
            message = u'Fehler beim Ändern Ihres Passwortes. (%s)' % retcode.EX_MESSAGE
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)


class ResetPassword(api.Form):
    api.context(Interface)
    fields = api.Fields(IForgotPassword)

    def update(self):
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/resetpassword'

    @api.action(u'Passwort zurücksetzen')
    def reset_pw(self):
        data, errors = self.extractData()
        if errors:
            return
        usermail = data.get('email')
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.resetPassword(usermail)
        if retcode.EX_RETURN == 0:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            if True:
                code = retcode.EX_PASSKEY
                validkey = saveMongoUserForPwReset(usermail, code)
                ploneapi.portal.send_email(
                    recipient=usermail,
                    sender=u"medien@bgetem.de",
                    subject=u"Zurücksetzen des Passworts auf bgetem.de",
                    body=createResetMessage(validkey),
                )

                message = u'Wir haben Ihnen eine E-Mail geschickt. Bitte prüfen Sie Ihr E-Mail-Postfach.'
                ploneapi.portal.show_message(message=message, request=self.request, type='info')
                return self.response.redirect(url)
            else:
                message = u'Leider ist beim Zurücksetzen Ihres Passwortes ein Fehler aufgetreten. Bitte versuchen Sie es zu\
                            einem späteren Zeitpunkt noch einmal.'
                ploneapi.portal.show_message(message=message, request=self.request, type='error')
                return self.response.redirect(url)

        else:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Fehler beim Zurücksetzen Ihres Passwortes. (%s)' % retcode.EX_MESSAGE
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)


class CreateValidPw(api.Form):
    api.context(Interface)
    fields = api.Fields(ICreateValidPw)

    dataValidators = [SamePasswordValidator]

    def update(self):
        self.url = ploneapi.portal.get().absolute_url() + '/medienportal'
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/createvalidpw'
        if self.request.get('code'):
            setSessionData(self.request, {'resetkey':self.request.get('code')})

    @api.action(u'Neues Passwort speichern')
    def change_pw(self):
        data, errors = self.extractData()
        if errors:
            return
        mycookie = getSessionData(self.request)
        resetkey = mycookie.get('resetkey')
        mongodata = readMongoUserForPwReset(resetkey)
        if not mongodata:
            message = u"Fehler beim Lesen Ihrer Daten! Bitte versuchen Sie es zu einem späteren Zeitpunkt erneut."
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)
        newdata = {}
        newdata['email'] = mongodata.get('email')
        newdata['old_password'] = mongodata.get('pwcode')
        newdata['new_password'] = data.get('passwort')
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.updatePassword(**newdata)
        if retcode.EX_RETURN == 0:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Ihr Passwort wurde erfolgreich gespeichert. Sie können sich nun mit dem neuen Passwort anmelden.'
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
            return self.response.redirect(url)
        else:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Fehler beim Speichern Ihres Passwortes. (%s)' % retcode.EX_MESSAGE
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)

class NewPassword(api.Form):
    api.context(Interface)
    fields = api.Fields(INewPassword)

    dataValidators = [SamePasswordValidator]

    def update(self):
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/newpassword'
        self.oldpw = self.request.get('code')

    @api.action(u'Neues Passwort speichern')
    def change_pw(self):
        data, errors = self.extractData()
        if errors:
            return
        newdata = {}
        newdata['email'] = data.get('email')
        newdata['old_password'] = self.oldpw
        newdata['new_password'] = data.get('passwort')
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.updatePassword(**newdata)
        if retcode.EX_RETURN == 0:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Ihr Passwort wurde erfolgreich gespeichert. Sie können sich nun mit dem neuen Passwort anmelden.'
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
            return self.response.redirect(url)
        else:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Fehler beim Speichern Ihres Passwortes. (%s)' % retcode.EX_MESSAGE
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)

 
class GetUser(api.Form):
     api.context(Interface)
     fields = api.Fields(ISearchUser)

     @api.action('Suchen')
     def search_user(self):
         data,errors = self.extractData()
         if errors:
             return
         sapapi = sapshopapi.getAPI()
         if '@' in data.get('email'):
             print 'SAP-Daten'
             userdata = sapapi.getUser(data.get('email'))
         else:
             print 'Mongo-Daten'
             userdata = getMongoUser(data.get('email'))
         print userdata

class CheckOrder(api.Form):
    api.context(Interface)
    fields = api.Fields(ICheckOrder)

    def update(self):
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/checkorder'
        self.userdata = getSessionData(self.request)
        self.verif = False
        if self.userdata.get('item')[0].get('MITNR'):
            self.verif = self.userdata.get('item')[0].get('VERIF')
        self.mnr = self.userdata.get('item')[0].get('MITNR')
        checker = self.checkBestand()
        if not checker:
            message = u'Bei Ihrer Bestellung ist leider ein Fehler aufgetreten. Bitte beachten Sie die aktualisierten Mengen bei den rot markierten\
                        Artikeln.'
            ploneapi.portal.show_message(message=message, request=self.request, type='error')

    def checkBestand(self):
        check = True
        carddata = getCartCookie(self.request)
        self.artlist = []
        self.gesamt = decimal.Decimal(0.0)
        self.gesamt_mem = decimal.Decimal(0.0)
        for i in carddata:
            art = {}
            artikel = ploneapi.content.find(UID = i)[0].getObject()
            artikel._v_article = None
            art['style'] = 'color:black;'
            if artikel.bestand < int(carddata[i].get('menge')):
                check = False
                orderdata = carddata[i]
                orderdata['menge'] = int(artikel.bestand)
                carddata[i] = orderdata
                art['style'] = 'color:red;'
            art['menge'] = carddata[i].get('menge')
            art['matnr'] = carddata[i].get('bestellung')
            art['titel'] = carddata[i].get('artikel')
            art['preis'] = formatMoney(decimal.Decimal(art['menge']) * artikel.preis)
            self.gesamt += decimal.Decimal(art['menge']) * artikel.preis
            if art['menge'] <= artikel.freimenge:
                self.gesamt_mem = self.gesamt_mem
                art['preis_mem'] = formatMoney(decimal.Decimal(0.0))
            else:
                self.gesamt_mem = (decimal.Decimal(art['menge']) - artikel.freimenge) * artikel.preis_mem
                art['preis_mem'] = formatMoney((decimal.Decimal(art['menge']) - artikel.freimenge) * artikel.preis_mem)
            self.artlist.append(art)
        self.gesamt += decimal.Decimal(3.5)
        self.gesamt = formatMoney(self.gesamt)
        self.gesamt_mem = formatMoney(self.gesamt_mem)
        if check == False:
            card = setCartCookie(carddata, self.request)
        return check

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

    @api.action('Verbindlich bestellen')
    def order(self):
        data,errors = self.extractData()
        if self.verif and len(errors) == 2:
            errors = None
        if errors:
            return
        sapapi = sapshopapi.getAPI()
        checker = self.checkBestand()
        if not checker:
            url = ploneapi.portal.get().absolute_url() + '/checkorder'
            message = u'Bei Ihrer Bestellung ist leider ein Fehler aufgetreten. Bitte beachten Sie die aktualisierten Mengen bei den rot markierten\
                        Artikeln.'
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return
        bestellung = sapapi.createOrder(self.userdata.get('email'), self.artlist)
        if bestellung.EX_RETURN == 0:
            self.bestellnummer = bestellung.EX_VBELN
            self.userdata['bestellnummer'] = self.bestellnummer
            key = setSessionData(self.request, self.userdata)

            mime_msg = MIMEMultipart('related')
            mime_msg['Subject'] = u"Ihre Bestellung auf bgetem.de"
            mime_msg['From'] = u"medien@bgetem.de"
            mime_msg['To'] = self.userdata.get('email')
            mime_msg.preamble = 'This is a multi-part message in MIME format.'
            msgAlternative = MIMEMultipart('alternative')
            mime_msg.attach(msgAlternative)

            htmltext = createOrderMessage(self.userdata, self.verif, self.mnr, self.artlist, self.gesamt_mem, self.gesamt, self.bestellnummer)
            msg_txt = MIMEText(htmltext, _subtype='html', 
                   _charset='utf-8')
            msgAlternative.attach(msg_txt)
            mail_host = ploneapi.portal.get_tool(name='MailHost')
            mail_host.send(mime_msg.as_string())

            #message = u'Vielen Dank, Ihre Bestellung ist bei uns eingegangen. Sie erhalten eine Bestätigung per E-Mail.'
            #ploneapi.portal.show_message(message=message, request=self.request, type='info')
            try:
                carddata = getCartCookie(self.request)
                for i in carddata:
                    artikel = ploneapi.content.find(UID = i)[0].getObject()
                    artikel._v_article = None
                session = ISession(self.request)
                del session['cart']
                session.save()
            except:
                print u'Problem beim Delete Session' 
            url = ploneapi.portal.get().absolute_url() + '/medienportal/orderconfirm'
            return self.response.redirect(url)

        else:
            message = u'Bei Ihrer Bestellung ist leider ein Fehler aufgetreten. Bitte versuchen Sie es später noch einmal. (%s)' % bestellung.EX_MESSAGE
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(self.formurl)

class OrderConfirm(api.View):
    api.context(Interface)

    def update(self):
        userdata = getSessionData(self.request)
        self.bestellnummer = userdata.get('bestellnummer')


class DeleteUserForm(api.Form):
    api.context(Interface)
    fields = api.Fields(IDeleteUser)

    def update(self):
        self.formurl = ploneapi.portal.get().absolute_url() + '/medienportal/deleteuserform'

    @api.action(u'Auftrag absenden')
    def del_user(self):
        data, errors = self.extractData()
        if errors:
            return
        email = getSessionData(self.request).get('email', '')
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.deleteUser(email)
        if retcode.EX_RETURN == 0:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            if True:
                code = retcode.EX_DELCODE
                validkey = saveMongoUserForDel(email, code)
                msgbody = createDelMessage(data, validkey)
                ploneapi.portal.send_email(
                    recipient=email,
                    sender=u"medien@bgetem.de",
                    subject=u"Ihre Auftrag zur Löschung eines Benutzers aus dem Medienportal der BG ETEM.",
                    body=msgbody,
                )
            else:
                message = u'Leider ist beim Auftrag zur Löschung Ihres Benutzerkontos ein Fehler aufgetreten. Bitte versuchen Sie es zu\
                            einem späteren Zeitpunkt noch einmal'
                ploneapi.portal.show_message(message=message, request=self.request, type='error')
                return self.response.redirect(url)
            cookie = {}
            key = setSessionData(self.request, cookie) 
            message = u'Wir haben Ihnen soeben eine Nachricht zur Bestätigung Ihrer E-Mail-Adresse gesendet. Bitte prüfen Sie\
                      ihr E-Mail-Postfach. Ihr Benutzerkonto kann erst gelöscht werden, wenn Sie auf den in der E-Mail\
                      enthaltenen Link klicken. Wir bitten um Ihr Verständnis, dass es gelegentlich beim Versand der Bestätigungsmail\
                      prozessbedingt zu Verzögerungen von bis zu einer Stunde kommen kann.'
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
            return self.response.redirect(url)

    @api.action('Abbrechen')
    def cancel_user(self):
         url = ploneapi.portal.get().absolute_url() + '/medienportal'
         return self.response.redirect(url)

class DelVerifyUser(api.Page):
    api.context(Interface)

    def render(self):
        key = self.request.get('code')
        if not key:
            return u"<h2>Unberechtigter Zugriff</h2><p>Sie sind nicht für den Aufruf dieser Seite berechtigt.</p>"
        data = readMongoUserForDel(key)
        if not data:
            return u"<h2>Fehler</h2><p>Beim Lesen Ihrer Daten ist ein Fehler aufgetreten, bitte versuchen Sie es zu einem späteren Zeitpunkt erneut.</p>"
        sapapi = sapshopapi.getAPI()
        retcode = sapapi.deleteUserVerify(**data)
        if retcode.EX_RETURN == 0:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            cookie = {}
            key = setSessionData(self.request, cookie)
            message = u"Wir haben in Ihrem Auftrag die Löschung Ihres Benutzerkontos erfolgreich ausgeführt."
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
            return self.response.redirect(url)
        else:
            url = ploneapi.portal.get().absolute_url() + '/medienportal'
            message = u'Bei der Löschung des Benutzerkontos ist ein Fehler aufgetreten. (%s)' % retcode.EX_MESSAGE
            ploneapi.portal.show_message(message=message, request=self.request, type='error')
            return self.response.redirect(url)
