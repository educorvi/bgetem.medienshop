# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2017 NovaReto GmbH
# # cklinger@novareto.de
#
import sys
import click
import base64
import logging
import transaction
import random

from plone import api
from DateTime import DateTime
from zope.component.hooks import setSite
from sapshopapi.sapshopapi import getAllItems, getArticle
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
server = smtplib.SMTP('10.4.27.27', 25)


logger = logging.getLogger("Plone")


def save_id(matnr):
    try:
        return base64.b64encode(unicode(matnr).encode('utf-8')).replace('=','-')
    except:
        import pdb; pdb.set_trace() 


@click.command()
@click.option('--shoppath', prompt='Path to Shop Instance')
def run(shoppath):
    work(app, shoppath)


def webcodehandler():
        """ Diese Methode wird immer dann aufgerufen wenn ein Dokument einen neuen Webcode erhalten soll.
            Mit der Methode soll eine 8-stellige, moeglichst eindeutige Zahl gebildet werden. Das
            soll durch folgende Methode erreicht werden:
            * Verkettung 2-stellige Jahreszahl(Konstante) + 6-stellige Zufallszahl
            * Catalogabfrage, ob im betr. Jahr ein Objekt mit dieser Kombination vorhanden ist, wenn ja:
            * wiederholter Aufruf des Zusfallszahlengenerators
        """
        #Bildung des Webcodes
        aktuell=str(DateTime()).split(' ')[0]
        neujahr='%s/01/01' %str(DateTime()).split(' ')[0][:4]
        konstante=str(aktuell[2:4])
        zufallszahl=str(random.randint(100000, 999999))
        code=konstante+zufallszahl
        #Sicherheitsabfrage
        results =  api.content.find(Webcode=code)
        while results:
            zufallszahl=str(random.randint(100000, 999999))
            code=konstante+zufallszahl
            results =  api.content.find(Webcode=code)
        return u'M%s' %unicode(code)

def work(app, shoppath):
    plone_root = app.unrestrictedTraverse(str(shoppath.split('/')[0]))
    setSite(plone_root)
    shop = app.unrestrictedTraverse(str(shoppath))
    SAPArticles = getAllItems()
    # ADDING
    mailbody = u"""\
<!DOCTYPE html>
<html>
        <body>
          <h1>Neue Artikel</h1>
            <ul>"""
    print "ADDING OBJECTS"
    newarts = False
    with click.progressbar(SAPArticles) as IteratorSAPArticles:
        for item in IteratorSAPArticles:
            if save_id(item.matnr) not in shop:
                newarts = True
                artikel = getArticle(item.matnr)
                logger.info('ADD SOMETHING TO SHOP')
                shop_item = api.content.create(
                        type="Artikel",
                        title=artikel.title,
                        description=item.description,
                        artikelnummer=item.matnr,
                        id=save_id(item.matnr),
                        webcode=webcodehandler(),
                        container=shop
                    )
                shop_item.medienart = artikel.medienart
                #api.content.transition(obj=shop_item, transition='publish')
                mailbody += u"<li>%s</li>" %artikel.title
                print artikel.title
                transaction.commit()
    mailbody += u"</ul>"
    if not newarts:
        mailbody += u"<p>Es wurden keine neuen Artikel hinzugefügt."
    # DELETE
    mailbody += u"""<h1>Artikel auf Status privat</h1>
                      <ul>"""
    shopset = set(shop.keys())
    sapset = set([save_id(x.matnr) for x in SAPArticles])
    print "DELETEING OBJECTS"
    delarts = False
    with click.progressbar(shopset.difference(sapset)) as delitems:
        for matnr in delitems:
            artpath = '/portal/medienportal/artikel/%s' %matnr
            artikel = api.content.get(path=artpath)
            if artikel:
                titel = artikel.title
                url = artikel.absolute_url().replace('http://nohost/portal', 'https://medien.bgetem.de')
                review_state = api.content.get_state(obj=artikel)
                if review_state != 'private':
                    delarts = True
                    #api.content.delete(shop[matnr])
                    api.content.transition(shop[matnr], transition='reject')
                    mailbody += u'<li><a href="%s">%s</a> (ID: %s)</li>' %(url, titel, matnr)
                    print 'Artikel soll geloescht werden: %s' %matnr
                    transaction.commit()
    mailbody += u"</ul>"                
    if not delarts:
        mailbody += u"<p>Es wurden keine vorhandenen Artikel auf den Status privat gesetzt.</p>"
    mailbody += u"</body></html>"
    fromaddr = "internet@bgetem.de"
    toaddr = "medien@bgetem.de"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Update Medienportal"
    body = mailbody
    msg.attach(MIMEText(body.encode('utf-8'), 'html', 'utf-8'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

if "app" in locals():
    oldargv = sys.argv
    sys.argv = sys.argv[0:1] + sys.argv[3:]
    run()
