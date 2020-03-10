Write Delete
============

Das Script wird wiefolgt gestartet:

..code-block: bash
  bin/instance run src/bgetem.medienshop/src/bgetem/medienshop/scripts/import.py --shoppath Plone/shop

Der Parameter --shoppath gibt an wo sich der Shop innerhalb des RootFolders
befindet.


Bemerkungen: 

Die Artikelnummer musste kodiert werden um Sie als ID/KEY innerhalb eines Plone-Folders verwenden zu können.
Gibt es eine Differenz zwischen Artikeln im SHOP und SAPAPI werden die
*Überhängenden* im SHOP gelöscht. Es wäre allerdings auch Denkbar diese in
einen anderen WF-Status zu setzen.


CK
