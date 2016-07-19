# -*- coding: utf-8 -*-
import json
from bson.objectid import ObjectId

from core.connection_provider import MongoConnectionProvider
from errors import MediaProError


class ReadOnlyRepository:
    def __init__(self, db_name, collection_name):
        self.__db_name = db_name
        self.__collection_name = collection_name
        self._collection = MongoConnectionProvider.get_instance()\
            .get_database(db_name).get_collection(collection_name)

    def find(self, query, *args, **kwargs):
        format_dates_query(query)
        return self._collection.find(query, *args, **kwargs)

    def find_one(self, _id):
        validate_id(_id)
        return self._collection.find_one(ObjectId(_id))


class FullAccessRepository(ReadOnlyRepository):
    def __init__(self, db_name, collection_name):
        ReadOnlyRepository.__init__(self, db_name, collection_name)

    def insert(self, document):
        return self._collection.insert_one(document)

    def update(self, query, update, upsert=False):
        return self._collection.update_one(query, update, upsert)

    def update_by_id(self, _id, update):
        validate_id(_id)
        return self.update({'_id': ObjectId(_id)}, {'$set': update})

    def delete(self, query):
        return self._collection.delete_one(query)

    def delete_by_id(self, _id):
        validate_id(_id)
        return self.delete({'_id': ObjectId(_id),
                            'status': {'$ne': 'RUNNING'}})


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class JSONDecoder:
    def __init__(self):
        pass

    def decode(self, text):
        return json.loads(text)


def validate_id(_id):
    if not ObjectId.is_valid(_id):
        raise MediaProError(MediaProError.INVALID_ID)


def format_dates_query(query):
    for k, v in query.iteritems():
        if isinstance(v, dict):
            format_dates_query(v)
        else:
            if k == 'from':
                query['$gte'] = query.pop('from')
            elif k == 'to':
                query['$lt'] = query.pop('to')
