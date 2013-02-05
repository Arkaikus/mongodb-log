# -*- coding: utf-8 *-*
import logging
import getpass
from datetime import datetime
from socket import gethostname
from bson import InvalidDocument

try:
    from pymongo import MongoClient as Connection
except ImportError:
    from pymongo import Connection


class MongoFormatter(logging.Formatter):
    def format(self, record):
        """Format exception object as a string"""
        data = record.__dict__.copy()

        if record.args:
            record.msg = record.msg % record.args

        data.update(
            username=getpass.getuser(),
            time=datetime.now(),
            host=gethostname(),
            message=record.msg,
            args=tuple(unicode(arg) for arg in record.args)
        )
        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])
        return data


class MongoHandler(logging.Handler):
    """ Custom log handler

    Logs all messages to a mongo collection. This  handler is
    designed to be used with the standard python logging mechanism.
    """

    @classmethod
    def to(cls, collection, db='mongolog', host='localhost', port=None,
        username=None, password=None, level=logging.NOTSET):
        """ Create a handler for a given  """
        return cls(collection, db, host, port, username, password, level)

    def __init__(self, collection, db='mongolog', host='localhost', port=None,
        username=None, password=None, level=logging.NOTSET):
        """ Init log handler and store the collection handle """
        logging.Handler.__init__(self, level)
        if (type(collection) == str):
            connection = Connection(host, port)
            if username and password:
                connection[db].authenticate(username, password)
            self.collection = connection[db][collection]
        else:
            self.collection = collection
        self.formatter = MongoFormatter()

    def emit(self, record):
        """ Store the record to the collection. Async insert """
        try:
            self.collection.insert(self.format(record))
        except InvalidDocument, e:
            logging.error("Unable to save log record: %s", e.message,
                exc_info=True)
