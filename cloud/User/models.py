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
            "name": datastore_entity.name,
            "dob": datastore_entity.dob,
            "phone": datastore_entity.phone,
            "address_line_1": datastore_entity.address_line_1,
            "address_line_2": datastore_entity.address_line_2,
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
        datastore_entity.name = json_object["name"]
        datastore_entity.dob = json_object["dob"]
        datastore_entity.phone = json_object["phone"]
        datastore_entity.address_line_1 = json_object["address_line_1"]
        datastore_entity.address_line_2 = json_object["address_line_2"]
        datastore_entity.owner_id = json_object["owner_id"]

        return datastore_entity, user_exists

    def check_validity(self, method, data):
        error = []

        if error:
            raise Exception(error)
