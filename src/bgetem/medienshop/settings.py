# -*- coding: utf-8 -*-
from zope.interface import provider
from zope.interface import Interface
from zope import schema
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from z3c.form import form
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api as ploneapi

class IMedienportalSettings(Interface):
    """ Define settings data structure """

    wartung = schema.Bool(title=u"Wartungsseite aktivieren",
                          description=u"Mit dieser Einstellung aktivieren Sie die Wartungsseite für das Medienportal.",)


class MedienportalPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IMedienportalSettings


MedienportalPanelView = layout.wrap_form(MedienportalPanelForm, ControlPanelFormWrapper)
MedienportalPanelView.label = u"Medienportal Einstellungen"

