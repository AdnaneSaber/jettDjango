from django.contrib import admin

from root.models import Animation, Model


admin.site.site_header = 'ABXR Admin'
admin.site.register(Model)
admin.site.register(Animation)
