from collective.beaker.interfaces import ISession
from pymongo import MongoClient
from bson.objectid import ObjectId
from App.config import getConfiguration
from bgetem.medienshop.mongoutil import get_mongo_client
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))

def getSessionData(request):
    """
    Liest das SessionCookie
    """
    session = ISession(request)
    mongo_objid = session.get('key', '')
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.mp_collection
    if mongo_objid:
        data = collection.find_one({"_id":mongo_objid})
    else:
        data = {}
    return data

def setSessionData(request, data):
    """
    Schreibt das Cookie in die Session
    """
    session = ISession(request)
    mongo_objid = session.get('key', '')
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.mp_collection
    if mongo_objid:
        insert = collection.replace_one({'_id':mongo_objid}, data, upsert=True)
        session.save()
    else:
        insert = collection.insert_one(data).inserted_id
        session['key'] = insert
        session.save()
    return insert

def saveMongoUser(data):
    """
    Save data before validation of e-Mail-Address
    """
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.vali_collection
    insert = collection.insert_one(data).inserted_id
    return insert

def getMongoUser(key):
    mongo_objid = ObjectId(key)
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.vali_collection
    data = collection.find_one({"_id":mongo_objid})
    return data

def saveMongoUserForDel(email, code):
    """
    Save data before validation of e-Mail-Address
    """
    data= {'email':email, 'delcode':code}
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.del_collection
    insert = collection.insert_one(data).inserted_id
    return insert

def readMongoUserForDel(key):
    mongo_objid = ObjectId(key)
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.del_collection
    data = collection.find_one({"_id":mongo_objid})
    return data

def saveMongoUserForPwReset(email, code):
    """
    Save data before Passwort Reset E-Mail.
    """
    data= {'email':email, 'pwcode':code}
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.del_collection
    insert = collection.insert_one(data).inserted_id
    return insert

def readMongoUserForPwReset(key):
    mongo_objid = ObjectId(key)
    client = get_mongo_client().client
    db = client.mp_database
    collection = db.del_collection
    data = collection.find_one({"_id":mongo_objid})
    return data

def delSessionData(request):
    """
    Loescht das Cookie
    """
    session = ISession(request)
    session.delete()
