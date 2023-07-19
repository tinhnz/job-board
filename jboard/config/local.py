import os

SECRET_KEY = os.getenv('SECRET_KEY')

DATABASE_URI = 'dbname={dbname} user={dbuser} password={dbpass} host={dbhost}'.format(
    dbname=os.environ.get('DBNAME'),
    dbuser=os.environ.get('DBUSER'),
    dbpass=os.environ.get('DBPASS'),
    dbhost=os.environ.get('DBHOST'),
)