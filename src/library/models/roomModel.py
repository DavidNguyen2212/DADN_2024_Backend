from library import db
import datetime

class Room:
    collection = db["rooms"]
    
    def __init__(self, rid: int, rname: str, temperature: float, humidity: float, lux: float, 
                 updated_at: str):
        # required
        self.rid = rid
        self.rname = rname
        # self.autoMode = autoMode
        self.temperature = temperature
        self.humidity = humidity
        self.lux = lux
        self.updated_at = updated_at
    
    @classmethod
    def insert_room_record(cls, new_record: dict):
        """
        Insert a room state into this collection.
        """
        result = cls.collection.insert_one(new_record)
        return result.inserted_id
    
    def to_dictFormat(self):
        """
        Prepare the "new_notif" for the insertion above
        """
        instanceNotif_to_dict = {key: value for key,value in vars(self).items() if value is not None} 
        return instanceNotif_to_dict