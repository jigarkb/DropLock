from google.appengine.ext import db


class User(db.Model):
    email = db.EmailProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    dob = db.StringProperty()
    phone = db.StringProperty()
    address = db.TextProperty()
    owner_id = db.StringProperty()
    code = db.TextProperty()

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

