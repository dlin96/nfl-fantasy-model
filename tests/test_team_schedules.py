import unittest
from src.data import team_schedules


class TeamScheduleTest(unittest.TestCase):
    def test_create_url(self):
        url = team_schedules.create_url("bengals", "schedule")
        self.assertEqual(url, "https://www.bengals.com/schedule/")
