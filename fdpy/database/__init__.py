import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

from fdpy.processor.utility import PROCESSOR_DIR

load_dotenv(str(PROCESSOR_DIR / '.env'))

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_PORT = os.environ.get('MONGODB_PORT')

DATA_COLLECTOR = os.environ.get('DATA_COLLECTOR')
COLLECTOR_PWD = os.environ.get('COLLECTOR_PWD')
DATA_ANALYST = os.environ.get('DATA_ANALYST')
ANALYST_PWD = os.environ.get('ANALYST_PWD')


def connect(db, username=DATA_COLLECTOR, password=COLLECTOR_PWD, host=MONGODB_URI, port=MONGODB_PORT):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://{}:{}@{}:{}/{}'.format(username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]
