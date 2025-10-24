from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import redis
import schedule
import time
import argparse

from selenium.webdriver.firefox.service import Service

from loggers.NoDuplicateLogger import no_duplicate_logger
from util import EmailUtils

parser = argparse.ArgumentParser()
parser.add_argument("--redis-host", type=str, default="", help="Redis host address")
parser.add_argument("--redis-port", type=int, default=6379, help="Redis port number")
parser.add_argument("--gmail-username", type=str, default="", help="Gmail username for sending email")
parser.add_argument("--gmail-password", type=str, default="", help="Gmail password for sending email")
parser.add_argument("--to-email", type=str, default="", help="Receiver's email")
parser.add_argument("--poll-interval", type=str, default="", help="Polling interval in seconds")
args = parser.parse_args()

options = Options()
service = Service()
redis_instance = redis.Redis(host=args.__getattribute__("redis_host"), port=args.__getattribute__("redis_port"))


def invoke_isro():
    global cached_next_isro_mission, next_isro_mission
    cached_next_isro_mission_bytes = redis_instance.get("next_isro_mission")
    if cached_next_isro_mission_bytes:
        cached_next_isro_mission = cached_next_isro_mission_bytes.decode('utf-8')

    options.add_argument("--headless")
    # Uncomment below line for docker build
    service.path = "/usr/local/bin/geckodriver"
    driver = webdriver.Firefox(options=options, service=service)
    driver.set_page_load_timeout(10)

    try:
        driver.get("https://lvg.shar.gov.in/VSCREGISTRATION/index.jsp")
        mission_div_element = driver.find_element(By.XPATH, "//*[@id=\"dividleft\"]")
        mission_text_elements = mission_div_element.find_elements(By.TAG_NAME, "font")
        texts = [mission_text_element.text for mission_text_element in mission_text_elements]
        next_isro_mission = ", ".join(texts)

        if cached_next_isro_mission != next_isro_mission:
            mission_div_element.screenshot("mission.png")
            EmailUtils.sendMail(next_isro_mission,
                                "ISRO has a new launch scheduled",
                                args.__getattribute__("gmail_username"),
                                args.__getattribute__("gmail_password"),
                                args.__getattribute__("to_email"))
            cache_data(next_isro_mission)
            cached_next_isro_mission = next_isro_mission
        else:
            no_duplicate_logger.info("No change in next ISRO mission")
    except Exception as e:
        no_duplicate_logger.info("Error occurred while fetching ISRO mission data")
        raise e
    finally:
        driver.quit()

    return next_isro_mission


def cache_data(data):
    no_duplicate_logger.info(f"Setting next_isro_mission cache value to {data}")
    redis_instance.set("next_isro_mission", data)


try:
    seconds = int(args.__getattribute__("poll_interval"))
    no_duplicate_logger.info(f"Starting scheduler to invoke ISRO every {seconds} seconds")
    schedule.every(seconds).seconds.do(invoke_isro)
    while True:
        schedule.run_pending()
        time.sleep(1)
except (KeyboardInterrupt, InterruptedError):
    no_duplicate_logger.info("Stopping scheduler")
