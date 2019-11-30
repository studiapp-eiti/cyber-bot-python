import logging
import os
import sys
import datetime
import random
import time
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db import db_connector
from studia3.studia3_mysql import queries
from studia3 import studia_requests
import messenger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('/var/log/cyber_bot/refresh_session_1.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(streamHandler)

if __name__ == "__main__":
    load_dotenv()
    db = db_connector.DBConnector()
    queries = queries.Queries(db)

    maintainers = queries.carry_transaction(queries.get_cookies, False)
    to_be_notified = list()
    for i, maintainer in enumerate(maintainers):
        if maintainer["cookie"] is not None:
            delta = maintainer["expires"].timestamp() - datetime.datetime.now().timestamp()
            m_id = maintainer["maintainer_id"]
            if delta <= 0:
                queries.carry_transaction(lambda: queries.update_cookies(m_id), True)
                to_be_notified.append(m_id)
                logger.info(f"Session expired for id: {m_id}. Inserting null to DB")
            else:
                client = studia_requests.Studia3Client(maintainer["cookie"])
                new_exp_date = client.is_logged_in()
                logger.debug(
                    f"Value of new_exp_date for {m_id} is {datetime.datetime.fromtimestamp(int(new_exp_date))}")
                if new_exp_date is False:
                    queries.carry_transaction(lambda: queries.update_cookies(m_id), True)
                    to_be_notified.append(m_id)
                    logger.debug(f"Cookie expired for {m_id}")
                elif new_exp_date is not None:
                    queries.carry_transaction(lambda: queries.update_cookies(m_id, new_exp_date), True)
                    if i + 1 < len(maintainers):
                        time.sleep(random.randrange(5, 30))
                else:
                    logger.warning("Timeout occurred!")
    if len(to_be_notified) is not 0:
        N = messenger.Notifier(to_be_notified)
        logger.info(f"Sending message to users with ids:{to_be_notified}")
        N.message_session_expired()
