from datetime import datetime
from django.contrib import admin
from catalpa.aihun.models import Operation

admin.site.register(Operation)

class Admin():

    list_related = True

# I Don't know what to replace this with... yet
#    def save_model(self, request, obj, form, change):
#        if not change:
#            obj.creator = request.user
        #obj.changed_by = request.user
#        obj.save()
