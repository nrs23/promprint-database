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
    list_display = ["register_name", "register_pages", "register_file"]


class EntryAdmin(admin.ModelAdmin):
    inlines = [MatchInline]
    list_display = ["entry_title", "entry_author", "entry_date", "register"]
    list_filter = ["register"]
    search_fields = ["entry_title", "entry_author"]


class LibraryEntryAdmin(admin.ModelAdmin):
    inlines = [MatchInline]
    list_display = [
        "entry_title", "entry_author", "entry_date", "source_library"
    ]
    list_filter = ["source_library"]
    search_fields = ["entry_title", "entry_author"]


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "register_entry__entry_title", "register_entry__entry_author",
        "register_entry__register", "library_entry__entry_title",
        "library_entry__entry_author", "library_entry__source_library"
    ]
    list_filter = ["register_entry__register", "library_entry__source_library"]
    search_fields = [
        "register_entry__entry_title", "register_entry__entry_author",
        "library_entry__entry_title", "library_entry__entry_author"
    ]


admin.site.register(Register, RegisterAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(LibraryEntry, LibraryEntryAdmin)
admin.site.register(Matches, MatchAdmin)
