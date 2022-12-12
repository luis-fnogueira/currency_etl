from airflow.models import Variable
from datetime import datetime, timedelta


class AirflowVariables:

    DATETIME_FORMAT = "%Y-%m-%d"


    @staticmethod
    def update_interval(dag_name_params: str) -> None:

        """
        This function updates the time_interval variable from Airflow.

        Arguments:

            dag_name_params: String. The DAG's parameters on Airflow.

        Returns:

            None. It updates the variable in Airflow.
        """

        # Capturing the Airflow variable that stores the DAG metadata.
        params = Variable.get(dag_name_params, default_var=False, deserialize_json=True)

        # Capturing the variable that indicates the time span that should be applied.
        time_interval = params['time_interval']
        # Changing the due date to the start date.

        params['params']['start_date'] = params['params']['end_date']

        # Generating the next end date.

        params['params']['end_date'] = AirflowVariables.get_next_date(
            date=params['params']['end_date'],
            time_interval=time_interval
        )

        if AirflowVariables.is_past_date(dateTime = params['params']['end_date']):

            # Saving the updated variable as an Airflow variable.

            Variable.set(dag_name_params, value=params, serialize_json=True)


    @staticmethod
    def get_next_date(date: datetime, time_interval: dict, date_format: str = DATETIME_FORMAT) -> str:
        """ Creating a method to capture the date of the day following the date of entry.
        Args:
            date      : Datetime. It is the base date that you want to use.
            date_format: String. It is the format to which you want to convert the base date.
            time_interval: Dict. Defines the amount of time that must be given between the current date and the next date.
        Returns:
            nexDate: It is the base date plus the number of days that have progressed.
        """

        # Converting the datetime variable to a string format.
        next_date = datetime.strptime(date, date_format)

        # Converting dictionary values to integer.
        for k in time_interval.keys():
            time_interval[k] = int(time_interval[k])

        # Adding another day to the current date.

        next_date = next_date + timedelta(
            days=time_interval['days'],
            seconds=time_interval['seconds'],
            microseconds=time_interval['microseconds'],
            milliseconds=time_interval['milliseconds'],
            minutes=time_interval['minutes'],
            hours=time_interval['hours'],
            weeks=time_interval['weeks']
        )

        # Returning to the next date.

        return next_date.strftime(date_format)


    @staticmethod
    def is_past_date(dateTime: str) -> bool:

        """ Creating method to validate if a date is less than or equal to the current date
        Args:
            dateTime: String. It is the date to be verified.
        Returns:
            Returns a Boolean value indicating whether the date is less than or equal to the current date.
        """

        # Checking if the specified date is earlier than or equal to the current date.

        return datetime.strptime(dateTime, AirflowVariables.DATETIME_FORMAT) < datetime.now()