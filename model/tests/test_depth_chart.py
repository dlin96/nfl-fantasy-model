import unittest
import pickle
import random
import sys

sys.path.append("model/depth_chart")
import depth_chart


class DepthChartTestCase(unittest.TestCase):

    def test_create_url(self):
        # regular, non-exception team
        url = depth_chart.create_url("bengals")
        self.assertEqual(url, "https://www.bengals.com/team/depth-chart")

        # team in exception dictionary
        self.assertEqual(depth_chart.create_url("texans"), "https://www.houstontexans.com/team/depth-chart")

    @unittest.skip
    def test_make_player_dict(self):
        with open("./test_response.txt", "r") as test_file:
            contents = test_file.read()
            p_dict = depth_chart.make_player_dict(contents)
            with open("ravens_2018.pkl", "rb") as ref_file:
                test_dict = pickle.load(ref_file)
            self.assertEqual(p_dict, test_dict)

    @unittest.skip
    def test_create_depth_chart(self):
        i = random.randrange(0, len(depth_chart.team_names))
        depth_chart.create_depth_chart(depth_chart.team_names[i])


if __name__ == '__main__':
    unittest.main()
