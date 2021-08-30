import functools
import ffmdl.common as common
import re
import collections
import json
import logging
from multiprocessing import Pool
import traceback

import bs4
import redis
import requests
import tqdm
import os
from dotenv import load_dotenv


# logging config
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
dc_logger = logging.getLogger("dc_logger")
dc_logger.setLevel(logging.INFO)


def init():
    load_dotenv()
    host = os.getenv("redis_host")
    port = os.getenv("redis_port")
    db = redis.Redis(host=host, port=port)
    return db


def create_url(team_name):
    team_name = common.exception_dict.get(team_name, team_name)
    return "https://www.{}.com/team/depth-chart".format(team_name)


def create_depth_chart(team_name, team_db):
    """
    function_name: create_depth_chart
    purpose: gets the depth chart from the team website for a specified team
    params: team_name - the name of the team to retrieve
            team_db - database for depth charts (redis instance)
    return: dict containing positions as keys and a list of player names as values
    """

    # open URL and get response
    dc_logger.info("Team name: %s", team_name)
    url = create_url(team_name)

    dc_logger.info("URL: %s", url)
    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as exception:
        response = exception.response

        # page not found error
        if response.status_code == 404:
            dc_logger.error("URL not found! %s", url)
        else:
            dc_logger.error("Error requesting url! %s", url)
            raise

    dc_logger.info("response: %d", response.status_code)
    soup = bs4.BeautifulSoup(response.text, "lxml")

    # return dictionary matching player lists and positions
    try:
        depth_chart = make_player_dict(soup.tbody.text)
    except AttributeError:
        dc_logger.error("%s don't have depth chart available. Check again later.", team_name)
        return None

    if depth_chart:
        dc_logger.info("inserting depth-chart into redis")
        team_db.set(team_name, json.dumps(depth_chart))
    return depth_chart


def make_player_dict(player_list):
    """
    function_name: make_player_dict
    purpose: create a player dict mapping the position to a list of player names
    params: @player_list: takes a string of positions followed by player names separated by \\n
            "WR1\nPlayer1\nPlayer2\nWR2\n..."
    return: dictionary object containing position -> player_list mappings
    """
    positions = ('WR', 'LWR', 'RWR', 'WR1', 'WR2', 'LT', 'LG', 'C', 'RG', 'RT', 'TE', 'QB', 'RB', 'SE', 'FL', 'FB')

    value = ""
    name_list = []
    position = ""
    player_dict = collections.defaultdict(list)

    try:
        table_body = re.sub(" +", " ", player_list.strip())
        player_list = re.sub("\n+", "\n", table_body)
        player_list = re.sub("\n \n", "\n", player_list)
    except AttributeError:
        traceback.print_exc()
        raise

    # iterate through each character in input string
    for char in player_list:

        # if we reached a newline character, we know we reached either the end of a name or position
        if char == '\n':

            # check if the value is a position or a player name
            pos_check = "".join(value.split())
            if pos_check in positions:

                # check to see if this is the first position in the string
                if not position:
                    position = pos_check

                # if it's NOT the first position string encountered, and we have a non-empty list of players
                # then copy the list (otherwise its a reference to the same list), and then place it in dictionary
                if position and len(name_list) > 0:
                    player_dict[position] += name_list[:]
                    position = pos_check
                    name_list.clear()
            else:
                if value:       # avoid inserting empty string
                    name_list.append(value)
            value = ""
        elif char == '\r':
            continue
        else:
            value += char

    if position and len(name_list) > 0:
        if value:
            name_list.append(value)
        player_dict[position] = name_list[:]

    return player_dict


def mt_update(team_db):
    populate_db = functools.partial(create_depth_chart, team_db=team_db)
    with Pool(4) as pool:
        list(tqdm.tqdm(pool.imap(populate_db, common.team_names), total=len(common.team_names)))


if __name__ == '__main__':
    depth_chart_db = init()
    mt_update(depth_chart_db)
