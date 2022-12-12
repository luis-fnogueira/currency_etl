import json
import boto3


class LambdaFuncs:

    def invoke_lambda(lambda_payload: dict) -> None:

        lambda_client = boto3.client('lambda')

        lambda_payload = {**lambda_payload}

        lambda_client.invoke(FunctionName='currency_data', 
                            InvocationType='Event', # Set execution to async
                            Payload=json.dumps(lambda_payload))