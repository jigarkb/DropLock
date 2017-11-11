import model
import utils
import logging


class Vault(object):
    def __init__(self):
        pass

    def get(self, debug=False, **filters):
        query_string = "select * from Vault"

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

        vault_entry, vault_entry_exists = self.get_datastore_entity(data)
        if vault_entry_exists:
            raise Exception("Vault Entry already Exists!")

        vault_entry.put()

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "email": datastore_entity.email,
            "owner_id": datastore_entity.owner_id,
            "file_name": datastore_entity.file_name,
            "file_id": datastore_entity.file_id,
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M'),
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M'),
            "uploaded": datastore_entity.uploaded
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        key_name = "{}/{}".format(json_object["owner_id"]+json_object["file_id"])
        vault_entry_exists = True
        datastore_entity = model.Vault.get_by_key_name(key_name)
        if not datastore_entity:
            vault_entry_exists = False
            datastore_entity = model.User(key_name=key_name)

        datastore_entity.email = json_object["email"]
        datastore_entity.owner_id = json_object["owner_id"]
        datastore_entity.file_id = json_object["file_id"]
        datastore_entity.file_name = json_object["file_name"]
        datastore_entity.uploaded = json_object["uploaded"]

        return datastore_entity, vault_entry_exists

    def check_validity(self, method, data):
        error = []

        if error:
            raise Exception(error)
