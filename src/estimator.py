from math import pow


def converter(data):
    """
    Convert all periods to days
    """
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
        # Challenge 1
        impact["currentlyInfected"] = int(data["reportedCases"]) * 10
        impact["infectionsByRequestedTime"] = int((int(impact["currentlyInfected"]) * pow(2,
                                                                                      (converter(data) / 3) // 1)) // 1)
        severeImpact["currentlyInfected"] = int(data["reportedCases"]) * 50
        severeImpact["infectionsByRequestedTime"] = int((int(severeImpact["currentlyInfected"]) * pow(2, (
                converter(data) / 3) // 1)) // 1)

        # Start of Challenge 2
        impact["severeCasesByRequestedTime"] = int((0.15 * impact["infectionsByRequestedTime"]) // 1)
        impact["hospitalBedsByRequestedTime"] = int((((int(data.get("totalHospitalBeds"))) * 0.35) - impact[
            "severeCasesByRequestedTime"]))

        severeImpact["severeCasesByRequestedTime"] = int((0.15 * severeImpact["infectionsByRequestedTime"]) // 1)
        severeImpact["hospitalBedsByRequestedTime"] = int((((int(data.get("totalHospitalBeds"))) * 0.35) -
                                                       severeImpact["severeCasesByRequestedTime"]))

        # End of Challenge 2

        # Challenge 3
        impact["casesForICUByRequestedTime"] = int((0.05 * impact["infectionsByRequestedTime"]) // 1)
        impact["casesForVentilatorsByRequestedTime"] = int((0.02 * impact["infectionsByRequestedTime"]) // 1)
        impact["dollarsInFlight"] = int(((impact["infectionsByRequestedTime"] * data["region"]["avgDailyIncomeInUSD"] * \
                                          data["region"]["avgDailyIncomePopulation"]) / converter(data)) // 1)

        severeImpact["casesForICUByRequestedTime"] = int((0.05 * severeImpact["infectionsByRequestedTime"]) // 1)
        severeImpact["casesForVentilatorsByRequestedTime"] = int((0.02 * severeImpact["infectionsByRequestedTime"]) // 1)
        severeImpact["dollarsInFlight"] = int(((severeImpact["infectionsByRequestedTime"] * data["region"][
            "avgDailyIncomeInUSD"] * data["region"]["avgDailyIncomePopulation"]) / converter(data)) // 1)
        # End of challenge 3

    else:
        raise TypeError("Type incorrect !")

    return {
        "data": data,
        "impact": impact,
        "severeImpact": severeImpact
    }