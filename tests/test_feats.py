import unittest
from src.features.build_features import build_base_df


class FeaturesTest(unittest.TestCase):
    @unittest.skip
    def test_base_feats(self):
        df = build_base_df()
        self.assertIsNotNone(df)
        fantasy_cols = ("total_passing_twopt", "total_rushing_twopt", "total_rushing_yds", "total_rushing_tds",
                        "total_rec_yds", "total_rec_tds", "total_passing_yds", "total_passing_tds", "total_fum_lost",
                        "total_ints", "over_300", "over_400", "avg_fantasy")
        assert set(fantasy_cols).issubset(df.columns.values)

    def test_z_score(self):
        pass

    def test_extra_pts(self):
        """
        Check if the over 300, 400 yard (or 100/200 yards for receivers/rushers) are correct using
        the current range of seasons. Will modify once database is updated with more recent stats.
        """
        pass
