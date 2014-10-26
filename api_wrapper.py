__author__ = 'DerekHu'

import requests

## Import api key
from api_key import dirble_key
from random import randint

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
    #  @Param   kwargs      Parameter dictionary for GET request
    #
    #  @Return  JSON response data
    def __get(self, portion, **kwargs):
        query_str = self.base_url + portion + '/apikey/' + dirble_key + '/'
        for key in kwargs:
            query_str += key + '/' + str(kwargs[key])
        response = self.s.get(query_str)
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
        return self.__get(portion='primaryCategories')


    ## Get station list in a category using cid
    #  @Param   cid     category id
    #  @Return  a list of stations. Each station contains id, name, streaurl, country, bitratem status
    def get_station_list(self, cid):
        return self.__get(portion='stations', id=cid)


    ## Get information on a station by sid
    #  @Param   sid     station id
    #  @Return  A dictionary contains detail information of a station. Information include id, name ,streamurl, bitrate, country, urlid, website, status, songhistory, directory
    def get_station(self, sid):
        return self.__get(portion='station', id=sid)


    ## Get random station by combining random category, station list search
    def get_random_station(self):
        categories = self.get_main_categories()
        station_list = self.get_station_list(categories[randint(0, len(categories)-1)]['id'])
        return self.get_station(station_list[randint(0, len(station_list)-1)]['id'])


if __name__ == "__main__":
    api = DribleAPI()
    #print(api.get_main_categories())
    #print(api.get_station_list(11))
    print(api.get_station(9390))
