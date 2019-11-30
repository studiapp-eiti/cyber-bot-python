from studia3.studia_requests import Studia3Client
import json
import datetime
# from studia3_mysql import db_handler
import logging
# def obtain_credentials_for_studia3(path):
#     with open(path, "r") as f:
#         return json.load(f)["studia3"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('sample2.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(streamHandler)
l = [1,2]
logger.debug("this is a debugging message")
logger.info("this is an informational message")
logger.warning("this is a warning message")
logger.error("this is an error message")
logger.critical(f"this is a critical messageg {l}")

# if __name__ == "__main__":
#     database = db_handler.Db()
#     maintainer_objects = database.get_cookies()
#     for maintainer in maintainer_objects:
#         exp_date = maintainer[2]
#         id = maintainer[0]
#         if (exp_date - datetime.datetime.now()).seconds <= 0:
#             database.update_cookies(id)
#         elif maintainer[1] is not None:  # 0 - maintainer Id, 1 - cookie, 2 - exp date
#             client = Studia3Client(maintainer[1])
#             new_exp_date = client.is_logged_in()
#             database.update_cookies(id, new_exp_date)
