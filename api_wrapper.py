__author__ = 'DerekHu'

import requests

## Import api key
from api_key import dirble_key

## Raised when when problems with the apikey
class APIError(RuntimeError):
    pass

class DribleAPI(object):

    def __init__(self):
        self.base_url = 'http://api.dirble.com/v1/'
        self.s = requests.session()


    ## Send a GET request to a specified API portion
    #
    #  @Param   portion     The portion that is appended to the base url for different query purpose
    #  @Param   params      Parameter dictionary for GET request
    #  @Param   kwargs      Other arguments
    #
    #  @Return  JSON response data
    def __get(self, portion, params={}, **kwargs):
        response = self.s.get(self.base_url + portion, params=params, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            e.args = e.args + (response.json(), )
            raise e

        data = response.json()
        if 'errormsg' in data and data['errormsg'] is not None:
            raise APIError(data['errormsg'], data)
        return data

    ## Get main, head categories
    #  @Return  a list of categories. Each category contains id, name, and description
    def get_main_categories(self):
        return self.__get('/primaryCategories/apikey/' + dirble_key)

    def get_stations_list(self, cid):
        query_str =  self.base_url + 'stations/apikey/{}/id/{}'.format(dirble_key, cid)
        return requests.get(query_str).json()


if __name__ == "__main__":
    api = DribleAPI()
    print(api.get_main_categories())
    #print(api.get_stations_list(56))
