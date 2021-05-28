import json
import src.common as common
import logging
import os
from dotenv import load_dotenv
import time

import requests
import redis

from bs4 import BeautifulSoup


FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
sched_logger = logging.getLogger(__name__)
sched_logger.setLevel(logging.INFO)

def init():
    load_dotenv()
    host = os.getenv("redis_host")
    port = os.getenv("redis_port")
    db_num = os.getenv("db_num")
    db = redis.Redis(host, port, db=db_num)


def create_url(team_name, ending):
    if team_name in common.exception_dict:
        team_name = common.EXCEPTION_DICT[team_name]
    url = "https://www.{}.com/" + ending + "/"
    return url.format(team_name)


def scrape_schedule(teamname):
    """
    function_name: scrape_schedule
    param: teamname - str
    return: list of 17 week regular season including BYE week
    """

    matchups = "nfl-o-matchup-cards"
    # weeks = "nfl-o-matchup-cards__date-info"
    opponent = "nfl-o-matchup-cards__team-full-name"
    season_type = "d3-o-section-title"
    team_sched = []

    sched_logger.info("teamname: %s", teamname)
    url = create_url(teamname, "schedule")
    sched_logger.info("url: %s", url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pre_reg = soup.find_all(class_=season_type)
        seas_types = []
        for item in pre_reg:
            span = item.find("span")
            if span:
                text = span.text.strip()
                if text in ("REGULAR SEASON", "PRESEASON"):
                    seas_types.append(text)

        sched_logger.info(seas_types)
        schedule = soup.find_all(class_=matchups)
        for item in schedule:
            # week = item.find_all(class_=weeks)[0].find("strong").text.strip()
            opp = "BYE"
            if len(item.find_all(class_=opponent)) > 0:
                opp = item.find_all(class_=opponent)[0].text.strip()
            # week = re.match(".*\\s([0-9]+)", week).group(1)
            team_sched.append(opp)

        if seas_types[0] == "PRESEASON":
            return team_sched[-17:]
        return team_sched[:17]
    sched_logger.error("STATUS CODE: %d", response.status_code)
    sched_logger.error("Try again later for team: %s", teamname)
    return None


def insert_sched(schedule_dict):
    """
    :function_name: insert_sched
    :param schedule_dict: bson obj of team's schedule
    :return: None
    """

    for team in schedule_dict.keys():
        db.set(team, json.dumps(schedule_dict[team]))


def update_scheds():
    sched_dict = {}
    for team_name in common.TEAM_NAMES:
        sched_dict[team_name] = scrape_schedule(team_name)
        time.sleep(2)
    sched_logger.info("schedule_dict: %s", sched_dict)
    insert_sched(sched_dict)


if __name__ == "__main__":
    update_scheds()
