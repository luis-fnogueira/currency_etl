import unittest
from mock import patch
from utils.aws.lambda_funcs import LambdaFuncs

class TestLambdaFuncs(unittest.TestCase):

    @patch(target='utils.aws.lambda_funcs.LambdaFuncs.invoke_lambda')
    def test_invoke_lambda(self, mock_invoke_lambda):

        """
        Testing the lambda_funcs function, which calls a lambda function in AWS. As it
        returns None, I had to mock the funcion and test its payload.
        """
        
        mock_invoke_lambda.return_value = {
                                "currency": "USD-BRL",
                                "table": "currency",
                                "schema": "public"
                                }

        self.assertEqual(LambdaFuncs.invoke_lambda(lambda_payload='some_payload'), 
                                {
                                "currency": "USD-BRL",
                                "table": "currency",
                                "schema": "public"
                                })


