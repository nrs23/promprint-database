from django.contrib import admin
from .models import Register, RegisterEntry, LibraryEntry, MatchCandidate


class RegisterEntryInline(admin.TabularInline):
    model = RegisterEntry
    extra = 1


class MatchInline(admin.TabularInline):
    model = MatchCandidate
    extra = 1


class RegisterAdmin(admin.ModelAdmin):
    inlines = [RegisterEntryInline]
    list_display = ["name", "pages", "file"]


class RegisterEntryAdmin(admin.ModelAdmin):
    inlines = [MatchInline]
    list_display = ["title", "author", "date", "register"]
    list_filter = ["register", "confirmed_match"]
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
admin.site.register(RegisterEntry, RegisterEntryAdmin)
admin.site.register(LibraryEntry, LibraryEntryAdmin)
admin.site.register(MatchCandidate, MatchAdmin)
