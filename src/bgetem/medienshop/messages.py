# -*- coding:utf-8 -*-
#Alles Nachrichten fuer die E-Mails
from datetime import datetime

def createBodyMessage(data, validkey):
    message=u"""\
Vielen Dank für Ihre Registrierung im Medienportal der BG ETEM. 

Für Sie wurde folgender Registrierungscode erzeugt:
 
https://medien.bgetem.de/validuser?code=%s
 
Bitte klicken Sie auf den Link, um die Registrierung abzuschließen.
 
Sofern Sie keine Registrierung beantragt haben, ignorieren Sie bitte diese E-Mail.
 
Freundliche Grüße
Ihre BG ETEM

https://medien.bgetem.de""" % validkey
    return message

def createDelMessage(data, validkey):
    message=u"""\
Wir haben Ihren Auftrag zur Löschung Ihrer Benutzerkennung erhalten.

Für diesen Auftrag wurde folgender Bestätigungscode erzeugt:
 
https://medien.bgetem.de/delverifyuser?code=%s
 
Bitte klicken Sie auf den Link, um die Löschung Ihres Kontos abzuschließen.
 
Sofern Sie keine Löschung des Benutzerkontos beantragt haben, ignorieren Sie bitte diese E-Mail.
 
Freundliche Grüße
Ihre BG ETEM

https://medien.bgetem.de""" % validkey
    return message


def createHTMLTable(verif, mnr, gesamt_mem, gesamt, artlist):
    message = u"<h3>Ihre Bestellung</h3>"
    if verif:
        message = "<h3>Ihre Bestellung für Mitgliedsnummer: %s</h3>" %mnr
    
    message += u"<table><thead><th>Artikel</th><th>Preis</th></thead><tbody>"
    for i in artlist:
        if verif:
            message += u'<tr><td>%s x %s (%s)</td><td align="right">%s €</td></tr>' %(i['menge'], i['titel'], i['matnr'], i['preis_mem'])
        else:
            message += u'<tr><td>%s x %s (%s)</td><td align="right">%s €</td></tr>' %(i['menge'], i['titel'], i['matnr'], i['preis'])
    if verif:
        message += u'<tr><td>Versandkosten</td><td align="right">0,00 €</td></tr>'
    else:
        message += u'<tr><td>Versandkosten</td><td align="right">3,50 €</td></tr>'
    if verif and gesamt_mem == "0,00":
        message += u'<tr><td><b>Summe Gesamt </b>(Bestellung innerhalb der Freimengen)</td><td align="right">%s €</td></tr>' % gesamt_mem
    elif verif and gesamt_mem != "0,00":
        message += u'<tr><td><b>Summe Gesamt </b></td><td align="right">%s €</td></tr>' % gesamt_mem
    else:
        message += u'<tr><td><b>Summe Gesamt </b></td><td align="right">%s €</td></tr>' % gesamt
    message += "</tbody></table>"
    return message

def createOrderMessage(userdata, verif, mnr, artlist, gesamt_mem, gesamt,  bestellnummer):
    items = userdata.get('item')
    rechnung = items[0]
    versand = items[1]
    ehrung = u'geehrter'
    if rechnung.get('ANRED') == u'Frau':
        ehrung = u'geehrte'
    datum = datetime.now().strftime('%d.%m.%Y')
    message=u"""\
<!DOCTYPE html>
<html>
<body>
<p>Vielen Dank für Ihren Auftrag auf bgetem.de.</p>
<p>Ihre Auftragsnummer: %s<br/>
Auftragsdatum: %s</p>
<p>Ihr Auftrag wird schnellstmöglich bearbeitet und an die von Ihnen angegebene Adresse versandt.</p>
%s 
<p>Freundliche Grüße<br/>
Ihre BG ETEM</p>
<p>https://medien.bgetem.de</p>
<p><b>Hinweis für Erstbesteller:</b><br/>
Wir müssen zunächst Ihre Angaben zur Mitgliedschaft bei der BG ETEM prüfen, da diese relevant sind für die korrekte Preiskalkulation.
Sollten sich hier Fragen ergeben, werden wir Kontakt mit Ihnen aufnehmen. Der Versand Ihrer Bestellung erfolgt erst nach erfolgreicher Prüfung.
Wir bitten um Ihr Verständnis.</p>
<h3>Ihre Rechnungsadresse:</h3>
<p>%s<br/>
%s %s<br/>
%s %s<br/>
%s<br/>
%s %s</p>
<h3>Ihre Lieferadresse:</h3>
<p>%s<br/>
%s %s<br/>
%s %s<br/>
%s<br/>
%s %s</p>
<p>Die Rechnung liegt der Lieferung bei.</p>
<p>Unsere Allgemeinen Geschäftsbedingungen (AGB) finden Sie unter:<br/>
https://www.bgetem.de/die-bgetem/impressum/medienportal-agb</p>
<p>Unsere Datenschutzerklärung finden Sie unter:<br/>
https://www.bgetem.de/die-bgetem/datenschutz</p>
<p>Sie haben Fragen zu Ihrem Auftrag? Bitte schreiben Sie eine E-Mail an versand@bgetem.de oder rufen Sie uns an unter 0221/3778-1020.</p>
</body>
</html>
""" % (bestellnummer,
       datum,
       createHTMLTable(verif, mnr, gesamt_mem, gesamt, artlist),
       rechnung.get('ANRED'),
       rechnung.get('NAME1'),
       rechnung.get('NAME2'),
       rechnung.get('NAME3'),
       rechnung.get('NAME4'),
       rechnung.get('STRAS'),
       rechnung.get('PSTLZ'),
       rechnung.get('ORT01'),
       versand.get('ANRED'),
       versand.get('NAME1'),
       versand.get('NAME2'),
       versand.get('NAME3'),
       versand .get('NAME4'),
       versand.get('STRAS'),
       versand.get('PSTLZ'),
       versand.get('ORT01'))

    return message.encode('utf-8')


def createResetMessage(passkey):
    url = 'https://medien.bgetem.de/createvalidpw?code=%s' % passkey
    message=u"""\
Vielen Dank für Ihren Auftrag auf bgetem.de. Sie möchten Ihr Passwort zurücksetzen. Bitte klicken Sie auf den Link, um sich ein neues Passwort
zu vergeben: 

%s

Sofern Sie die Zurücksetzung Ihres Passworts nicht beantragt haben, ignorieren Sie bitte diese E-Mail.
 
Freundliche Grüße
Ihre BG ETEM

https://medien.bgetem.de""" % url
    return message
