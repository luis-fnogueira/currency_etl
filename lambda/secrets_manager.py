import json
import boto3
from botocore.exceptions import ClientError


class SecretsManager:

    @staticmethod
    def get_secret(secret_name: str) -> None:

        secret_name = secret_name
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            return json.loads(client.get_secret_value(
                SecretId=secret_name
            )['SecretString'])
        except ClientError as e:

            raise e
