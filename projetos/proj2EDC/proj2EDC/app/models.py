from django.db import models
import os
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
endpoint = "http://localhost:7200"
repo_name = "anuncios"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

def get_id():
    input = """ 
        PREFIX stand: <http://stand.com/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        select ?id where { 
        
         
        
            ?s a stand:Anuncio. 
            ?s stand:id ?id.
        }
        order by desc(xsd:integer(?id)) limit 1
    """

    res = accessor.sparql_select(body={"query": input}, repo_name=repo_name)
    res = json.loads(res)  # ultimo id
    res = res['results']['bindings'][0]['id']['value']
    res = int(res) + 1
    return res

def content_file_name(instance, filename):
    filename = "%s.png" % (get_id())
    return os.path.join('.', filename)

# Create your models here.
class Image(models.Model):
    id = get_id()
    image = models.ImageField(upload_to=content_file_name)

    def __str__(self):
        return self.id

