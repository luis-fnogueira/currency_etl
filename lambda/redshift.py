import logging
import psycopg2
from sqlalchemy import create_engine


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Redshift:

    def __init__(self, credentials: dict) -> None:
        
        self.__CREDENTIALS = credentials

        self.__URI = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"


    def __get_conn(self):

        try:

            return psycopg2.connect(
                host = self.__CREDENTIALS['host'],
                port = self.__CREDENTIALS['port'],
                user = self.__CREDENTIALS['user'],
                password = self.__CREDENTIALS['password'],
                database = self.__CREDENTIALS['database']
                )

        except Exception as error:

            logger.error(error)


    def __insert_data(self, data: dict, table: str, schema: str) -> None:

        """
        This function must be used to insert real data from the API.

        Args:
            data: str: The data retrieved from the API
            table: str: Table where data you'll be stored
            schema: str: Schema where table will be stored
        """

        try:

            # Running query SQL and getting data how DataFrame.
            
            data.to_sql(
                name      = table,
                con       = create_engine(self.__URI),
                schema    = schema,
                if_exists = "append",
                index     = False,
                dtype     = {}
            )

            # Returning the dataframe.

            logger.info(f"Record was loaded into: {schema}.{table}")

        except Exception as error:


            logger.error(error)


    def send_data_to_redshift(self, data: dict, table: str, schema: str) -> None:

        """
        This function effectively sends data to Redshift. If there was no error
        in the request, the data will be inserted. If the request returned an
        error, the error will be inserted in the correct column.
        """

        # if the key status is NOT in the dataset, send data to redshift
        if 'status' not in data:
        
            return self.__insert_data(data=data,
                                      table=table,
                                       schema=schema)

        else:

            raise AttributeError('There was a problem with the request')

   