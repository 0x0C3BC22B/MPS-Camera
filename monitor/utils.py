from mongoengine import connect

def init_mongo_connection(db_name: str = 'ipcamera_db', host: str = 'localhost', port: int = 27017):
    """
    Initialize default MongoDB connection for mongoengine.
    """
    connect(
        db=db_name,
        host=host,
        port=port
    )

