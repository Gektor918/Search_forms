from tinydb import Query, TinyDB


class FormModel:
    def __init__(self, db_path='db.json'):
        self.db = TinyDB(db_path)
        self.Form = Query()

    def insert_new_form(self, data):
        return self.db.insert(data)
    
    def search_form(self, result_filter):
        return self.db.search((self.Form.order_date == result_filter['order_date']) &
                              (self.Form.lead_email == result_filter['lead_email']) &
                              (self.Form.phone_number == result_filter['phone_number']) &
                              (self.Form.text_message == result_filter['text_message']))
