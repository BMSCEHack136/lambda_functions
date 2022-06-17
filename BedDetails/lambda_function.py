import json
import smtplib
from pymongo import MongoClient


def lambda_handler(event, context):

    _id = event["queryStringParameters"]["id"]
    # _id = "SATY971552"

    client = MongoClient(
        "mongodb+srv://user:user@cluster0.vgvn2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client.get_database("MediCare")
    table = db.Bed

    bed_data = list(table.find({"Hospital_id": _id}))
    bed_data[0]["_id"] = 1

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Requested-With": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps({"data": bed_data}),
    }
