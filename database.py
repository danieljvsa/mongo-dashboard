from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, url):
        self.url = url
        self.connection = None
        self.databases = []
        self.version = "" 
        self.db_unauthorized = ["local", "admin"]
        self.dbs = {}
        self.collections = {} 
        self.storageSize = 0

    def __enter__(self):
        self.connection = MongoClient(self.url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def get_stats(self):
        for name in self.connection.list_database_names():
            if(name in self.db_unauthorized): continue
            self.databases.append(name)
        self.version = self.connection.server_info()["version"]
    
    def get_databases(self):
        try:
            for db in self.databases:
                if(db in self.db_unauthorized): continue
                db_command = self.connection[db]
                db_info = db_command.command('dbStats')
                
                if(db not in self.dbs): self.dbs[db] = {}
                
                self.dbs[db]['collectionsNumber'] = db_info['collections']
                self.dbs[db]['storageSize'] = db_info['storageSize']
                self.dbs[db]['indexes'] = db_info['indexes']
                self.dbs[db]['documents'] = db_info['objects'] 
                self.dbs[db]['collections'] = db_command.list_collection_names()
                self.storageSize += db_info['storageSize']

                for collection in self.dbs[db]['collections']:
                    if(db not in self.collections): self.collections[db] = {}
                    if(collection not in self.collections[db]): self.collections[db][collection] = {}
                    if('indexes' not in self.collections[db][collection]): self.collections[db][collection]['indexes'] = []
                    
                    for index in db_command[collection].index_information():
                        self.collections[db][collection]['indexes'].append(index)
                    
                    self.collections[db][collection]['indexesNumber'] = len(self.collections[db][collection]['indexes'])
                    self.collections[db][collection]['documents'] = db_command[collection].count_documents({})
                    self.collections[db][collection]['storageSize'] = db_command.command('collstats', collection)['storageSize']
                    self.dbs[db]['storageSize'] += self.collections[db][collection]['storageSize'] 
                    self.collections[db][collection]['storageSize'] = round(self.collections[db][collection]['storageSize'] / 1048576, 3)
            
            self.dbs[db]['storageSize'] = round(self.dbs[db]['storageSize'] / 1048576, 3)  
            self.storageSize = round(self.storageSize / 1048576, 3)
        except Exception as error:
            print("database/MongoClientDB/get_databases: %s"%error)
            
    def print_data(self):
        print("Databases    ")
        print(self.dbs)
        print('Collections:   ')
        print(self.collections)