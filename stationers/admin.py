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
    list_display = ["name", "pages", "file", "_entry_count"]

    def _entry_count(self, obj):
        return obj.registerentry_set.count()

    _entry_count.short_description = "Entry Count"


class RegisterEntryAdmin(admin.ModelAdmin):
    inlines = [MatchInline]
    list_display = [
        "title", "author", "date", "register", "_match_count",
        "human_checked",
    ]
    list_filter = ["register", "human_checked"]
    search_fields = ["title", "author"]

    def _match_count(self, obj):
        return obj.matchcandidate_set.count()

    _match_count.short_description = "Match Candidate Count"


class LibraryEntryAdmin(admin.ModelAdmin):
    inlines = [MatchInline]
    list_display = ["title", "author", "date", "source_library"]
    list_filter = ["source_library"]
    search_fields = ["title", "author"]


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "match_type", "register_entry__title", "library_entry__title",
        "register_entry__author", "library_entry__author",
        "register_entry__register", "library_entry__source_library",
        "human_checked"
    ]
    list_filter = [
        "register_entry__register", "library_entry__source_library",
        "human_checked"
    ]
    search_fields = [
        "register_entry__title", "register_entry__author",
        "library_entry__title", "library_entry__author"
    ]


admin.site.register(Register, RegisterAdmin)
admin.site.register(RegisterEntry, RegisterEntryAdmin)
admin.site.register(LibraryEntry, LibraryEntryAdmin)
admin.site.register(MatchCandidate, MatchAdmin)
