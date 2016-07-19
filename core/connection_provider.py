# -*- coding: utf-8 -*-
from pymongo import MongoClient


class MongoConnectionProvider:
    """
    Provides a single connection instance for MongoDB.
    """
    __instance = None

    @classmethod
    def connect(cls, uri):
        connection = MongoClient(host=uri)
        cls.__instance = MongoConnectionProvider(connection)

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def __init__(self, connection):
        self.__connection = connection

    def __del__(self):
        self.__connection.close()

    def get_database(self, db_name, codec_options=None, read_preference=None,
                     write_concern=None, read_concern=None):
        """Get a :class:`~pymongo.database.Database` with the given name and
        options.

        Useful for creating a :class:`~pymongo.database.Database` with
        different codec options, read preference, and/or write concern from
        this :class:`MongoClient`.

        :Parameters:
          - `name`: The name of the database - a string.
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`. If ``None`` (the
            default) the :attr:`codec_options` of this :class:`MongoClient` is
            used.
          - `read_preference` (optional): The read preference to use. If
            ``None`` (the default) the :attr:`read_preference` of this
            :class:`MongoClient` is used. See :mod:`~pymongo.read_preferences`
            for options.
          - `write_concern` (optional): An instance of
            :class:`~pymongo.write_concern.WriteConcern`. If ``None`` (the
            default) the :attr:`write_concern` of this :class:`MongoClient` is
            used.
          - `read_concern` (optional): An instance of
            :class:`~pymongo.read_concern.ReadConcern`. If ``None`` (the
            default) the :attr:`read_concern` of this :class:`MongoClient` is
            used.
        """
        return self.__connection.get_database(db_name, codec_options,
                                              read_preference, write_concern,
                                              read_concern)
