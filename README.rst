MongoLog: Simple python logging handler for MongoDB.
=======================================================

:Info: MongoDB python logging handler. Python centralized logging made easy.
:Author: `Andrei Savu`_
:Maintainer: `Arkaikus`_

Setup
-----

Install the package with:

    pip install -I git+https://github.com/Arkaikus/mongolog.git

Usage
-----

MongoHandler will create a new database and collection if they do not exist.

>>> import logging
>>> from mongolog.handlers import MongoHandler
>>>
>>> log = logging.getLogger('demo')
>>> log.setLevel(logging.DEBUG)
>>> log.addHandler(MongoHandler('mongolog','log', host='localhost', port=27017, username='user', password='pass'))
>>>
>>> log.debug('Some message')


Check the samples folder for more details.


Why centralized logging?
------------------------

* Easy troubleshouting:
    * Having the answers to why? quickly and accurately.
    * For troubleshouting while the system is down.
    * Removed risk of loss of log information.
* Resource tracking.
* Security.


What is MongoDB?
----------------

"MongoDB is a high-performance, open source, schema-free document-oriented
database."

It can eficiently store arbitrary JSON objects. You can read more at
`MongoDB website`_.


Why MongoDB is great for logging?
---------------------------------

* MongoDB inserts can be done asynchronously.
* Old log data automatically LRU's out thanks to capped collections.
* It's fast enough for the problem.
* Document-oriented / JSON is a great format for log information.

Read more about this subject on the `MongoDB blog`_.


Have fun!


.. _Andrei Savu: https://github.com/andreisavu
.. _Arkaikus: https://github.com/arkaikus
.. _MongoDB website: http://www.mongodb.org
