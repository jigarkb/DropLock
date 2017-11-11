from google.appengine.ext import db


class User(db.Model):
    email = db.EmailProperty()
    name = db.StringProperty()
    dob = db.StringProperty()
    phone = db.StringProperty()
    address_line_1 = db.TextProperty()
    address_line_2 = db.TextProperty()
    owner_id = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class Vault(db.Model):
    email = db.EmailProperty()
    owner_id = db.StringProperty()
    file_name = db.StringProperty()
    file_id = db.StringProperty()
    uploaded = db.BooleanProperty(default=False)

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)

