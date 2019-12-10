import json
from scrappers import scrapper_creator
import pathlib
from dotenv import load_dotenv


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


load_dotenv()

if __name__ == "__main__":
    with open("scrappers/config.json") as f:
        data = json.load(f, encoding="UTF-8")
    scrapper = None

    if data:
        course = data["courses"][0]
        id_ = course["id"]
        for scrapper_content in course["scrappers"]:
            scrapper = scrapper_creator.ScrapperCreator.from_json(scrapper_content, id_)
            scrapper.iter_urls()

for base_url, child_urls in scrapper.data.items():
    print(f"{bcolors.FAIL}Subpath content for url: {base_url} {bcolors.ENDC}")
    for path, content in child_urls.items():
        print(f"{bcolors.WARNING}Path name: {path[1]} \nurl: {path[0]}  {bcolors.ENDC}")
        print(content)
