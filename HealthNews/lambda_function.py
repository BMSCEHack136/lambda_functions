import json
import smtplib
from pymongo import MongoClient


def lambda_handler(event, context):

    client = MongoClient(
        "mongodb+srv://user:user@cluster0.vgvn2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client.get_database("MediCare")
    table = db.News
    #     print(list(table.find()))

    data = list(table.find())

    for i in data:
        del i["_id"]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Requested-With": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps({"data": data}),
    }
