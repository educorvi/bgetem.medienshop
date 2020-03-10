# -*- coding: utf-8 -*-
import re
from zope.interface import Interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    minlength_error = len(password) < 8

    maxlength_error = len(password) > 28

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    #symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not ( minlength_error or maxlength_error or digit_error or uppercase_error or lowercase_error )

    return {
        'password_ok' : password_ok,
        'minlength_error' : minlength_error,
        'maxlength_error' : maxlength_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
    }


class WeakPassword(schema.ValidationError):
    u""" Das eingegebene Passwort entspricht nicht den Richtlinien: (8-28 Zeichen, mind. eine Zahl, mind. ein Grossbuchstabe, 
        mind. ein Kleinbuchstabe. """


def validatePassword(value):
    if value:
        check = password_check(value)
        if not check.get('password_ok'):
            raise WeakPassword
    return True

class AuswahlAnrede(schema.ValidationError):
    u"""Bitte wählen Sie eine Anrede aus."""

def validateAnrede(value):
    if value not in [u'Herr', u'Frau']:
        raise AuswahlAnrede
    return True

class NotCheckedBox(schema.ValidationError):
    u""" Bitte bestätigen Sie Ihr Einverständnis."""

def validateCheckbox(value):
    if not value:
        raise NotCheckedBox
    return True

bgetemanrede = SimpleVocabulary((
    SimpleTerm(value=u'auswahl', token=u'auswahl', title=u'Bitte auswählen...'),
    SimpleTerm(value=u'Frau', token=u'Frau', title=u'Frau'),
    SimpleTerm(value=u'Herr', token=u'Herr', title=u'Herr'),
    ))

saplaender = SimpleVocabulary((
    SimpleTerm(value=u'AT', token=u'Oesterreich', title=u'Österreich'),
    SimpleTerm(value=u'BE', token=u'Belgien', title=u'Belgien'),
    SimpleTerm(value=u'BG', token=u'Bulgarien', title=u'Bulgarien'),
    SimpleTerm(value=u'BY', token=u'Weissrussland', title=u'Weissrussland'),
    SimpleTerm(value=u'CH', token=u'Schweiz', title=u'Schweiz'),
    SimpleTerm(value=u'DE', token=u'Deutschland', title=u'Deutschland'),
    SimpleTerm(value=u'DK', token=u'Daenemark', title=u'Dänemark'),
    SimpleTerm(value=u'EE', token=u'Estland' , title=u'Estland'),
    SimpleTerm(value=u'ES', token=u'Spanien', title=u'Spanien'),
    SimpleTerm(value=u'FI', token=u'Finnland', title=u'Finnland'),
    SimpleTerm(value=u'FR', token=u'Frankreich', title=u'Frankreich'),
    SimpleTerm(value=u'GR', token=u'Griechenland', title=u'Griechenland'),
    SimpleTerm(value=u'HU', token=u'Ungarn', title=u'Ungarn'),
    SimpleTerm(value=u'IE', token=u'Irland', title=u'Irland'),
    SimpleTerm(value=u'IT', token=u'Italien', title=u'Italien'),
    SimpleTerm(value=u'LU', token=u'Luxemburg', title=u'Luxemburg'),
    SimpleTerm(value=u'LV', token=u'Lettland', title=u'Lettland'),
    SimpleTerm(value=u'MT', token=u'Malta', title=u'Malta'),
    SimpleTerm(value=u'NL', token=u'Niederlande', title=u'Niederlande'),
    SimpleTerm(value=u'NO', token=u'Norwegen', title=u'Norwegen'),
    SimpleTerm(value=u'PL', token=u'Polen', title=u'Polen'),
    SimpleTerm(value=u'PT', token=u'Portugal', title=u'Portugal'),
    SimpleTerm(value=u'RO', token=u'Rumaenien', title=u'Rumänien'),
    SimpleTerm(value=u'RS', token=u'Serbien', title=u'Republik Serbien'),
    SimpleTerm(value=u'RU', token=u'Russische Foederation', title=u'Russische Föderation'),
    SimpleTerm(value=u'SE', token=u'Schweden', title=u'Schweden'),
    SimpleTerm(value=u'SI', token=u'Slowenien', title=u'Slowenien'),
    SimpleTerm(value=u'SK', token=u'Slowakei', title=u'Slowakei'),
    SimpleTerm(value=u'TR', token=u'Tuerkei', title=u'Türkei'),
    SimpleTerm(value=u'UA', token=u'Ukraine', title=u'Ukraine'),
    SimpleTerm(value=u'YU', token=u'Jugoslawien', title=u'Jugoslawien')
    ))

class IUser(Interface):
    anrede = schema.Choice(title=u"Anrede", source=bgetemanrede, constraint=validateAnrede)
    name1 = schema.TextLine(title=u"Firma/Vorname Name", description=u"(Maximal 40 Zeichen)")
    name2 = schema.TextLine(title=u"Abteilung/Ansprechpartner", description=u"(Maximal 40 Zeichen)", required=False)
    name3 = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    name4 = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    strasse = schema.TextLine(title=u"Strasse und Hausnummer")
    plz = schema.TextLine(title=u"Postleitzahl")
    meinort = schema.TextLine(title=u"Ort")
    land = schema.Choice(title=u"Land", source=saplaender, default=u"DE")

    versand = schema.Bool(title=u'Abweichende Versandanschrift',
                          description=u'Bitte klicken Sie hier für eine abweichende Versandanschrift',
                          required = False)

    anrede_v = schema.Choice(title=u"Anrede*", source=bgetemanrede, required=False)
    name1_v = schema.TextLine(title=u"Firma/Vorname Name*", description=u"(Maximal 40 Zeichen)", required=False)
    name2_v = schema.TextLine(title=u"Abteilung/Ansprechpartner", description=u"(Maximal 40 Zeichen)", required=False)
    name3_v = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    name4_v = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    strasse_v = schema.TextLine(title=u"Strasse und Hausnummer*", required=False)
    plz_v = schema.TextLine(title=u"Postleitzahl*", required=False)
    ort_v = schema.TextLine(title=u"Ort*", required=False)
    land_v = schema.Choice(title=u"Land*", source=saplaender, default=u"DE", required=False)

    email = schema.TextLine(title=u"E-Mail")
    telefon = schema.TextLine(title=u"Telefon", description=u"Bitte geben Sie uns Ihre Telefonnummer für evtl. Rückfragen.\
                              Format: +49 30 1234567 (Vorwahl ohne „0“, keine Sonderzeichen, max. 20 Zeichen)", required=False)
    #art = schema.TextLine(title=u"Art", default=u"R")
    mitnr = schema.TextLine(title=u"Mitgliedsnummer (8-stellig, ohne Betriebsstätten-Nr.)", required=False)
    passwort = schema.Password(title=u"Passwort", constraint=validatePassword)
    passwort2 = schema.Password(title=u"Passwort wiederholen")

    datenschutz = schema.Bool(title=u'Datenschutz',
                              constraint = validateCheckbox,
                              description=u'Ich bin einverstanden, dass meine Daten gespeichert und zum Zwecke der Abwicklung meiner Bestellungen\
                                            an den vertraglichen Versanddienstleister der BG ETEM weitergeleitet werden. Die Datenschutzerklärung\
                                            der BG ETEM habe ich gelesen.')

class INewPassword(Interface):

    email = schema.TextLine(title=u"E-Mail")
    passwort = schema.Password(title=u"Neues Passwort", constraint=validatePassword)
    passwort2 = schema.Password(title=u"Neues Passwort wiederholen")

class ICreateValidPw(Interface):

    passwort = schema.Password(title=u"Neues Passwort", constraint=validatePassword)
    passwort2 = schema.Password(title=u"Neues Passwort wiederholen")


class IChangeAnschrift(Interface):
    anrede = schema.Choice(title=u"Anrede", source=bgetemanrede, constraint=validateAnrede)
    name1 = schema.TextLine(title=u"Firma/Vorname und Name", description=u"(Maximal 40 Zeichen)")
    name2 = schema.TextLine(title=u"Abteilung/Ansprechpartner", description=u"(Maximal 40 Zeichen)", required=False)
    name3 = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    name4 = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    strasse = schema.TextLine(title=u"Strasse und Hausnummer")
    plz = schema.TextLine(title=u"Postleitzahl")
    meinort = schema.TextLine(title=u"Ort")
    land = schema.Choice(title=u"Land", source=saplaender, default=u"DE")

    anrede_v = schema.Choice(title=u"Anrede*", source=bgetemanrede, required=False)
    name1_v = schema.TextLine(title=u"Firma/Vorname Name*", description=u"(Maximal 40 Zeichen)", required=False)
    name2_v = schema.TextLine(title=u"Abteilung/Ansprechpartner", description=u"(Maximal 40 Zeichen)", required=False)
    name3_v = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    name4_v = schema.TextLine(title=u"ggfs. Fortsetzung", description=u"(Maximal 40 Zeichen)", required=False)
    strasse_v = schema.TextLine(title=u"Strasse und Hausnummer")
    plz_v = schema.TextLine(title=u"Postleitzahl")
    ort_v = schema.TextLine(title=u"Ort")
    land_v = schema.Choice(title=u"Land", source=saplaender, default=u"DE")
    telefon = schema.TextLine(title=u"Telefon", description=u"Bitte geben Sie uns Ihre Telefonnummer für evtl. Rückfragen", required=False)


class ILogin(Interface):

    email = schema.TextLine(title=u"E-Mail")
    passwort = schema.Password(title=u"Passwort")

class ISearchUser(Interface):

    email = schema.TextLine(title=u'E-Mail')

class IChangePassword(Interface):

    old_password = schema.Password(title=u'Ihr bisheriges Passwort')
    new_password = schema.Password(title=u'Ihr neues Passwort', constraint=validatePassword)
    new_password2 = schema.Password(title=u'Neues Passwort wiederholen', constraint=validatePassword)

class IForgotPassword(Interface):

    email = schema.TextLine(title=u'E-Mail')

class ICheckOrder(Interface):

    agb = schema.Bool(title=u"Allgemeine Geschäftsbedingungen (AGB), Datenschutz",
                      constraint = validateCheckbox,
                      description = u"Ich habe die AGB und die Datenschutzerklärung der BG ETEM gelesen und erkläre mein Einverständnis.\
                                    Ausdrücklich bin ich einverstanden, dass meine Daten gespeichert und zum Zwecke der Abwicklung meiner Bestellung\
                                    an den vertraglichen Versanddienstleister der BG ETEM weitergeleitet werden.")

class IDeleteUser(Interface):

    delok = schema.Bool(title=u"Löschen meiner Benutzerkennung.",
                        constraint = validateCheckbox,
                        description = u"Ich erkläre hiermit ausdrücklich, dass meine Benutzerkennung im Medienportal der BG ETEM gelöscht werden soll.\
                                      Wir senden Ihnen eine E-Mail zur Bestätigung und melden Sie vom Medienportal ab.")
