import socket
import time
import json
from json import JSONDecodeError

class RequestLogMiddleware(object):
    def process_request(self, request):
        request.start_time = time.time()
        #print( request.start_time, time.ctime(request.start_time))

    def process_response(self, request, response):

        if response['content-type'] == 'application/json':
            if getattr(response, 'streaming', False):
                response_body = '<<<Streaming>>>'
            else:
                response_body = response.content
        elif response['content-type'] == 'application/xml':
            if getattr(response, 'streaming', False):
                response_body = '<<<Streaming>>>'
            else:
                response_body = response.content
        else:
            response_body = '<<<Not XML>>>'

        log_data = {
            'user': request.user.pk,

            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),

            'request_method': request.method,
            'request_path': request.get_full_path(),
            #'request_body': request.body,

            'response_status': response.status_code,
            'response_body': response_body,

            'run_time': int((time.time() - request.start_time) * 1000) ,
        }

        # save log_data in some way
        logs = {}
        try:
            with open("logs.json") as log:
                try:
                    logs = json.load(log)
                    if isinstance(logs, dict):
                        with open("logs.json", "w") as log_json:
                            cpt = len(logs)
                            if cpt != 0:
                                logs["{}".format(cpt + 1)] = log_data
                            else:
                                logs["1"] = log_data
                                #data = json.dumps(logs, indent=4)
                                #print(type(data))
                            log_json.write(json.dumps(logs, indent=4))
                    else:
                        pass
                except JSONDecodeError:
                    with open("logs.json", "w") as log_json:
                        logs["1"] = log_data
                        print(type(logs))
                        log_json.write(json.dumps(logs, indent=4))
        except FileNotFoundError:
            print("Fichier introuvable")

        return response