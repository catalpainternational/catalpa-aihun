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

    @property
    def is_valid(self,):
        ops = Operation.objects.filter(object_id=self.uuid).filter(name="voiding")
        for op in ops:
            if op.is_voiding():
                return False
        return True

    @property
    def last_modified(self,):
        op = Operation.objects.filter(object_id=self.uuid).filter(name__in=['creation','modification','importation']).order_by("-date")[0]
        return op.date

    @property
    def last_modification(self,):
        op = Operation.objects.filter(object_id=self.uuid).filter(name__in=['creation','modification','importation']).order_by("-date")[0]
        return op

    @property
    def creation_date(self,):
        op = Operation.objects.filter(object_id=self.uuid).filter(name='creation').order_by("-date")[0]
        return op.date


class ModelType(Model):
    name = models.CharField(_('name'), db_index=True, max_length=100)
    description = models.CharField(_('description'), max_length=765, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        abstract = True

class Operation(models.Model):
    """
    Typically: creation, modification or voiding of a model.
    The affected relation model is know through the generic foreign key
    """
    uuid = models.CharField(primary_key=True, unique=True, db_index=True, max_length=36, default=make_uuid, editable=False,)
    operator = models.ForeignKey(User, related_name="%(class)s_operations", verbose_name=_('Operator'), null=True, blank=False,)
    date = models.DateTimeField(_('operation date'), auto_now_add=True)
    name = models.CharField(_('operation'),max_length=15, null=False, blank=False) #e.g.: modification, creation, voiding
    description = models.CharField(_('operation description'),max_length=765,blank=True) #e.g: Voided because it was a Cylon
    ####################
    ## Aaaaarg. This is where the mismatch between the DB and Object paradigms collide
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36,db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    #instead of subject = models.ForeignKey(Model)

    def setup(self,operator,operation,operated,reason):
        self.operator = operator
        self.name = operation
        self.description = reason
        self.object_id = operated.uuid
        self.content_type = ContentType.objects.get_for_model(operated.__class__)

    def create(self,who,what,why):
        self.setup(who,'creation',what,why)

    def modify(self,who,what,why):
        self.setup(who,'modification',what,why)

    def void(self,who,what,why):
        self.setup(who,'voiding',what,why)

    def import_op(self,who,what,why):
        self.setup(who,'importation',what,why)


    """
    Supported operations: voiding, creation, modification
    """
    def is_voiding(self):
        return self.name == 'voiding'

    def is_creation(self):
        return self.name == 'creation'

    def is_modification(self):
        return self.name == 'modification'

    def is_import(self):
        return self.name == 'importation'

    class Meta:
        abstract = False
