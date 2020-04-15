from src.estimator import covid19ImpactEstimator
import unittest

data = {
    "region": {
        "name": "Africa",
        "avgAge": 19.7,
        "avgDailyIncomeInUSD": 5,
        "avgDailyIncomePopulation": 0.71
    },
    "periodType": "days",
    "timeToElapse": 3,
    "reportedCases": 674,
    "population": 66622705,
    "totalHospitalBeds": 1380614
}


class TestEstimator(unittest.TestCase):

    def test_output_data_type(self):
        result = covid19ImpactEstimator(data)
        self.assertIsInstance(result, dict)

    def test_challenge_1(self):
        result = covid19ImpactEstimator(data)

        self.assertEqual(result["impact"]["currentlyInfected"], 6740)
        self.assertEqual(result["severeImpact"]["currentlyInfected"], 33700)
        self.assertEqual(result["impact"]["infectionsByRequestedTime"], 13480)
        self.assertEqual(result["severeImpact"]["infectionsByRequestedTime"], 67400)


if __name__ == "__main__":
    unittest.main()
