from database import MongoDBConnection
from dashboard import plot_dashboard, plot_instance, plot_collections

if __name__ == '__main__':
    db_instance = plot_instance()
    if(db_instance):
        with MongoDBConnection(db_instance) as conn:
            print("Connected...")
            conn.get_stats()
            conn.get_databases()
            print("MongoDB version: %s"%conn.version)
            print("Databases: %s"%conn.databases)
            print("Storage Size: %s MB"%(conn.storageSize))
            database = plot_dashboard(conn.databases, conn.dbs, conn.collections)
            if(database is not '----'):
                plot_collections(database, conn.collections)
        