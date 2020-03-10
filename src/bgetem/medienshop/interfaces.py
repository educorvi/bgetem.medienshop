# -*- coding: utf-8 -*-
import random
from bgetem.medienshop import _
from five import grok
from DateTime import DateTime
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema import ValidationError
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IContextSourceBinder
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.autoform import directives
from plone.supermodel import model

class IBgetemMedienshopLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

themenabisz = SimpleVocabulary((
    SimpleTerm(value=u'arbeitsbedingte gesundheitsgefahren', token=u'arbeitsbedingte gesundheitsgefahren', title=u'Arbeitsbedingte Gesundheitsgefahren'),
    SimpleTerm(value=u'arbeitsmedizin', token=u'arbeitsmedizin', title=u'Arbeitsmedizin'),
    SimpleTerm(value=u'arbeitsmittel_werkzeuge', token=u'arbeitsmittel_werkzeuge', title=u'Arbeitsmittel/Werkzeuge'),
    SimpleTerm(value=u'ams', token=u'ams', title=u'Arbeitsschutzmanagement-System (AMS)'),
    SimpleTerm(value=u'organisation des arbeitsschutzes', token=u'organisation des arbeitsschutzes', title=u'Arbeitssicherheit und Gesundheitsschutz organisieren'),
    SimpleTerm(value=u'arbeitsstaetten', token=u'arbeitsstaetten', title=u'Arbeitsstätten (Beleuchtung, Fußboden, Verkehrswege)'),
    SimpleTerm(value=u'auslandsaufenthalt', token=u'auslandsaufenthalt', title=u'Auslandsaufenthalt'),
    SimpleTerm(value=u'baustellen', token=u'baustellen', title=u'Bau- und Montagestellen'),
    SimpleTerm(value=u'bgm', token=u'bgm', title=u'Betriebliches Gesundheitsmanagement / Betriebliche Gesundheitsförderung (BGM/BGF)'),
    SimpleTerm(value=u'betriebsarzt', token=u'betriebsarzt', title=u'Betriebsärztliche und sicherheitstechnische Betreuung'),
    SimpleTerm(value=u'betriebsanweisungen', token=u'betriebsanweisungen', title=u'Betriebsanweisungen'),
    SimpleTerm(value=u'betriebssport', token=u'betriebssport', title=u'Betriebssport'),
    SimpleTerm(value=u'bg', token=u'bg', title=u'Berufsgenossenschaft'),
    SimpleTerm(value=u'bildschirmarbeit', token=u'Bildschirmarbeit', title=u'Bildschirmarbeit'),
    SimpleTerm(value=u'biologische arbeitsstoffe', token=u'biologische arbeitsstoffe', title=u'Biologische Arbeitsstoffe'),
    SimpleTerm(value=u'brand und explosionsschutz', token=u'brand und explosionsschutz', title=u'Brand- und Explosionsschutz'),
    SimpleTerm(value=u'demografie', token=u'demografie', title=u'Demografischer Wandel'),
    SimpleTerm(value=u'elektrische anlagen', token=u'elektrische anlagen', title=u'Elektrische Anlagen und Betriebsmittel'),
    SimpleTerm(value=u'elektrische gefaehrdungen', token=u'elektrische gefaehrdungen', title=u'Elektrische Gefährdungen'),
    SimpleTerm(value=u'elektromagnetische felder', token=u'elektromagnetische felder', title=u'Elektromagnetische Felder (EMF)'),
    SimpleTerm(value=u'elektrotechnische arbeiten', token=u'elektrotechnische arbeiten', title=u'Elektrotechnische Arbeiten / Qualifikation'),
    SimpleTerm(value=u'ergonomie', token=u'ergonomie', title=u'Ergonomie'),
    SimpleTerm(value=u'erhoehter Standort', token=u'erhoehter Standort', title=u'Erhöhter Standort/Absturzsicherung'),
    SimpleTerm(value=u'erste hilfe', token=u'erste hilfe', title=u'Erste Hilfe'),
    SimpleTerm(value=u'gefaehrdungsbeurteilung', token=u'gefaehrdungsbeurteilung', title=u'Gefährdungsbeurteilung'),
    SimpleTerm(value=u'gefahrstoffe', token=u'gefahrstoffe', title=u'Gefahrstoffe'),
    SimpleTerm(value=u'hh', token=u'hh', title=u'Hand- und Hautschutz'),
    SimpleTerm(value=u'heben und tragen', token=u'heben und tragen', title=u'Heben und Tragen'),
    SimpleTerm(value=u'innerbetrieblicher transport', token=u'innerbetrieblicher transport', title=u'Innerbetrieblicher Transport'),
    SimpleTerm(value=u'ladungssicherung', token=u'landungssicherung', title=u'Ladungssicherung'),
    SimpleTerm(value=u'lagern und stapeln', token=u'lagern und stapeln', title=u'Lagern und Stapeln'),
    SimpleTerm(value=u'laerm', token=u'laerm', title=u'Lärm'),
    SimpleTerm(value=u'lueftungstechnik', token=u'lueftungstechnik', title=u'Lüftungstechnik'),
    SimpleTerm(value=u'maschinen und anlagen', token=u'maschinen und anlagen', title=u'Maschinen und Anlagen'),
    SimpleTerm(value=u'messungen', token=u'messungen', title=u'Messungen'),
    SimpleTerm(value=u'mitgliedschaft-beitrag', token=u'mitgliedschaft-beitrag', title=u'Mitgliedschaft/Beitrag'),
    SimpleTerm(value=u'psa', token=u'psa', title=u'Persönliche Schutzausrüstungen'),
    SimpleTerm(value=u'psychische belastung', token=u'psychische belastung', title=u'Psychische Belastung und Beanspruchung'),
    SimpleTerm(value=u'raumklima', token=u'raumklima', title=u'Raumklima'),
    SimpleTerm(value=u'rechtsgrundlagen', token=u'rechtsgrundlagen', title=u'Rechtsgrundlagen'),
    SimpleTerm(value=u'regelmaessige pruefungen', token=u'regelmaessige pruefungen', title=u'Regelmäßige Prüfungen'),
    SimpleTerm(value=u'rue', token=u'rue', title=u'Rehabilitation und Entschädigung'),
    SimpleTerm(value=u'schweissen-schneiden-loeten', token=u'schweissen-schneiden-loeten', title=u'Schweißen, Schneiden, Löten'),
    SimpleTerm(value=u'sozialer arbeitsschutz', token=u'sozialer arbeitsschutz', title=u'Sozialer Arbeitsschutz'),
    SimpleTerm(value=u'stolpern-rutschen-stuerzen', token=u'stolpern-rutschen-stuerzen', title=u'Stolpern, Rutschen, Stürzen'),
    SimpleTerm(value=u'ionisierende strahlung', token=u'ionisierende strahlung', title=u'Strahlung, ionisierende'),
    SimpleTerm(value=u'optische strahlung', token=u'optische strahlung', title=u'Strahlung, optische'),
    SimpleTerm(value=u'sucht', token=u'sucht', title=u'Sucht'),
    SimpleTerm(value=u'unternehmermodell', token=u'unternehmermodell', title=u'Unternehmermodell'),
    SimpleTerm(value=u'unterweisung', token=u'unterweisung', title=u'Unterweisung'),
    SimpleTerm(value=u'verkehrssicherheit', token=u'verkehrssicherheit', title=u'Verkehrssicherheit'),
    SimpleTerm(value=u'versicherungsschutz', token=u'versicherungsschutz', title=u'Versicherungsschutz (Arbeitsunfall, Wegeunfall, Berufskrankheit)'),
    SimpleTerm(value=u'vibrationen', token=u'vibrationen', title=u'Vibrationen'),
    SimpleTerm(value=u'zahlen und statistik', token=u'zahlen und statistik', title=u'Zahlen und Statistik'),
    SimpleTerm(value=u'zeitarbeit', token=u'zeitarbeit', title=u'Zeitarbeit'),
    ))

abiszdict = {
    1:u'arbeitsbedingte gesundheitsgefahren',
    2:u'arbeitsmittel_werkzeuge',
    3:u'ams',
    4:u'arbeitsstaetten',
    5:u'auslandsaufenthalt',
    6:u'betriebsarzt',
    7:u'betriebsanweisungen',
    8:u'betriebssport',
    9:u'bg',
    10:u'bildschirmarbeit',
    11:u'biologische arbeitsstoffe',
    12:u'brand und explosionsschutz',
    13:u'demografie',
    14:u'elektrische anlagen',
    15:u'elektrische gefaehrdungen',
    16:u'elektromagnetische felder',
    17:u'elektrotechnische arbeiten',
    18:u'ergonomie',
    19:u'erhoehter Standort',
    20:u'erste hilfe',
    21:u'gefaehrdungsbeurteilung',
    22:u'gefahrstoffe',
    23:u'gda',
    24:u'bgm',
    25:u'hh',
    26:u'heben und tragen',
    27:u'innerbetrieblicher transport',
    28:u'ladungssicherung',
    29:u'lagern und stapeln',
    30:u'laerm',
    31:u'lueftungstechnik',
    32:u'maschinen und anlagen',
    33:u'messungen',
    34:u'mitgliedschaft-beitrag',
    35:u'organisation des arbeitsschutzes',
    36:u'psa',
    37:u'psychische belastung',
    38:u'raumklima',
    39:u'rechtsgrundlagen',
    40:u'regelmaessige pruefungen',
    41:u'rue',
    42:u'schweissen-schneiden-loeten',
    43:u'sozialer arbeitsschutz',
    44:u'stolpern-rutschen-stuerzen',
    45:u'ionisierende strahlung',
    46:u'optische strahlung',
    47:u'sucht',
    48:u'unternehmermodell',
    49:u'unterweisung',
    50:u'verkehrssicherheit',
    51:u'versicherungsschutz',
    52:u'vibrationen',
    53:u'zahlen und statistik',
    54:u'zeitarbeit',
    55:u'arbeitsmedizin',
    }


BRANCHEN = {
    u'Druck und Papierverarbeitung':[
        SimpleTerm(value=u'buchbinderei', token=u'buchbinderei', title=u'Buchbinderei und Druckverarbeitung'),
        SimpleTerm(value=u'digitaldruck', token=u'digitaldruck', title=u'Digital-, Sieb- und Sonderdruck'),
        SimpleTerm(value=u'etikettendruck', token=u'etikettendruck', title=u'Etiketten- und Schmalbahndruck'),
        SimpleTerm(value=u'flexodruck', token=u'flexodruck', title=u'Flexo- und Tiefdruck'),
        SimpleTerm(value=u'foto', token=u'foto', title=u'Foto und Grafik'),
        SimpleTerm(value=u'offsetdruck', token=u'offsetdruck', title=u'Offsetdruck'),
        SimpleTerm(value=u'packmittelherstellung', token=u'packmittelherstellung', title=u'Packmittelherstellung und Wellpappe'),
        SimpleTerm(value=u'uvdruck', token=u'uvdruck', title=u'UV-Druck'),
        SimpleTerm(value=u'zeitungszustellung', token=u'zeitungszustellung', title=u'Zeitungszustellung'),],
    u'Elektrohandwerke':[
        SimpleTerm(value=u'elektromaschinenbau', token=u'elektromaschinenbau', title=u'Elektromaschinenbau'),
        SimpleTerm(value=u'elektrotechnik', token=u'elektrotechnik', title=u'Elektrotechnik'),
        SimpleTerm(value=u'informationstechnik', token=u'informationstechnik', title=u'Informationstechnik'),
        SimpleTerm(value=u'photovoltaikanlagen', token=u'photovoltaikanlagen', title=u'Photovoltaikanlagen'),],
    u'Elektrotechnische Industrie':[
        SimpleTerm(value=u'raumfahrzeuge', token=u'raumfahrzeuge', title=u'Bau von Luft- und Raumfahrzeugen'),
        SimpleTerm(value=u'baugruppen', token=u'baugruppen', title=u'Elektrische Baugruppen, Geräte und Halbleiter'),
        SimpleTerm(value=u'kleingrossgeraete', token=u'kleingrossgeraete', title=u'Elektrische Klein- und Großgeräte sowie elektromedizinische Geräte'),
        SimpleTerm(value=u'industriemontage', token=u'industriemontage', title=u'Elektrotechnische Großinstallation und Industriemontage'),
        SimpleTerm(value=u'kfzindustrie', token=u'kfzindustrie', title=u'Module für die Kfz-Industrie'),],
    u'Energie- und Wasserwirtschaft':[
        SimpleTerm(value=u'abwasser', token=u'abwasser', title=u'Abwasserentsorgung'),
        SimpleTerm(value=u'baeder', token=u'baeder', title=u'Bäder'),
        SimpleTerm(value=u'biogas', token=u'biogas', title=u'Biogas'),
        SimpleTerm(value=u'fernwaerme', token=u'fernwaerme', title=u'Fernwärmeversorgung'),
        SimpleTerm(value=u'gaserversorgung', token=u'gaserversorgung', title=u'Gasversorgung'),
        SimpleTerm(value=u'kraftwerke', token=u'kraftwerke', title=u'Kraftwerke'),
        SimpleTerm(value=u'sparten', token=u'sparten', title=u'Spartenübergreifendes'),
        SimpleTerm(value=u'stromversorgung', token=u'stromversorgung', title=u'Stromversorgung (EVU)'),
        SimpleTerm(value=u'wasserversorgung', token=u'wasserversorgung', title=u'Wasserversorgung'),
        SimpleTerm(value=u'windenergie', token=u'windenergie', title=u'Windenergie'),],
    u'Feinmechanik':[
        SimpleTerm(value=u'automaten', token=u'automaten', title=u'Automaten'),
        SimpleTerm(value=u'bueromaschinen', token=u'bueromaschinen', title=u'Büromaschinen'),
        SimpleTerm(value=u'dentaltechnik', token=u'dentaltechnik', title=u'Dentaltechnik'),
        SimpleTerm(value=u'optik', token=u'optik', title=u'Feinmechanische und optische Instrumente und Geräte'),
        SimpleTerm(value=u'film', token=u'film', title=u'Filmproduktion'),
        SimpleTerm(value=u'galvanotechnik', token=u'galvanotechnik', title=u'Galvanotechnik'),
        SimpleTerm(value=u'kino', token=u'kino', title=u'Kino'),
        SimpleTerm(value=u'raumfahrttechnik', token=u'raumfahrttechnik', title=u'Luft- und Raumfahrttechnik'),
        SimpleTerm(value=u'metallwaren', token=u'metallwaren', title=u'Metallwaren'),
        SimpleTerm(value=u'musikinstrumente', token=u'musikinstrumente', title=u'Musikinstrumente'),
        SimpleTerm(value=u'oberflaechenbehandlung', token=u'oberflaechenbehandlung', title=u'Oberflächenbehandlung'),
        SimpleTerm(value=u'orthopaedietechnik', token=u'orthopaedietechnik', title=u'Orthopädietechnik'),
        SimpleTerm(value=u'rehatechnik', token=u'rehatechnik', title=u'Rehatechnik'),
        SimpleTerm(value=u'schusswaffen', token=u'schusswaffen', title=u'Schusswaffen'),
        SimpleTerm(value=u'tierpraeparation', token=u'tierpraeparation', title=u'Tierpräparation'),
        SimpleTerm(value=u'uhren und schmuck', token=u'uhren und schmuck', title=u'Uhren und Schmuck'),],
    u'Textil und Mode':[
        SimpleTerm(value=u'garnherstellung', token=u'garnherstellung', title=u'Garnherstellung'),
        SimpleTerm(value=u'herstellung textiler flaechen', token=u'herstellung textiler flaechen', title=u'Herstellung textiler Flächen'),
        SimpleTerm(value=u'konfektion', token=u'konfektion', title=u'Konfektion'),
        SimpleTerm(value=u'schuhherstellung', token=u'schuhherstellung', title=u'Schuhherstellung und -reparatur'),
        SimpleTerm(value=u'textilreinigung', token=u'textilreinigung', title=u'Textilreinigung'),
        SimpleTerm(value=u'textilveredelung', token=u'textilveredelung', title=u'Textilveredlung'),
        SimpleTerm(value=u'waescherei', token=u'waescherei', title=u'Wäscherei'),],
    }


bgetembranchen = SimpleVocabulary((
    SimpleTerm(value=u'druckundpapier', token=u'druckundpapier', title=u'Druck und Papierverarbeitung'),
    SimpleTerm(value=u'buchbinderei', token=u'buchbinderei', title=u'Buchbinderei und Druckverarbeitung'),
    SimpleTerm(value=u'digitaldruck', token=u'digitaldruck', title=u'Digital-, Sieb- und Sonderdruck'),
    SimpleTerm(value=u'etikettendruck', token=u'etikettendruck', title=u'Etiketten- und Schmalbahndruck'),
    SimpleTerm(value=u'flexodruck', token=u'flexodruck', title=u'Flexo- und Tiefdruck'),
    SimpleTerm(value=u'foto', token=u'foto', title=u'Foto und Grafik'),
    SimpleTerm(value=u'offsetdruck', token=u'offsetdruck', title=u'Offsetdruck'),
    SimpleTerm(value=u'packmittelherstellung', token=u'packmittelherstellung', title=u'Packmittelherstellung und Wellpappe'),
    SimpleTerm(value=u'uvdruck', token=u'uvdruck', title=u'UV-Druck'),
    SimpleTerm(value=u'zeitungszustellung', token=u'zeitungszustellung', title=u'Zeitungszustellung'),
    SimpleTerm(value=u'elektrohandwerke', token=u'elektrohandwerke', title=u'Elektrohandwerke'),
    SimpleTerm(value=u'elektromaschinenbau', token=u'elektromaschinenbau', title=u'Elektromaschinenbau'),
    SimpleTerm(value=u'elektrotechnik', token=u'elektrotechnik', title=u'Elektrotechnik'),
    SimpleTerm(value=u'informationstechnik', token=u'informationstechnik', title=u'Informationstechnik'),
    SimpleTerm(value=u'photovoltaikanlagen', token=u'photovoltaikanlagen', title=u'Photovoltaikanlagen'),
    SimpleTerm(value=u'elektrotechnische industrie', token=u'elektrotechnische industrie', title=u'Elektrotechnische Industrie'),
    SimpleTerm(value=u'kleingrossgeraete', token=u'kleingrossgeraete', title=u'Elektrische Klein- und Großgeräte sowie elektromedizinische Geräte'),
    SimpleTerm(value=u'baugruppen', token=u'baugruppen', title=u'Elektrische Baugruppen, Geräte und Halbleiter'),
    SimpleTerm(value=u'kfzindustrie', token=u'kfzindustrie', title=u'Module für die Kfz-Industrie'),
    SimpleTerm(value=u'industriemontage', token=u'industriemontage', title=u'Elektrotechnische Großinstallation und Industriemontage'),
    SimpleTerm(value=u'raumfahrzeuge', token=u'raumfahrzeuge', title=u'Bau von Luft- und Raumfahrzeugen'),
    SimpleTerm(value=u'energie und wasserwirtschaft', token=u'energie und wasserwirtschaft', title=u'Energie- und Wasserwirtschaft'),
    SimpleTerm(value=u'wasserversorgung', token=u'wasserversorgung', title=u'Wasserversorgung'),
    SimpleTerm(value=u'gaserversorgung', token=u'gaserversorgung', title=u'Gasversorgung'),
    SimpleTerm(value=u'fernwaerme', token=u'fernwaerme', title=u'Fernwärmeversorgung'),
    SimpleTerm(value=u'abwasser', token=u'abwasser', title=u'Abwasserentsorgung'),
    SimpleTerm(value=u'stromversorgung', token=u'stromversorgung', title=u'Stromversorgung (EVU)'),
    SimpleTerm(value=u'baeder', token=u'baeder', title=u'Bäder'),
    SimpleTerm(value=u'biogas', token=u'biogas', title=u'Biogas'),
    SimpleTerm(value=u'sparten', token=u'sparten', title=u'Spartenübergreifendes'),
    SimpleTerm(value=u'windenergie', token=u'windenergie', title=u'Windenergie'),
    SimpleTerm(value=u'kraftwerke', token=u'kraftwerke', title=u'Kraftwerke'),
    SimpleTerm(value=u'feinmechanik', token=u'feinmechanik', title=u'Feinmechanik'),
    SimpleTerm(value=u'automaten', token=u'automaten', title=u'Automaten'),
    SimpleTerm(value=u'bueromaschinen', token=u'bueromaschinen', title=u'Büromaschinen'),
    SimpleTerm(value=u'dentaltechnik', token=u'dentaltechnik', title=u'Dentaltechnik'),
    SimpleTerm(value=u'optik', token=u'optik', title=u'Feinmechanische und optische Instrumente und Geräte'),
    SimpleTerm(value=u'film', token=u'film', title=u'Filmproduktion'),
    SimpleTerm(value=u'galvanotechnik', token=u'galvanotechnik', title=u'Galvanotechnik'),
    SimpleTerm(value=u'kino', token=u'kino', title=u'Kino'),
    SimpleTerm(value=u'raumfahrttechnik', token=u'raumfahrttechnik', title=u'Luft- und Raumfahrttechnik'),
    SimpleTerm(value=u'metallwaren', token=u'metallwaren', title=u'Metallwaren'),
    SimpleTerm(value=u'musikinstrumente', token=u'musikinstrumente', title=u'Musikinstrumente'),
    SimpleTerm(value=u'oberflaechenbehandlung', token=u'oberflaechenbehandlung', title=u'Oberflächenbehandlung'),
    SimpleTerm(value=u'orthopaedietechnik', token=u'orthopaedietechnik', title=u'Orthopädietechnik'),
    SimpleTerm(value=u'rehatechnik', token=u'rehatechnik', title=u'Rehatechnik'),
    SimpleTerm(value=u'schusswaffen', token=u'schusswaffen', title=u'Schusswaffen'),
    SimpleTerm(value=u'tierpraeparation', token=u'tierpraeparation', title=u'Tierpräparation'),
    SimpleTerm(value=u'uhren und schmuck', token=u'uhren und schmuck', title=u'Uhren und Schmuck'),
    SimpleTerm(value=u'textilundmode', token=u'textilundmode', title=u'Textil und Mode'),
    SimpleTerm(value=u'herstellung textiler flaechen', token=u'herstellung textiler flaechen', title=u'Herstellung textiler Flächen'),
    SimpleTerm(value=u'konfektion', token=u'konfektion', title=u'Konfektion'),
    SimpleTerm(value=u'schuhherstellung', token=u'schuhherstellung', title=u'Schuhherstellung und -reparatur'),
    SimpleTerm(value=u'textilreinigung', token=u'textilreinigung', title=u'Textilreinigung'),
    SimpleTerm(value=u'garnherstellung', token=u'garnherstellung', title=u'Garnherstellung'),
    SimpleTerm(value=u'waescherei', token=u'waescherei', title=u'Wäscherei'),
    SimpleTerm(value=u'textilveredelung', token=u'textilveredelung', title=u'Textilveredlung')
    ))

branchendict = {
    'DP':u'druckundpapier',
    1:u'buchbinderei',
    2:u'digitaldruck',
    3:u'etikettendruck',
    4:u'flexodruck',
    5:u'foto',
    6:u'offsetdruck',
    7:u'packmittelherstellung',
    8:u'uvdruck',
    9:u'zeitungszustellung',
    'AH':u'elektrohandwerke',
    10:u'elektromaschinenbau',
    11:u'elektrotechnik',
    12:u'informationstechnik',
    13:u'photovoltaikanlagen',
    14:u'baustellen',
    'EI':u'elektrotechnische industrie',
    15:u'kleingrossgeraete',
    16:u'baugruppen',
    17:u'kfzindustrie',
    18:u'industriemontage',
    19:u'raumfahrzeuge',
    'EW':u'energie und wasserwirtschaft',
    20:u'wasserversorgung',
    21:u'gaserversorgung',
    22:u'fernwaerme',
    23:'abwasser',
    24:u'stromversorgung',
    25:u'baeder',
    26:u'biogas',
    27:u'sparten',
    28:u'windenergie',
    29:u'kraftwerke',
    'FM':u'feinmechanik',
    30:u'automaten',
    31:u'bueromaschinen',
    32:u'dentaltechnik',
    33:u'optik',
    34:u'film',
    35:u'galvanotechnik',
    36:u'kino',
    37:u'raumfahrttechnik',
    38:u'metallwaren',
    39:u'musikinstrumente',
    40:u'oberflaechenbehandlung',
    41:u'orthopaedietechnik',
    42:u'rehatechnik',
    43:u'schusswaffen',
    44:u'tierpraeparation',
    45:u'uhren und schmuck',
    'TM':u'textilundmode',
    46:u'herstellung textiler flaechen',
    47:u'konfektion',
    48:u'schuhherstellung',
    49:u'textilreinigung',
    50:u'garnherstellung',
    51:u'waescherei',
    52:u'textilveredelung',
    }

bgetemzielgruppen = SimpleVocabulary((
    SimpleTerm(value=u'auszubildende', token=u'auszubildende', title=u'Auszubildende'),
    SimpleTerm(value=u'betriebsaerzte', token=u'betriebsaerzte', title=u'Betriebsärztinnen und Betriebsärzte'),
    SimpleTerm(value=u'betriebsraete', token=u'betriebsraete', title=u'Betriebs-/Personalräte'),
    SimpleTerm(value=u'fachkraefte', token=u'fachkraefte', title=u'Fachkräfte'),
    SimpleTerm(value=u'fasi', token=u'fasi', title=u'Fachkräfte für Arbeitssicherheit'),
    SimpleTerm(value=u'fuehrung', token=u'fuehrung', title=u'Führungskräfte'),
    SimpleTerm(value=u'kmu', token=u'kmu', title=u'kleinere und mittlere Unternehmen (KMU)'),
    SimpleTerm(value=u'fachkraft', token=u'fachkraft', title=u'Mitarbeiterinnen und Mitarbeiter'),
    SimpleTerm(value=u'sicherheitsbeauftragte', token=u'sicherheitsbeauftragte', title=u'Sicherheitsbeauftragte'),
    SimpleTerm(value=u'unternehmer', token=u'unternehmer', title=u'Unternehmerinnen und Unternehmer'),
    ))

zielgruppendict = {
    1:'auszubildende',
    2:'betriebsaerzte',
    3:'betriebsraete',
    4:'fachkraft',
    5:'fasi',
    6:'fuehrung',
    7:'kmu',
    8:'sicherheitsbeauftragte',
    9:'unternehmer',
    }

bgetemmedienart = SimpleVocabulary((
    SimpleTerm(value=u'K01', token=u'infofaltblatt', title=u'Faltblätter'),
    SimpleTerm(value=u'K03', token=u'broschueren', title=u'Broschüren'),
    SimpleTerm(value=u'K04', token=u'multimedia', title=u'Multimedia'),
    SimpleTerm(value=u'K05', token=u'plakate', title=u'Plakate/Aushänge'),
    SimpleTerm(value=u'K06', token=u'film', title=u'Filme'),
    SimpleTerm(value=u'K07', token=u'azubi', title=u'Azubi-Pakete'),
    SimpleTerm(value=u'K08', token=u'umodellordner', title=u'Unternehmermodell-Ordner'),
    SimpleTerm(value=u'K09', token=u'wandkalender', title=u'Aktionsmedien'),
    SimpleTerm(value=u'K10', token=u'kugelschreiber', title=u'Anstecknadel, Aufkleber'),
    SimpleTerm(value=u'K11', token=u'download', title=u'Download Medien'),
    SimpleTerm(value=u'P01', token=u'bgv', title=u'DGUV Vorschriften'),
    SimpleTerm(value=u'P02', token=u'beiblaetter', title=u'DGUV Regeln'),
    SimpleTerm(value=u'P03', token=u'bgi-bgr', title=u'DGUV Informationen'),
    SimpleTerm(value=u'P04', token=u'sammlungen', title=u'DGUV Grundsätze'),
    SimpleTerm(value=u'P05', token=u'gesetze', title=u'Gesetze/Verordnungen'),
    SimpleTerm(value=u'P08', token=u'download_praevention', title=u'Download Regelwerk'),
    ))

handlungsebenen = SimpleVocabulary((
    SimpleTerm(value=u'orga_kultur', token=u'orga_kultur', title=u'Organisation und Kultur'),
    SimpleTerm(value=u'technik_verfahren', token=u'technik_verfahren', title=u'Technik und Verfahren'),
    SimpleTerm(value=u'umsetzung', token=u'umsetzung', title=u'Umsetzung'),
    SimpleTerm(value=u'verhalten', token=u'verhalten', title=u'Verhalten'),
    ))

medienkonzept = SimpleVocabulary((
    SimpleTerm(value=u'fokussiert', token=u'fokussiert', title=u'Fokussiert'),
    SimpleTerm(value=u'fundiert', token=u'fundiert', title=u'Fundiert'),
    SimpleTerm(value=u'elementar', token=u'elementar', title=u'Elementar'),
    ))

mediendict = {
    1:'elementar',
    2:'fokussiert',
    3:'fundiert',
    }

def possibleArtikel(context):
    pcat = getToolByName(context, 'portal_catalog')
    brains = pcat(portal_type = 'Artikel')
    terms = []
    if brains:
        for i in brains:
            terms.append(SimpleVocabulary.createTerm(i.id, i.id, i.Title))
    return SimpleVocabulary(terms)
directlyProvides(possibleArtikel, IContextSourceBinder)

@grok.provider(IContextAwareDefaultFactory)
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

class IArtikel(model.Schema):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    artikelnummer = schema.TextLine(
        title=_(u'Artikelnummer'),
        description=_(u'Diese Artikelnummer stellt die Verbindung zum SAP-\
            Medienshop her.'),
        required=True,
    )

    beschreibung = RichText(
        title = _(u'Artikelbeschreibung'),
        description = _(u'Hier können Sie eine ausführliche Beschreibung des\
            Artikels verfassen.'),
        required = False,
    )

    abisz = schema.List(
        title = _(u'Themen von A-Z'),
        description = _(u'Hier können Sie dem Artikel Themen von A-Z zuordnen'),
        value_type = schema.Choice(vocabulary = themenabisz),
        required = True,
    )

    branchen = schema.List(
        title = _(u'Branchen der BG ETEM'),
        description = _(u'Hier können Sie dem Artikel Branchen der BG ETEM zuordnen.'),
        value_type = schema.Choice(vocabulary = bgetembranchen),
        required = True,
    )

    zielgruppen = schema.List(
        title = _(u'Zielgruppen der BG ETEM'),
        description = _(u'Hier können Sie dem Artikel Zielgruppen der BG ETEM\
            zuordnen.'),
        value_type = schema.Choice(vocabulary = bgetemzielgruppen),
        required = True,
    )

    handlungsebenen = schema.List(
        title = u'Handlungsebenen PPM',
        value_type = schema.Choice(vocabulary = handlungsebenen),
        required = False,
    )

    medienkonzept = schema.Choice(
        title = u'Medienkonzept BG ETEM',
        vocabulary = medienkonzept,
        required = False,
    )

    medienart = schema.Choice(
        title = _(u'Medienart des Artikels'),
        description = _(u'Hier können Sie auswählen zu welcher Medienart der\
            Artikel gehört'),
        vocabulary = bgetemmedienart,
        required = True,
    )

    titelbild = NamedBlobImage(
        title = _(u'Titelbild des Artikels'),
        required = False,
    )

    bildunterschrift = schema.TextLine(
        title = _(u'Bildunterschrift'),
        required = False,
    )

    download_only = schema.Bool(
        title = _(u'Nur Download'),
        description = _(u'Hier markieren, wenn der Artikel nur per Download verfügbar ist.'),
        required = False,
    )

    download = NamedBlobFile(
        title = _(u'Datei zum Download'),
        required = False,
    )

    filetitle = schema.TextLine(
        title = _(u'Dateititel'),
        description = _(u'Hier können Sie alternativ einen Titel für die Datei vergeben.'),
        required = False,
    )

    artikelreferenzen = RelationList(
        title = _(u'Referenzen zu diesem Artikel'),
        description = _(u'Hier können Sie Referenzen zu diesem Artikel auswählen'),
        value_type = RelationChoice(title=u"Artikelreferenzen", source=ObjPathSourceBinder()),
        required = False,
    )

    interne_bemerkungen = schema.Text(
            title = u"Interne Bemerkungen",
            description = u"Dieses Feld bitte nur für interne Bemerkungen verwenden.",
            required = False,
    )

    webcode = schema.TextLine(
              title=u"Webcode",
              description=u"Der Webcode für diesen Artikel wird automatisch errechnet und angezeigt. Sie\
                          können diesen Webcode bei Bedarf jedoch jederzeit überschreiben.",
              required = True,
              defaultFactory = genWebcode,
              )

class IArtikelListe(Interface):
    """Schema fuer die Artikelliste einer Bestellung"""

    artikel = schema.TextLine(title = u'Art.-nr.', required = True)
    bestellnummer = schema.TextLine(title = u'Bestellnummer', required = True)
    beschreibung = schema.TextLine(title = u'Beschreibung', required = True)
    anzahl = schema.Int(title = u'Anzahl', required = True)


class NotValidAnrede(ValidationError):
    u""" Bitte treffen Sie eine Auswahl 'Herr' oder 'Frau' für die Anrede. """

def validateAnrede(value):
    if value:
        if value == u'Auswahl':
            raise NotValidAnrede(value)
    return True

def validatePLZ(value):
    return True

def validateMail(value):
    return True

class NotValidHinweis(ValidationError):
    u""" Bitte bestätigen Sie die Nutzungsbedingungen für den BGHW-Medienshop. """

def validateHinweis(value):
    if value:
        if value == u'nein':
            raise NotValidHinweis(value)
    return True


class IBestellung(Interface):
    """Schema fuer das Bestellformular"""

    bestellung = schema.List(title = u'Ihre Bestellung bei der BG ETEM',
                             description = u'Bitte kontrollieren Sie Ihre Auswahl und korrigieren\
                             eventuell die angegebenen Bestellmengen',
                             value_type = schema.Object(title = u'Bestellung',
                                                        schema = IArtikelListe),
                             required = True,)

class IVersandadresse(Interface):

    mitgliedsbetrieb = schema.Bool(title = u'Mitgliedsbetrieb der BG ETEM',
                                   description = u'Bitte bestätigen Sie hier die Mitgliedschaft Ihres\
                                   Betriebes bei der BG ETEM.',
                                   default = True,)

    mitgliedsnummer = schema.TextLine(title = u'Mitgliedsnummer',
                                      required = False,)

    firma = schema.TextLine(title = u'Firma', required = True)

    anrede = schema.Choice(title = u'Anrede',
                           description = u'Bitte treffen Sie eine Auswahl.',
                           vocabulary = SimpleVocabulary.fromValues([u'Auswahl', u'Herr', u'Frau']),
                           required = True,
                           constraint = validateAnrede,)

    titel = schema.Choice(title = u'Titel',
                          description = u'Bitte treffen Sie eine Auswahl.',
                          vocabulary = SimpleVocabulary.fromValues([u'kein Titel', u'Dr.', u'Prof.']),
                          default = u'kein Titel',
                          required = False,)

    vorname = schema.TextLine(title = u'Vorname', required = True)

    name = schema.TextLine(title = u'Name', required = True)

    strhnr = schema.TextLine(title = u'Straße und Hausnummer', required = True)

    plz = schema.TextLine(title = u'Postleitzahl', required = True, constraint=validatePLZ)

    ort = schema.TextLine(title = u'Ort', required = True)

    telefon = schema.TextLine(title = u'Telefon', required = False)

    email = schema.TextLine(title = u'E-Mail', required = True, constraint=validateMail)

    lieferung = schema.Bool(title = u'abweichende Lieferadresse',
                            description = u'Bitte hier markieren, wenn eine abweichende Lieferanschrift\
                            gewünscht wird.',
                            default = False,)

    a_firma = schema.TextLine(title = u'Firma', required = False)

    a_anrede = schema.Choice(title = u'Anrede',
                             description = u'Bitte treffen Sie eine Auswahl.',
                             vocabulary = SimpleVocabulary.fromValues([u'Auswahl', u'Herr', u'Frau']),
                             required = False,)

    a_titel = schema.Choice(title = u'Titel',
                            description = u'Bitte treffen Sie eine Auswahl.',
                            vocabulary = SimpleVocabulary.fromValues([u'kein Titel', u'Dr.', u'Prof.']),
                            default = u'kein Titel',
                            required = False,)

    a_vorname = schema.TextLine(title = u'Vorname', required = False)

    a_name = schema.TextLine(title = u'Name', required = False)

    a_strhnr = schema.TextLine(title = u'Straße und Hausnummer', required = False)

    a_plz = schema.TextLine(title = u'Postleitzahl', required = False)

    a_ort = schema.TextLine(title = u'Ort', required = False)

    hinweis = schema.Choice(title = u'Einverständniserklärung',
                          description = u'Ich erkläre mich im Namen des Unternehmens, das ich vertrete\
                          , mit den Nutzungsbedingungen der BG ETEM einverstanden.',
                          vocabulary = SimpleVocabulary.fromValues([u'ja', u'nein']),
                          required = True,
                          constraint = validateHinweis,)
