import json
import smtplib
from pymongo import MongoClient


def lambda_handler(event, context):

    _id = event["queryStringParameters"]["id"]
    _pass = event["queryStringParameters"]["pass"]

    client = MongoClient(
        "mongodb+srv://user:user@cluster0.vgvn2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client.get_database("MediCare")
    table = db.Hospital

    hos_data = list(table.find({"_id": _id}))

    if len(hos_data) == 0:

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "X-Requested-With": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"message": "notReg"}),
        }

    else:

        if hos_data[0]["password"] == _pass:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "X-Requested-With": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps({"message": "sucess"}),
            }

        else:

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "X-Requested-With": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps({"message": "invalidPass"}),
            }
