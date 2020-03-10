# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2017 NovaReto GmbH
# # cklinger@novareto.de
#
import sys
import click
import base64
import logging
import transaction
import requests

from plone import api
from zope.component.hooks import setSite
from sapshopapi.sapshopapi import getAllItems, getArticle
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
server = smtplib.SMTP('10.4.27.27', 25)


logger = logging.getLogger("Plone")


@click.command()
def run():
    work(app)


def work(app):
    result = requests.get('http://localhost:8081/portal/medienportal')
    if result:
        if result.status_code == 200:
            print 'Client 1 ready'
    else:
        print 'Problem mit Client 1'
    result = requests.get('http://localhost:8082/portal/medienportal')
    if result:
        if result.status_code == 200:
            print 'Client 2 ready'
    else:
        print 'Problem mit Client 2'
    result = requests.get('http://localhost:8083/portal/medienportal')
    if result:
        if result.status_code == 200:
            print 'Client 3 ready'
    else:
        print 'Problem mit Client 3'
    result = requests.get('http://localhost:8084/portal/medienportal')
    if result:
        if result.status_code == 200:
            print 'Client 4 ready'
    else:
        print 'Problem mit Client 4'        

    #mailbody += u"</body></html>"
    #fromaddr = "internet@bgetem.de"
    #toaddr = "medien@bgetem.de"
    #msg = MIMEMultipart()
    #msg['From'] = fromaddr
    #msg['To'] = toaddr
    #msg['Subject'] = "Update Medienportal"
    #body = mailbody
    #msg.attach(MIMEText(body.encode('utf-8'), 'html', 'utf-8'))
    #text = msg.as_string()
    #server.sendmail(fromaddr, toaddr, text)

if "app" in locals():
    oldargv = sys.argv
    sys.argv = sys.argv[0:1] + sys.argv[3:]
    run()
