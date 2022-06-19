import json
from pymongo import MongoClient

import requests
from bs4 import BeautifulSoup
import html5lib


newsCat = {
    "Latest": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen",
    "Medicine": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE/sections/CAQiRENCQVNMUW9JTDIwdk1HdDBOVEVTQldWdUxVZENJZzRJQkJvS0NnZ3ZiUzh3TkhOb015b0tFZ2d2YlM4d05ITm9NeWdBKikIAColCAoiH0NCQVNFUW9JTDIwdk1HdDBOVEVTQldWdUxVZENLQUFQAVAB?hl=en-IN&gl=IN&ceid=IN%3Aen",
    "HealthCare": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE/sections/CAQiR0NCQVNMd29JTDIwdk1HdDBOVEVTQldWdUxVZENJZzhJQkJvTENna3ZiUzh3TVcxM01uZ3FDeElKTDIwdk1ERnRkeko0S0FBKikIAColCAoiH0NCQVNFUW9JTDIwdk1HdDBOVEVTQldWdUxVZENLQUFQAVAB?hl=en-IN&gl=IN&ceid=IN%3Aen",
    "MentalHealth": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE/sections/CAQiR0NCQVNMd29JTDIwdk1HdDBOVEVTQldWdUxVZENJZzhJQkJvTENna3ZiUzh3TTNnMk9XY3FDeElKTDIwdk1ETjROamxuS0FBKikIAColCAoiH0NCQVNFUW9JTDIwdk1HdDBOVEVTQldWdUxVZENLQUFQAVAB?hl=en-IN&gl=IN&ceid=IN%3Aen",
    "Nutrition": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE/sections/CAQiRENCQVNMUW9JTDIwdk1HdDBOVEVTQldWdUxVZENJZzRJQkJvS0NnZ3ZiUzh3TldScVl5b0tFZ2d2YlM4d05XUnFZeWdBKikIAColCAoiH0NCQVNFUW9JTDIwdk1HdDBOVEVTQldWdUxVZENLQUFQAVAB?hl=en-IN&gl=IN&ceid=IN%3Aen",
    "Fitness": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE/sections/CAQiW0NCQVNQZ29JTDIwdk1HdDBOVEVTQldWdUxVZENJZzhJQkJvTENna3ZiUzh3TWpkNE4yNHFHZ29ZQ2hSR1NWUk9SVk5UWDFORlExUkpUMDVmVGtGTlJTQUJLQUEqKQgAKiUICiIfQ0JBU0VRb0lMMjB2TUd0ME5URVNCV1Z1TFVkQ0tBQVABUAE?hl=en-IN&gl=IN&ceid=IN%3Aen",
}


def googleNewsData(URL):

    soup = BeautifulSoup(requests.get(URL).content, "html5lib")

    division = soup.find_all("div", class_="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc")

    newsData = []
    count, errorCount = 0, 0
    for div in division:

        try:

            tempNewsData = dict()
            tempNewsData["title"] = div.find("h3").text
            tempNewsData["imgUrl"] = (
                div.find("a").find("img")["srcset"].split("1x")[-1][2:-3]
            )
            tempNewsData["url"] = "https://news.google.com/" + div.find("a")["href"][2:]
            tempNewsData["time"] = (
                div.find("div", class_="QmrVtf RD0gLb kybdz").find("time").text
            )
            tempNewsData["publisher"] = (
                div.find("div", class_="QmrVtf RD0gLb kybdz").find("a").text
            )

            newsData.append(tempNewsData)

        except:
            errorCount += 1
            pass

    return newsData


client = MongoClient(
    "mongodb+srv://user:user@cluster0.vgvn2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = client.get_database("MediCare")
records = db.News


def lambda_handler(event, context):

    records.drop()
    for topic in newsCat:
        print(topic)
        news = dict()
        news[topic] = googleNewsData(newsCat[topic])

        records.insert_one(news)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Requested-With": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": {"message": "news updated!!", "keys": news.keys()},
    }


# lambda_handler(3, 3)
