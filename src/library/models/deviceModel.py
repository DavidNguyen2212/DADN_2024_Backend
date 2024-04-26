from library import db
import datetime

class Device:
    collection = db["devices"]
    
    def __init__(self, rid: int, did: int, dname: str,  updated_at: str, tempAC: int = None, state: str = "off"):
        # required
        self.rid = rid
        self.dname = dname
        self.state = state
        self.updated_at = updated_at

        # for AC
        self.tempAC = tempAC
    
    @classmethod
    def insert_device_record(cls, new_record: dict):
        """
        Insert a device state into this collection.
        """
        result = cls.collection.insert_one(new_record)
        return result.inserted_id
    
    def to_dictFormat(self):
        """
        Prepare the "new_notif" for the insertion above
        """
        instanceNotif_to_dict = {key: value for key,value in vars(self).items() if value is not None} 
        return instanceNotif_to_dict