import json
from scrappers import scrapper_creator
import pathlib
from dotenv import load_dotenv
import logging


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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('scrapper.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(streamHandler)

if __name__ == "__main__":
    with open("scrappers/config.json") as f:
        data = json.load(f, encoding="UTF-8")
    scrapper = None

    if data:
        try:
            scrapper_config = data["global_configuration"]
            for course in scrapper_config["courses"]:
                for scrapper_config in course:
                    scrapper = scrapper_creator.ScrapperCreator.from_json(scrapper_config, course["id"])

        except KeyError as e:
            logger.exception(e)

        # course = data["courses"][0]
        # id_ = course["id"]
        # for scrapper_content in course["scrappers"]:
        #     scrapper = scrapper_creator.ScrapperCreator.from_json(scrapper_content, id_)
        #     scrapper.iter_urls()

for base_url, child_urls in scrapper.data.items():
    print(f"{bcolors.FAIL}Subpath content for url: {base_url} {bcolors.ENDC}")
    for path, content in child_urls.items():
        print(f"{bcolors.WARNING}Path name: {path[1]} \nurl: {path[0]}  {bcolors.ENDC}")
        print(content)
