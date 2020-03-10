from zope.interface import implementer
from bgetem.medienshop.interfaces import bgetembranchen, bgetemzielgruppen, bgetemmedienart, themenabisz
from zope.schema.interfaces import IVocabularyFactory

@implementer(IVocabularyFactory)
class UserFriendlyBranchen(object):
    def __call__(self, context):
        return bgetembranchen
UserFriendlyBranchenVocabularyFactory = UserFriendlyBranchen()    

@implementer(IVocabularyFactory)
class UserFriendlyZielgruppen(object):
    def __call__(self, context):
        return bgetemzielgruppen
UserFriendlyZielgruppenVocabularyFactory = UserFriendlyZielgruppen()

@implementer(IVocabularyFactory)
class UserFriendlyMedienarten(object):
    def __call__(self, context):
        return bgetemmedienart
UserFriendlyMedienartenVocabularyFactory = UserFriendlyMedienarten()

@implementer(IVocabularyFactory)
class UserFriendlyThemen(object):
    def __call__(self, context):
        return themenabisz
UserFriendlyThemenVocabularyFactory = UserFriendlyThemen()
