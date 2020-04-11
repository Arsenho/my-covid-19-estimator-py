from math import pow


def converter(data):
    days = None
    if isinstance(data, dict):
        if data.get("periodType") == "days":
            days = data.get("timeToElapse")
        elif data.get("periodType") == "weeks":
            days = data.get("timeToElapse") * 7
        elif data.get("periodType") == "months":
            days = data.get("timeToElapse") * 30
        return days
    else:
        raise TypeError


def estimator(data):
    """
    data: {},  the input data you got
    impact: {},  your best case estimation
     severeImpact: {} your severe case estimation
    """
    impact = {}
    severeImpact = {}
    if isinstance(data, dict):

        impact["currentlyInfected"] = int(data["reportedCases"]) * 10
        impact["infectionsByRequestedTime"] = (int(impact["currentlyInfected"]) * pow(2,
                                                                                      (converter(data) / 3) // 1)) // 1
        impact["severeCasesByRequestedTime"] = (0.15 * impact["infectionsByRequestedTime"]) // 1
        impact["hospitalBedsByRequestedTime"] = ((((int(data.get("totalHospitalBeds"))) * 0.925) * 0.35) - impact[
            "severeCasesByRequestedTime"]) // 1
        impact["casesForICUByRequestedTime"] = (0.05 * impact["infectionsByRequestedTime"]) // 1
        impact["casesForVentilatorsByRequestedTime"] = (0.02 * impact["infectionsByRequestedTime"]) // 1
        impact["dollarsInflight"] = (impact["infectionsByRequestedTime"] * data["region"]["avgDailyIncomeInUSD"] * \
                                     data["region"]["avgDailyIncomePopulation"] * converter(data)) // 1

        severeImpact["currentlyInfected"] = int(data["reportedCases"]) * 50
        severeImpact["infectionsByRequestedTime"] = (int(severeImpact["currentlyInfected"]) * pow(2, (
                converter(data) / 3) // 1)) // 1
        severeImpact["severeCasesByRequestedTime"] = (0.15 * severeImpact["infectionsByRequestedTime"]) // 1
        severeImpact["hospitalBedsByRequestedTime"] = ((((int(data.get("totalHospitalBeds"))) * 0.925) * 0.35) -
                                                       severeImpact["severeCasesByRequestedTime"]) // 1
        severeImpact["casesForICUByRequestedTime"] = (0.05 * severeImpact["infectionsByRequestedTime"]) // 1
        severeImpact["casesForVentilatorsByRequestedTime"] = (0.02 * severeImpact["infectionsByRequestedTime"]) // 1
        severeImpact["dollarsInflight"] = (severeImpact["infectionsByRequestedTime"] * data["region"][
            "avgDailyIncomeInUSD"] * data["region"]["avgDailyIncomePopulation"] * converter(data)) // 1

    else:
        raise TypeError("Type incorrect !")

    return {
        "data": data,
        "impact": impact,
        "severeImpact": severeImpact
    }

#if __name__ == "__main__":
#   data = {
#        "region": {
#            "name": "Africa",
#            "avgAge": 19.7,
#            "avgDailyIncomeInUSD": 5,
#            "avgDailyIncomePopulation": 0.71
#        },
#        "periodType": "days",
#        "timeToElapse": 3,
#        "reportedCases": 674,
#        "population": 66622705,
#        "totalHospitalBeds": 1380614
#   }
#   for key, value in estimator(data).items():
#       print("{}:{}".format(key, value))