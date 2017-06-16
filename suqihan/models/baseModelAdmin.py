from django.contrib.admin.options import ModelAdmin

default_ordering = ("lastmodified",)

class BaseModelAdmin(ModelAdmin):
    pass

class BaseModelAdminDefaultOrdering(BaseModelAdmin):
    ordering = default_ordering





