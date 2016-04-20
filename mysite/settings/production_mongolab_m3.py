from .production import *

#
# custom production.py settings file to specifically use the mongolab m1 instance

#
# mongo database connection settings
MONGO_SERVER_ADDRESS    = 'ds015781-a0.mlab.com'        #environ.get('MONGO_SERVER_ADDRESS')   # ie: '123.132.123.123'
MONGO_AUTH_DB           = 'admin'                       #environ.get('MONGO_AUTH_DB')          # 'admin'
MONGO_USER              = 'admin'                       #environ.get('MONGO_USER')             # 'admin'
MONGO_PASSWORD          = 'dataden1'                    #environ.get('MONGO_PASSWORD')         # 'dataden1'
MONGO_PORT              =  int(15781)                   #int(environ.get('MONGO_PORT'))        # 27017              cast MONGO_PORT to integer!
MONGO_HOST = 'mongodb://%s:%s@%s:%s/%s' % ( MONGO_USER,
                                            MONGO_PASSWORD,
                                            MONGO_SERVER_ADDRESS,
                                            MONGO_PORT,
                                            MONGO_AUTH_DB )