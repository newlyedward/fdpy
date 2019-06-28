

from fdpy.processor.utility import PROCESSOR_DIR


class MongoClient:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_engine(cls, engine):
        load_dotenv(str(PROCESSOR_DIR / '.env'))
        MONGODB_URI = os.environ.get('MONGODB_URI')
        MONGODB_PORT = os.environ.get('MONGODB_PORT')
        return cls(
            mongo_uri=engine.settings.get('MONGO_URI'),
            mongo_db=engine.settings.get('MONGO_DATABASE', 'items')
        )

    def start_engine(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_engine(self):
        self.client.close()
