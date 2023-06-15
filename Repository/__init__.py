import pymongo
import motor
import json


class MongoBaseClass:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient('localhost', 27017)
        self.async_client = motor.MotorClient()