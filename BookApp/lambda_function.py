import json
import smtplib
from pymongo import MongoClient
import random


def lambda_handler(event, context):

    _id = event["queryStringParameters"]["hId"]
    pid = event["queryStringParameters"]["pId"]
    time = event["queryStringParameters"]["tim"]
    date = event["queryStringParameters"]["date"]

    client = MongoClient(
        "mongodb+srv://user:user@cluster0.vgvn2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    db = client.get_database("MediCare")
    table = db.Appointment
    print(list(table.find()))

    data = {
        "_id": _id[:4] + pid[:5],
        "Hospital_id": _id,
        "Patient_id": pid,
        "Date": date,
        "Time": time,
        "resolve": "0",
    }

    table.insert_one(data)
    # print(table.find())

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Requested-With": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps({"data": "updated"}),
    }
