from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result

from django.core import serializers
from myApp.models import FCT, DRI, DRI_women, Family, Person, Crop
import json

def Couch_connect(user, mypass, url):
    # IBM Cloudant Legacy authentication
    client = Cloudant(user, mypass, url=url)
    client.connect()
    return client

def Couch_create(client, database_name):
    if database_name in client:
        my_database = client[database_name]
    else:
        my_database = client.create_database(database_name)
    return my_database

def Couch_post(my_database, myDats):
    if my_database.exists():
        # Create documents using the sample data.
        # Go through each row in the array
        for mydat in myDats:
            # Create a document using the Database API.
            new_document = my_database.create_document(mydat['fields'])
        return True

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


myid = "82e081b0-8c7a-44fe-bb89-b7330ba202a2-bluemix"
mypass = "f8dabca0c2ed8c226f6a794ceaa65b625ae642f86ee0afcedf093d7e153edbd6"
myurl = "https://82e081b0-8c7a-44fe-bb89-b7330ba202a2-bluemix:f8dabca0c2ed8c226f6a794ceaa65b625ae642f86ee0afcedf093d7e153edbd6@82e081b0-8c7a-44fe-bb89-b7330ba202a2-bluemix.cloudantnosqldb.appdomain.cloud"

client = Couch_connect(myid, mypass, url=myurl)

tmp = serializers.serialize('json',FCT.objects.all())
tmp = tmp.replace("\"pk\": ", "\"_id\": \"")
tmp = tmp.replace(", \"fields\"", "\", \"fields\"")
mydats = json.loads(tmp)
database_name = "fct"

my_database = Couch_create(client, database_name)
if my_database.exists():
    print(f"'{database_name}' successfully created.")
my_database.bulk_docs(mydats)

tmp = serializers.serialize('json',DRI.objects.all())
tmp = tmp.replace("\"pk\": ", "\"_id\": \"")
tmp = tmp.replace(", \"fields\"", "\", \"fields\"")
mydats = json.loads(tmp)
database_name = "dri"

my_database = Couch_create(client, database_name)
if my_database.exists():
    print(f"'{database_name}' successfully created.")
my_database.bulk_docs(mydats)

tmp = serializers.serialize('json',DRI_women.objects.all())
tmp = tmp.replace("\"pk\": ", "\"_id\": \"")
tmp = tmp.replace(", \"fields\"", "\", \"fields\"")
mydats = json.loads(tmp)
database_name = "dri_women"

my_database = Couch_create(client, database_name)
if my_database.exists():
    print(f"'{database_name}' successfully created.")
my_database.bulk_docs(mydats)

tmp = serializers.serialize('json',Family.objects.all())
tmp = tmp.replace("\"pk\": ", "\"_id\": \"")
tmp = tmp.replace(", \"fields\"", "\", \"fields\"")
mydats = json.loads(tmp)
database_name = "family"

my_database = Couch_create(client, database_name)
if my_database.exists():
    print(f"'{database_name}' successfully created.")
my_database.bulk_docs(mydats)

tmp = serializers.serialize('json',Person.objects.all())
tmp = tmp.replace("\"pk\": ", "\"_id\": \"")
tmp = tmp.replace(", \"fields\"", "\", \"fields\"")
mydats = json.loads(tmp)
database_name = "person"

my_database = Couch_create(client, database_name)
if my_database.exists():
    print(f"'{database_name}' successfully created.")
my_database.bulk_docs(mydats)

tmp = serializers.serialize('json',Crop.objects.all())
tmp = tmp.replace("\"pk\": ", "\"_id\": \"")
tmp = tmp.replace(", \"fields\"", "\", \"fields\"")
mydats = json.loads(tmp)
database_name = "crop"

my_database = Couch_create(client, database_name)
if my_database.exists():
    print(f"'{database_name}' successfully created.")
my_database.bulk_docs(mydats)



client.disconnect()
