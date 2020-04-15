from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_xml.renderers import XMLRenderer
import json
from .mixins import RequestLogViewMixin

try:
    from .estimator import estimator
except ImportError:
    print("Import failed")

outputData = None
logs = {}


# Create your views here.
class EstimatorData(RequestLogViewMixin, APIView):
    def get(self, request):
        global outputData

        if isinstance(request, Request):
            if outputData is not None:
                response = Response(
                    outputData,
                    status=status.HTTP_200_OK,
                    content_type='application/json; charset=utf8'
                )
                return response
            else:
                if (
                        request.data["data-period-type"] and
                        request.data["data-time-to-elapse"] and
                        request.data["data-reported-cases"] and
                        request.data["data-population"] and
                        request.data["data-total-hospital-beds"]
                ):
                    input_data = {
                        "region": {
                            "name": "Africa",
                            "avgAge": 19.7,
                            "avgDailyIncomeInUSD": 4,
                            "avgDailyIncomePopulation": 0.73
                        },
                        "periodType": request.data["data-period-type"],
                        "timeToElapse": int(request.data["data-time-to-elapse"]),
                        "reportedCases": int(request.data["data-reported-cases"]),
                        "population": int(request.data["data-population"]),
                        "totalHospitalBeds": int(request.data["data-total-hospital-beds"])
                    }
                    outputData = estimator(input_data)
                    response = Response(
                        outputData,
                        status=status.HTTP_200_OK,
                        content_type='application/json; charset=utf8'
                    )
                    return response
                else:
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

    def post(self, request):
        global outputData

        if isinstance(request, Request):

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


class EstimatorDataXML(RequestLogViewMixin, APIView):
    renderer_classes = (XMLRenderer,)

    def get(self, request):
        global outputData

        if isinstance(request, Request):
            if outputData is not None:
                response = Response(
                    outputData,
                    status=status.HTTP_200_OK,
                    content_type='application/xml; charset=utf8'
                )
                return response
            else:
                if (
                        request.data["data-period-type"] and
                        request.data["data-time-to-elapse"] and
                        request.data["data-reported-cases"] and
                        request.data["data-population"] and
                        request.data["data-total-hospital-beds"]
                ):
                    input_data = {
                        "region": {
                            "name": "Africa",
                            "avgAge": 19.7,
                            "avgDailyIncomeInUSD": 4,
                            "avgDailyIncomePopulation": 0.73
                        },
                        "periodType": request.data["data-period-type"],
                        "timeToElapse": int(request.data["data-time-to-elapse"]),
                        "reportedCases": int(request.data["data-reported-cases"]),
                        "population": int(request.data["data-population"]),
                        "totalHospitalBeds": int(request.data["data-total-hospital-beds"])
                    }
                    outputData = estimator(input_data)
                    response = Response(
                        outputData,
                        status=status.HTTP_200_OK,
                        content_type='application/xml; charset=utf8'
                    )
                    return response
                else:
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

    def post(self, request):
        global outputData
        if isinstance(request, Request):

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
                    # print(logs)
                    if isinstance(logs, dict):
                        lines = ""
                        for key, value in logs.items():
                            # print(value)
                            line = "{}\t\t{}\t\t{}\t\t{}\n".format(
                                value["request_method"],
                                value["request_path"],
                                value["response_status"],
                                str(value["run_time"]) + " ms"
                            )
                            # print(line)
                            lines += line
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
                                    content_type='text/plain; charset=utf8'
                                )
                                return response
                        except FileNotFoundError:
                            print("Fichier logs.txt introuvable")
                    else:
                        pass

            except FileNotFoundError:
                print("Le fichier logs est introuvable")
                return Response("Le fichier logs est introuvable", status=status.HTTP_404_NOT_FOUND)
        else:
            pass
