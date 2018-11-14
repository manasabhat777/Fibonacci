from mongoengine import *


class RequestLog(Document):
    request_log_time = DateTimeField(required=True, unique=True)
    request = StringField(max_length=100, required=True)
    response = DictField()
    status_code = IntField()

    meta = {'collection': 'log-collection'}
