from database import MongoDBConnection
from dashboard import plot_dashboard

MONGODB_URL = "<MONGO_URL>"


if __name__ == '__main__':
    with MongoDBConnection(MONGODB_URL) as conn:
        print("Connected...")
        conn.get_stats()
        conn.get_databases()
        print("MongoDB version: %s"%conn.version)
        print("Databases: %s"%conn.databases)
        print("Storage Size: %s MB"%(conn.storageSize))
        plot_dashboard(conn.databases, conn.dbs, conn.collections)
       