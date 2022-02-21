# -*- coding: utf-8 *-*
import sys
import getpass
import logging

from bson import InvalidDocument
from datetime import datetime
from pymongo.collection import Collection
from socket import gethostname

from pymongo import MongoClient


if sys.version_info[0] >= 3:
    unicode = str


class MongoFormatter(logging.Formatter):
    def format(self, record):
        """Format exception object as a string"""
        data = record.__dict__.copy()

        if record.args:
            msg = record.msg % record.args
        else:
            msg = record.msg

        data.update(
            username=getpass.getuser(),
            time=datetime.now(),
            host=gethostname(),
            message=msg,
            args=tuple(unicode(arg) for arg in record.args),
        )
        if "exc_info" in data and data["exc_info"]:
            data["exc_info"] = self.formatException(data["exc_info"])
        return data


class MongoHandler(logging.Handler):
    """Custom log handler

    Logs all messages to a mongo collection. This  handler is
    designed to be used with the standard python logging mechanism.
    """

    def __init__(
        self,
        db: str,
        collection: str,
        host="localhost",
        port=27017,
        username=None,
        password=None,
        level=logging.NOTSET,
    ):
        """Init log handler and store the collection handle"""
        logging.Handler.__init__(self, level)
        assert isinstance(db, str), "[db] must be a string"
        assert isinstance(collection, str), "[collection] must be a string"

        connection = MongoClient(host, port)
        database = connection.get_database(db)

        if username and password:
            database.authenticate(username, password)

        if collection in database.list_collection_names():
            self.collection = database[collection]
        else:
            self.collection = database.create_collection(collection, capped=True, size=10000000)

        self.formatter = MongoFormatter()

    def emit(self, record):
        """Store the record to the collection. Async insert"""
        try:
            self.collection.insert_one(self.format(record))
        except InvalidDocument as e:
            logging.error("Unable to save log record: %s", e.message, exc_info=True)
