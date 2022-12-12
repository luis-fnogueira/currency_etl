import requests
import pandas as pd


class CurrencyQuotation:

    @staticmethod
    def get_currency(currency: str) -> requests.Response:

        """
        This functions gets the last currency quote from a specified currency. 
        It uses the AwesomeAPI. Link: https://docs.awesomeapi.com.br/api-de-moedas

        Args:
            Currency: str. The currency that you want the price in the "USD-BRL" format.

        Return:
            The response from the API.
        """

        try:

            return requests.get(url=f'https://economia.awesomeapi.com.br/json/last/{currency}')

        except Exception as error:

            """
            Em case of error it'll return a message like this:
            {'status': 404, 'code': '<code>', 'message': '<message>'}
            """

            return error

    @staticmethod
    def currency_to_df(response: requests.Response) -> pd.DataFrame:

        """"
        Getting the currency passed in the URL and transforming it to the
        way that it's written in the dictionary
        Example:
        USD-BRL to USDBRL

        Args:
            response: Response Object. The object created from the request

        Return:
            A dataframe with the 
        """
        currency = response.url[-7::].replace('-', '')

        return pd.DataFrame(response.json()[currency], index=[0])
