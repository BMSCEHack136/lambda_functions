import json
from pymongo import MongoClient



client = MongoClient("mongodb+srv://user:user@cluster0.vgvn2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('CollegeConnect')
records = db.News

print(list(records.find({}))[0])
def lambda_handler(event, context):
    data = list(records.find({}))[0]
    
    return {
        "statusCode": 200,
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "X-Requested-With" : "*",
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Methods" : "OPTIONS,POST,GET"
        },
        "body": json.dumps({k:v for k,v in data.items() if k!="_id"})
    }