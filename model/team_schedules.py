import json
import logging
import requests
import re
import redis
import time

from bs4 import BeautifulSoup

# import mongodb_ops

FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
sched_logger = logging.getLogger(__name__)
sched_logger.setLevel(logging.INFO)

with open("consts.json", "r") as fp:
    team_consts = json.loads(fp.read())
db = redis.Redis("localhost", 6379, db=1)


def create_url(team_name, ending):
    if team_name in team_consts['EXCEPTION_DICT']:
        team_name = team_consts['EXCEPTION_DICT'][team_name]
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

    sched_logger.info("teamname: {}".format(teamname))
    url = create_url(teamname, "schedule")
    sched_logger.info("url: {}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pre_reg = soup.find_all(class_=season_type)
        seas_types = []
        for item in pre_reg:
            span = item.find("span")
            if span:
                text = span.text.strip()
                if text == "REGULAR SEASON" or text == "PRESEASON":
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
        else:
            return team_sched[:17]
    else:
        sched_logger.error("STATUS CODE: {}".format(response.status_code))
        sched_logger.error("Try again later for team: {}".format(teamname))


def insert_sched(schedule_dict):
    """
    :function_name: insert_sched
    :param schedule_bson: bson obj of team's schedule
    :return: None
    """

    for team in schedule_dict.keys():
        db.set(team, json.dumps(schedule_dict[team]))


def update_scheds():
    sched_dict = {}
    for team_name in team_consts['TEAM_NAMES']:
        sched_dict[team_name] = scrape_schedule(team_name)
        time.sleep(2)
    sched_logger.info("schedule_dict: {}".format(sched_dict))
    insert_sched(sched_dict)


if __name__ == "__main__":
    update_scheds()
    # sched_logger.info(scrape_schedule("patriots"))
