from django.contrib import admin
from .models import Register, Entry, LibraryEntry, Matches


class EntryInline(admin.TabularInline):
    model = Entry
    extra = 1


class MatchInline(admin.TabularInline):
    model = Matches
    extra = 1


class RegisterAdmin(admin.ModelAdmin):
    inlines = [EntryInline]
    list_display = ["name", "pages", "file"]


class EntryAdmin(admin.ModelAdmin):
    inlines = [MatchInline]
    list_display = ["title", "author", "date", "register"]
    list_filter = ["register"]
    search_fields = ["title", "author"]


class LibraryEntryAdmin(admin.ModelAdmin):
    inlines = [MatchInline]
    list_display = [
        "title", "author", "date", "source_library"
    ]
    list_filter = ["source_library"]
    search_fields = ["title", "author"]


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "register_entry__title", "register_entry__author",
        "register_entry__register", "library_entry__title",
        "library_entry__author", "library_entry__source_library"
    ]
    list_filter = ["register_entry__register", "library_entry__source_library"]
    search_fields = [
        "register_entry__title", "register_entry__author",
        "library_entry__title", "library_entry__author"
    ]


admin.site.register(Register, RegisterAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(LibraryEntry, LibraryEntryAdmin)
admin.site.register(Matches, MatchAdmin)
