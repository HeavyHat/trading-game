import pandas as pd

from urllib.request import urlopen
from urllib.error import URLError
import json
import time


class FxClientError(Exception):
    def __init__(self, message='Generic error'):
        self.message = message


class FxClient:
    """
      FxClient(endpoint, api_key)

      args:
        endpoint: the full http url to the exchange incl port. no ending slash
                  e.g. 'https://127.0.0.1:8080'
        api_key : the key
                  e.g. 'api_key1'
      raises:
        connection errors alone will be raised as FxClientError

        all failures returned by the api will be returned
          e.g. res = client.buy("GBPUSD", -1)
        will _not_ raise FxClientError
        but ("error" in res) == True

    """

    def __init__(self, endpoint, api_key):
        self._endpoint = endpoint
        self._api_key = api_key

    # private
    def _get_json(self, url):
        try:
            return json.loads(urlopen(url).read().decode('latin-1'))
        except(URLError):
            raise FxClientError()

    # public interface
    def buy(self, ccy_pair, amount):
        url = "{}/trade/{}/buy/{}/{}".format(self._endpoint, self._api_key, ccy_pair, amount)
        return self._get_json(url)

    def sell(self, ccy_pair, amount):
        url = "{}/trade/{}/sell/{}/{}".format(self._endpoint, self._api_key, ccy_pair, amount)
        return self._get_json(url)

    def account(self):
        url = "{}/account/{}".format(self._endpoint, self._api_key)
        return self._get_json(url)

    def market(self):
        url = "{}/market".format(self._endpoint)
        return self._get_json(url)


client = FxClient("https://manchester.fxbattle.uk", "49ddf4")
columns = ["GBPJPY",
           "EURGBP",
           "EURJPY",
           "EURUSD",
           "GBPUSD",
           "USDJPY"]
market_data = pd.DataFrame(columns=columns)
while True:
    time.sleep(0.1)
    current_tick = client.market()
    print(current_tick)
    current_prices = dict((key, (float(current_tick[key].split(" ")[-1]) + float(current_tick[key].split(" ")[-2]))/2) for key in current_tick.keys())
    market_data = market_data.append(current_prices, ignore_index=True)
    print(market_data)
