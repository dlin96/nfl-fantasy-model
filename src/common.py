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
