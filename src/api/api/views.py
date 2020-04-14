import time
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer
import json
from .mixins import RequestLogViewMixin

try:
    from src.estimator import estimator
except ImportError:
    print("Import failed")

outputData = None
logs = {}
compteur = 0


def write_logs(log, position):
    global logs
    if isinstance(log, dict) and isinstance(logs, dict):
        logs[position] = log
        logs_json = json.dumps(logs, indent=4)
        return logs_json


def get_logs():
    global logs
    logs = json.loads(logs)


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
                                                                                          (converter(
                                                                                              data) / 3) // 1)) // 1)
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
        severeImpact["casesForVentilatorsByRequestedTime"] = int(
            (0.02 * severeImpact["infectionsByRequestedTime"]) // 1)
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


# Create your views here.
class EstimatorData(RequestLogViewMixin, APIView):
    def get(self, request):
        global compteur, outputData

        if isinstance(request, Request):
            compteur += 1
            if outputData is not None:
                response = Response(
                    outputData,
                    status=status.HTTP_200_OK,
                    content_type='application/json; charset=utf8'
                )
                return response
            else:
                data = {}
                response = Response(
                    data,
                    status=status.HTTP_200_OK,
                    content_type='application/json; charset=utf8'
                )
                return response
        else:
            pass

    def post(self, request):
        global  compteur, outputData
        compteur += 1
        if isinstance(request.data, dict):
            outputData = estimator(request.data)
            if isinstance(outputData, dict):
                response = Response(
                    outputData,
                    status=status.HTTP_200_OK,
                    content_type='application/json; charset=utf8'
                )
                return response
            else:
                pass
        else:
            pass


class EstimatorDataXML(RequestLogViewMixin, APIView):
    renderer_classes = (XMLRenderer,)

    def get(self, request):
        global compteur, outputData

        if isinstance(request, Request):
            compteur += 1
            if outputData is not None:
                response = Response(
                    outputData,
                    status=status.HTTP_200_OK,
                    content_type='application/xml; charset=utf8'
                )
                return response
            else:
                data = {}
                response = Response(
                    data,
                    status=status.HTTP_200_OK,
                    content_type='application/xml; charset=utf8'
                )
                return response
        else:
            pass

    def post(self, request):
        global  compteur, outputData
        compteur += 1
        if isinstance(request.data, dict):
            outputData = estimator(request.data)
            if isinstance(outputData, dict):
                response = Response(
                    outputData,
                    status=status.HTTP_200_OK,
                    content_type='application/xml; charset=utf8'
                )
                return response
            else:
                pass
        else:
            pass


class LogsOutput(RequestLogViewMixin, APIView):
    def get(self, request):
        if isinstance(request, Request):
            try:
                with open("logs.json") as log:
                    logs = json.load(log)
                    print(type(logs))
                    #print(logs)
                    if isinstance(logs, dict):
                        lines = ""
                        for key, value in logs.items():
                            #print(value)
                            line = "{}\t{}\t{}\t{}".format(
                                value["request_method"],
                                value["request_path"],
                                value["response_status"],
                                str(value["run_time"]) + "ms"
                            )
                            #print(line)
                            lines += "\n" + line
                        print(lines)
                        try:
                            with open("logs.txt", "w") as logs_txt:
                                logs_txt.write(lines)
                        except FileNotFoundError:
                            print("Fichier logs.txt introuvable")
                        try:
                            with open("logs.txt") as logs_txt:
                                response = Response(
                                    logs_txt.read(),
                                    status=status.HTTP_200_OK,
                                    content_type="text/plain"
                                )
                                return response
                        except FileNotFoundError:
                            print("Fichier logs.txt introuvable")
                    else:
                        pass

            except FileNotFoundError:
                print("Le fichier logs est introuvable")
                return Response("Le fichier logs est introuvable", status=status.HTTP_404_NOT_FOUND)