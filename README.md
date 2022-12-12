# Currency ETL project

## Summary

This project gets currency quotation data from the [AwesomeAPI]('https://docs.awesomeapi.com.br/api-de-moedas') and stores them in a Redshift table.

[![image](https://i.imgur.com/zmQtAkv.png)](https://imgur.com/a/upJS3SN)

The flow is the following: every minute a DAG in Airflow triggers the Lambda function on AWS to get the data from the API and just after store it on Redshift.

## About the Lambda function

[![image](https://i.imgur.com/wCzT1uM.png)](https://imgur.com/a/0cKGfgA)

- For better security the credentials of Redshift are stored in Secrets Manager, so first of all one needs to retrieve them. 
- Secondly, the class quotation_currency gets data from the API and then converts it to a Pandas DF, so it can be stored in the table.
- The dataframe is passed to a function that stores the data.

### Note
This project is intented to be used with one or a couple currencies. So it'd be simple to make a query with a WHERE clause. But if you want to use with a lot of currencies, I recommend creating a table for each quotation.