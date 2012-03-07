from datetime import datetime
from django.contrib import admin
from catalpa.aihun.models import Operation


class OperationAdmin(admin.ModelAdmin):
    list_display = ("date","name","operator","description")
    

class Admin():

    list_related = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        obj.changed_by = request.user
        obj.save()


admin.site.register(Operation,OperationAdmin)
