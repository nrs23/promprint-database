from django.db import models
from django.utils.translation import gettext_lazy as _


class Register(models.Model):
    register_name = models.CharField(max_length=100)
    register_start_date = models.DateField("register start date")
    register_end_date = models.DateField("register end date")
    register_pages = models.IntegerField(default=0)
    register_file = models.FileField(upload_to="register_pdfs")

    def __str__(self):
        return self.register_name


class Entry(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    entry_date = models.DateField("date of entry")
    entry_author = models.CharField(max_length=100)
    entry_title = models.CharField(max_length=500)
    entry_volumes = models.CharField(max_length=100, blank=True)
    entry_edition = models.CharField(max_length=100, blank=True)
    register_page = models.IntegerField(default=0)
    confirmed_match = models.BooleanField(default=False)

    def match_entry(self):
        associated_library_entries = LibraryEntry.objects.filter(
            register=self.register.id)
        matched_titles = associated_library_entries.filter(
            entry_title__iexact=self.entry_title)
        matched_author_and_titles = matched_titles.filter(
            entry_author__iexact=self.entry_author)
        for matched_entry in matched_author_and_titles:
            _, _ = Matches.objects.get_or_create(match_type="EXC",
                                                 register_entry=self,
                                                 library_entry=matched_entry)
        matched_only_titles = matched_titles.exclude(
            entry_author__iexact=self.entry_author)
        for matched_entry in matched_only_titles:
            _, _ = Matches.objects.get_or_create(match_type="PAR",
                                                 register_entry=self,
                                                 library_entry=matched_entry)

    def __str__(self):
        return f"{self.entry_author}: {self.entry_title}"


class LibraryEntry(models.Model):

    class Library(models.TextChoices):
        BODLEIAN_LIBRARY = "BOL", _("Bodleian Library")
        BRITISH_LIBRARY = "BRL", _("British Library")
        CAMBRIDGE_LIBRARY = "CAL", _("Cambridge Library")
        SCOTLAND_LIBRARY = "SCL", _("National Library of Scotland")
        TRINITY_LIBRARY = "TRL", _("Trinity College Dublin Library")

    source_library = models.CharField(max_length=3,
                                      choices=Library,
                                      default=Library.BRITISH_LIBRARY)
    register = models.ManyToManyField(Register)
    entry_date = models.DateField("date of entry")
    entry_author = models.CharField(max_length=100)
    entry_title = models.CharField(max_length=500)
    entry_volumes = models.CharField(max_length=100, blank=True)
    entry_edition = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.entry_author}: {self.entry_title}"


class Matches(models.Model):

    class MatchType(models.TextChoices):
        EXACT = "EXC", _("Exact match")
        PARTIAL = "PAR", _("Partial match")
        FUZZY = "FUZ", _("Fuzzy match")
        NONE = "NON", _("No match")

    match_type = models.CharField(max_length=3,
                                  choices=MatchType,
                                  default=MatchType.NONE)
    register_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    library_entry = models.ForeignKey(LibraryEntry,
                                      on_delete=models.CASCADE,
                                      null=True)

    def __str__(self):
        return (f"{self.register_entry} | {self.library_entry}")
