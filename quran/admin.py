from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Part)
admin.site.register(Place)
admin.site.register(Surah)
admin.site.register(Aya)
admin.site.register(Reader)
admin.site.register(Aya_Audio)