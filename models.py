from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import uuid

# A move away from auto-incement id's and to uuid's
def make_uuid():
    return str(uuid.uuid4())

    
class Model(models.Model):
    uuid = models.CharField(primary_key=True, unique=True, db_index=True, max_length=36, default=make_uuid, editable=False,)
    
    class Meta:
        abstract = True

class ModelType(Model):
    name = models.CharField(_('name'), db_index=True, max_length=100)
    description = models.CharField(_('description'), max_length=765, blank=True)
 
    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        abstract = True

class Operation(models.Model):
    """
    Typically: creation, deletion or modification of a model.
    The affected relation model is know through the generic foreign key
    """
    uuid = models.CharField(primary_key=True, unique=True, db_index=True, max_length=36, default=make_uuid, editable=False,)
    operator = models.ForeignKey(User, related_name="%(class)s_operations", verbose_name=_('Operator'), null=True, blank=False,)
    date = models.DateTimeField(_('operation date'), auto_now_add=True)
    name = models.IntegerField(_('operation'), null=True, blank=True) #e.g.: modification, creation, voiding
    description = models.CharField(_('operation description'),max_length=765,blank=True) #e.g: Voided because it was a Cylon
    ####################
    ## Aaaaarg. This is where the mismatch between the DB and Object paradigms collide
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    #instead of subject = models.ForeignKey(Model)
    class Meta:
        abstract = False
