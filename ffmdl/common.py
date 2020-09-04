"""
Filename: common.py
Author: David Lin

Purpose: For all common constants that are used across files/functionalities.
Include things like team names, teams with exceptions to url scheme, position names, divisions, etc.
"""

import logging


team_names = ["texans", "titans", "colts", "jaguars",
              "ravens", "browns", "bengals", "steelers",
              "raiders", "chiefs", "chargers", "broncos",
              "patriots", "dolphins", "bills", "jets",
              "cowboys", "eagles", "redskins", "giants",
              "bears", "lions", "packers", "vikings",
              "falcons", "saints", "panthers", "buccaneers",
              "seahawks", "niners", "rams", "cardinals"]

exception_dict = {
        "texans": "houstontexans",
        "titans": "titansonline",
        "ravens": "baltimoreravens",
        "browns": "clevelandbrowns",
        "broncos": "denverbroncos",
        "dolphins": "miamidolphins",
        "bills": "buffalobills",
        "jets": "newyorkjets",
        "cowboys": "dallascowboys",
        "eagles": "philadelphiaeagles",
        "bears": "chicagobears",
        "lions": "detroitlions",
        "falcons": "atlantafalcons",
        "saints": "neworleanssaints",
        "niners": "49ers",
        "rams": "therams",
        "cardinals": "azcardinals"
    }

position_names = ["WR", "LWR", "RWR", "WR1", "WR2", "LT", "LG", "C", "RG", "RT", "TE",
                  "QB", "RB", "SE", "FL", "FB", "RB2"]

skill_pos = ("QB", "RB", "TE", "WR")

pos_target_map = {
    'TE': 'total_rec_yds',
    'WR': 'total_rec_yds',
    'RB': 'total_rushing_yds',
    'QB': 'total_passing_yds',
}

divisions = {
    "nfc": {
        "north": ["vikings", "packers", "lions", "bears"],
        "south": ["buccaneers", "panthers", "falcons", "saints"],
        "east": ["cowboys", "eagles", "washington", "giants"],
        "west": ["49ers", "seahawks", "rams", "cardinals"]
    },
    "afc": {
        "north": ["patriots", "jets", "dolphins", "bills"],
        "south": ["colts", "texans", "titans", "jaguars"],
        "east": ["ravens", "browns", "steelers", "bengals"],
        "west": ["raiders", "broncos", "chiefs", "chargers"]
    }
}

teams = (
    # NFC North
    "MIN", "GB", "DET", "CHI",

    # NFC South
    "TB", "CAR", "ATL", "NO",

    # NFC West
    "SF", "SEA", "STL", "ARI",

    # NFC East
    "DAL", "NYG", "WAS", "PHI",

    # AFC South
    "IND", "HOU", "JAC", "TEN",

    # AFC East
    "BAL", "CLE", "PIT", "CIN",

    # AFC West
    "OAK", "DEN", "KC", "SD",

    # AFC North
    "NE", "NYJ", "MIA", "BUF"
)

pos_cols = {
    'WR': ["games_played", "total_rec_yds", "total_rec_tds", "total_recs", "total_targets"],
    'TE': ["games_played", "total_rec_yds", "total_rec_tds", "total_recs", "total_targets"],
    'RB': ["games_played", "total_rushing_yds", "total_rushing_tds", "total_rushing_att"],
    'QB': ["games_played", "total_passing_yds", "total_passing_tds", "total_passing_att"],
}

model_types = ("lin_reg", "svm", "nn", "decision_tree", "random_forest")

# Number Constants
TOTAL_GAMES_PER_SEASON = 16

# 2pt pass, 2pt rush, rush yds, rush td, pass yd, pass td, fumble lost, int, >300, >400
# TODO: >100, >200 receiving/rushing
pt_multipliers = (2, 2, 0.1, 6, 0.1, 6, 0.04, 4, -2, -2, 1, 2)


def get_logger(name):
    formatter = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    return logging.getLogger(name)
