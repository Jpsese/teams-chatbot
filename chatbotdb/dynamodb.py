import boto3

from botocore.exceptions import ClientError

class Dynamodb:

    def __init__(self, tableName, region, awsCred=None):
        self.tableName = tableName

        if awsCred != None:
            pass
        else:
            self._dynamodb_c = self._get_dynamodb_client(region)
            self._dynamodb_r = self._get_dynamodb_resource(region)

    def _get_dynamodb_client(self, region):
        dynamodb = boto3.client(
            'dynamodb',
            region_name=region
        )
        return dynamodb

    def _get_dynamodb_resource(self, region):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=region
        )
        return dynamodb

    def put_item(self, item):
        print('@teams: put_item')
        try:
            table = self._dynamodb_r.Table(self.tableName)
            resp = table.put_item(
                Item=item
            )
            return resp

        except ClientError as error:
            raise ClientError(error)

    def update_item(self, key, item):
        try:
            resp = self._dynamodb_c.update_item(
                TableName=self.tableName,
                Key=key,
                AttributeUpdates=item
            )

        except ClientError as error:
            raise ClientError(error)

        return resp

    def get_item(self, key):
        table = self._dynamodb_r.Table(self.tableName)
        resp = table.get_item(
            Key=key,
            ReturnConsumedCapacity='TOTAL'
        )
        return resp
