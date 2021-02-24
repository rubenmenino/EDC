from django.db import models
import os
from BaseXClient import BaseXClient

def get_id():
    res = ''
    try:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        input = "let $i := (for $id in collection('anuncios')//anuncio return sum($id/id)) return $i[last()]+1"
        query = session.query(input)

        res = query.execute()
    finally:
        if session:
            session.close()

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

