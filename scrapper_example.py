import json
from scrappers.base_scrapper import Scrapper





if __name__ == "__main__":
    with open("config.json") as f:
        data = json.load(f, encoding="UTF-8")

    if data:
        course = data["courses"][0]
        id_ = course["id"]
        for content in course["scrappers"]:
            scrp = Scrapper.from_json(content, id_)