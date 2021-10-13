from django.contrib import admin

from root.models import Animation, Effect, Light, Model, Sound, TextToSpeech, Language, Movement


admin.site.site_header = 'ABXR Admin'
admin.site.register(Model)
admin.site.register(Animation)
admin.site.register(TextToSpeech)
admin.site.register(Language)
admin.site.register(Movement)
admin.site.register(Effect)
admin.site.register(Sound)
admin.site.register(Light)
