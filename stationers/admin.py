from django.contrib import admin
from .models import Register, Entry, LibraryEntry, Matches

admin.site.register(Register)
admin.site.register(Entry)
admin.site.register(LibraryEntry)
admin.site.register(Matches)
