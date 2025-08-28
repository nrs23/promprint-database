from django.contrib import admin
from .models import Register, RegisterEntry, LibraryEntry, MatchCandidate
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources, widgets


def redo_match_search(modeladmin, request, queryset):
    # Saving RegisterEntry objects will trigger the search function
    for register in queryset:
        entries = RegisterEntry.objects.filter(register=register.id)
        for entry in entries:
            entry.save()


redo_match_search.short_description = "Redo match search on each entry" \
                                      " in selected registers"


class RegisterEntryInline(admin.TabularInline):
    model = RegisterEntry
    extra = 1


class MatchInline(admin.TabularInline):
    model = MatchCandidate
    extra = 1


class RegisterAdmin(admin.ModelAdmin):
    inlines = [RegisterEntryInline]
    list_display = ["name", "pages", "file", "_entry_count"]
    actions = [redo_match_search]

    def _entry_count(self, obj):
        return obj.registerentry_set.count()

    _entry_count.short_description = "Entry Count"


class RegisterEntryResource(resources.ModelResource):
    register = fields.Field(
        column_name='register',
        attribute='register',
        widget=widgets.ForeignKeyWidget(Register, field='name')
    )

    class Meta:
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'register', 'date', 'author', 'title')
        model = RegisterEntry


class RegisterEntryAdmin(ImportExportModelAdmin):
    resource_classes = [RegisterEntryResource]
    inlines = [MatchInline]
    list_display = [
        "title",
        "author",
        "date",
        "register",
        "_match_count",
        "match_confirmed",
    ]
    list_filter = ["register", "match_confirmed"]
    search_fields = ["title", "author"]

    def _match_count(self, obj):
        return obj.matchcandidate_set.count()

    _match_count.short_description = "Match Candidate Count"


class LibraryEntryResource(resources.ModelResource):
    register = fields.Field(
        column_name='register',
        attribute='register',
        widget=widgets.ManyToManyWidget(Register, field='name', separator='|')
    )

    class Meta:
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'source_library', 'register', 'date', 'author', 'title')
        model = LibraryEntry


class LibraryEntryAdmin(ImportExportModelAdmin):
    resource_classes = [LibraryEntryResource]
    inlines = [MatchInline]
    list_display = ["title", "author", "date", "source_library"]
    list_filter = ["source_library"]
    search_fields = ["title", "author"]


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "match_type", "register_entry__title", "library_entry__title",
        "register_entry__author", "library_entry__author",
        "register_entry__register", "library_entry__source_library",
        "match_confirmed"
    ]
    list_filter = [
        "register_entry__register", "library_entry__source_library",
        "match_type", "match_confirmed"
    ]
    search_fields = [
        "register_entry__title", "register_entry__author",
        "library_entry__title", "library_entry__author"
    ]


admin.site.register(Register, RegisterAdmin)
admin.site.register(RegisterEntry, RegisterEntryAdmin)
admin.site.register(LibraryEntry, LibraryEntryAdmin)
admin.site.register(MatchCandidate, MatchAdmin)
