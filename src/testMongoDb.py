from pymongo import MongoClient
import os

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://' + process.env.DB_CONTAINER + "/" +  os.environ.get('API_PASSWORD')')
db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
print(serverStatusResult)