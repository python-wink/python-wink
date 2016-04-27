import json
import os


class ApiResponseJSONLoader(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        with open('{}/{}'.format(os.path.dirname(__file__),
                                 self.file_name)) as json_file:
            response_dict = json.load(json_file)
        return response_dict
