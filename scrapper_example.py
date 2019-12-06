import json
from scrappers import scrapper_creator
import pathlib
from dotenv import load_dotenv
p = pathlib.Path(__file__).parents[1] / ".env"
load_dotenv()

if __name__ == "__main__":
    with open("scrappers/config.json") as f:
        data = json.load(f, encoding="UTF-8")
    scrp = None
    if data:
        course = data["courses"][0]
        id_ = course["id"]
        for content in course["scrappers"]:
            scrp = scrapper_creator.ScrapperCreator.from_json(content, id_)
            scrp.iter_urls()


for d in scrp.data.values():
    e = d.copy()
    print(e.values())