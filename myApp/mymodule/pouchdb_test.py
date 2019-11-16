from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result

def Couch_connect(user, mypass, url):
    # IBM Cloudant Legacy authentication
    client = Cloudant(user, mypass, url=url)
    client.connect()
    return client

def Couch_create(client, database_name):
    my_database = client.create_database(database_name)
    if my_database.exists():
        print(f"'{database_name}' successfully created.")
        return my_database
    else:
        print('database failed')
        return "database creation failed"

def Couch_post(my_database, myDats):
    if my_database.exists():
        # Create documents using the sample data.
        # Go through each row in the array
        for mydat in myDats:
            # Create a document using the Database API.
            new_document = my_database.create_document(json_document)

            # Check that the document exists in the database.
            if new_document.exists():
                return True
            else:
                return false
    else:
        print('database failed')
        return false


def Couch_delete(client, database_name):
    try:
        client.delete_database(database_name)
    except CloudantException:
        print(f"There was a problem deleting '{database_name}'.\n")
    else:
        print(f"'{database_name}' successfully deleted.\n")


def Couch_disconnect(client):
    client.disconnect()
