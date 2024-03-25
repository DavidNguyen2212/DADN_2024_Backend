from library import db
import datetime

class Notification:
    collection = db["notifications"]
    
    def __init__(self, notif_type: str, content: str, created_at: str, device: str = None, place: str =None):
        # required
        self.type = notif_type
        self.content = content
        self.created_at = created_at
        # optional
        self.device = device
        self.place = place
    
    @classmethod
    def insert_notification(cls, new_notif: dict):
        """
        Insert a notification into this collection.
        """
        result = cls.collection.insert_one(new_notif)
        return result.inserted_id

    @classmethod
    def find_notifs_by_day(cls, day):
        """
        Find notification list by the day requested by user. Return the result of query, 
        not an Notification object.
        Use the format_notifs() from services to deal with it
        """
        day_to_get_datetime = datetime.datetime.strptime(day, "%Y-%m-%d")

        # Create the range for the query
        start_datetime = day_to_get_datetime.replace(hour=0, minute=0, second=0)
        end_datetime = day_to_get_datetime.replace(hour=23, minute=59, second=59)

        # Searching
        notices = Notification.collection.find({
            "created_at": {
            "$gte": start_datetime.isoformat(),
            "$lte": end_datetime.isoformat()
            }
        }).sort({"created_at": -1})
        
        return notices
    
    def to_dictFormat(self):
        """
        Prepare the "new_notif" for the insertion above
        """
        instanceNotif_to_dict = {key: value for key,value in vars(self).items() if value is not None} 
        return instanceNotif_to_dict
        

    
    # def update_book(self, title, new_data):
    #     """
    #     Update a book's data by its title.
    #     """
    #     result = self.collection.update_one({"title": title}, {"$set": new_data})
    #     return result.modified_count
    
    # def delete_book(self, title):
    #     """
    #     Delete a book by its title.
    #     """
    #     result = self.collection.delete_one({"title": title})
    #     return result.deleted_count