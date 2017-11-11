import model
import utils
import logging


class User(object):
    def __init__(self):
        pass

    def get(self, debug=False, **filters):
        query_string = "select * from User"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "%s='%s' and " % (field, filters[field])
            else:
                query_string += "%s='%s'" % (field, filters[field])
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    def add(self, **data):
        self.check_validity(method='add', data=data)

        user, user_exists = self.get_datastore_entity(data)
        if user_exists:
            raise Exception("User already Exists!")

        user.put()

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "email": datastore_entity.email,
            "first_name": datastore_entity.first_name,
            "last_name": datastore_entity.last_name,
            "dob": datastore_entity.dob,
            "phone": datastore_entity.phone,
            "address": datastore_entity.address,
            "owner_id": datastore_entity.owner_id,
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M'),
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M'),
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        user_exists = True
        datastore_entity = model.User.get_by_key_name(json_object["email"])
        if not datastore_entity:
            user_exists = False
            datastore_entity = model.User(key_name=json_object["email"])

        datastore_entity.email = json_object["email"]
        datastore_entity.first_name = json_object.get("first_name")
        datastore_entity.last_name = json_object.get("last_name")
        datastore_entity.dob = json_object.get("dob")
        datastore_entity.phone = json_object.get("phone")
        datastore_entity.address = json_object.get("address")
        datastore_entity.owner_id = json_object.get("owner_id")
        datastore_entity.code = json_object.get("code")

        return datastore_entity, user_exists

    def check_validity(self, method, data):
        error = []

        if error:
            raise Exception(error)
