import logging
from redshift import Redshift
from secrets_manager import SecretsManager
from currency_quotation import CurrencyQuotation


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    logger.info(f"[1] Retrieving the credentials of Redshift from Secrets Manager and settingthe currency to get data")
    credentials: dict = SecretsManager.get_secret(secret_name='redshift_secret_1')
    currency: str = event['currency']
    

    logger.info("[2] Retrieving data from the API")
    data = CurrencyQuotation.get_currency(currency=currency)


    logger.info("[3] Passing data retrieved to a df")
    df_data = CurrencyQuotation.currency_to_df(data)
    

    logger.info("[4] Inserting data in Redshift...")
    database = Redshift(credentials=credentials)
    database.send_data_to_redshift(
                                   data=df_data,
                                   table=event['table'],
                                   schema=event['schema']
                                   )
