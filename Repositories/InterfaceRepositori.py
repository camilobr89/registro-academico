from http import client
from re import X
import pymongo 
import certifi 
from bson import DBRef 
from bson.objectid import ObjectId 
from typing import TypeVar, Generic, List, get_origin, get_args
import json

T = TypeVar('T')

class InterfaceRepositori(Generic[T]):
    def __init__(self):
        ca = certifi.where()
        dataConfig = self.loadFileConfig()
        client = pymongo.MongoClient(dataConfig['db-connect'], tlsCAFile=ca)
        self.db = client[dataConfig['db']]
        theClass = get_args(self.__orig_bases__[0])
        self.collection = theClass[0].__name__.lower()

    def loadFileConfig(self):
        with open('config.json') as file:
            data = json.load(file)
        return data

    def save(self, item: T):
        laCollection = self.db[self.collection]
        elId = ""
        item = self.transformRefs(item)
        if hasattr(item, '_id') and item._id != "":
            elId = item._id
            _id = ObjectId(elId)
            loCollection = self.db[self.collection]
            delattr(item, '_id')
            item = item.__dict__
            updateItem = { "$set": item }
            x = laCollection.update_one({ "_id": _id }, updateItem)
        else:
            _id = laCollection.insert_one(item.__dict__)
            elId = _id.inserted_id.__str__()

        x = laCollection.find_one({"_id": ObjectId(elId)})
        x["_id"] = x["_id"].__str__()
        return self.findById(elId)

    def delete(self, id):
        laCollection = self.db[self.collection]
        account = laCollection.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": account} 
    
    def update(self, id, item: T):
        _id = ObjectId(id) 
        laCollection = self.db[self.collection]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item} 
        x = laCollection.update_one({"_id": _id}, updateItem) 
        return {"updated_count": x.matched_count}

    def findById(self, id):
        laCollection = self.db[self.collection]
        x = laCollection.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    def findAll(self):
        laCollection = self.db[self.collection]
        data = []
        for x in laCollection.find():
            x["_id"] = x["_id"].__str__() 
            x = self.transformObjectIds(x) 
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def query(self, theQuery):
        laCollection = self.db[self.collection]
        data = []
        for x in laCollection.find(theQuery):
            x["_id"] = x["_id"].__str__() 
            x = self.transformObjectIds(x) 
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def queryAggregation(self, theQuery):
        laCollection = self.db[self.collection]
        data = []
        for x in laCollection.aggregate(theQuery):
            x["_id"] = x["_id"].__str__() 
            x = self.transformObjectIds(x) 
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):
                laCollection = self.db[x[k].collection]
                value = laCollection.find_one({"_id": ObjectId(x[k].id)})
                value["_id"] = value["_id"].__str__()
                x[k] = value
                x[k] = self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict) :
                x[k] = self.getValuesDBRef(x[k]) 
        return x

    def getValuesDBRefFromList(self, theList):
        newList = []
        laCollection = self.db[theList[0]._id.collection]
        for item in theList:
            value = laCollection.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList

    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__() 
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute]=self.transformObjectIds(x[attribute])
        return x

    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = x
        return newList

    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("Object") == 1:
                newObject = self.ObjectToDBRef(getattr(item, k))
                setattr(item, k, newObject) 
        return item

    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower() 
        return DBRef(nameCollection, ObjectId(item._id))

        
            

