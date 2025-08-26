from django.db import models
from django.utils.translation import gettext_lazy as _
import logging

from thefuzz import fuzz

logger = logging.getLogger(__name__)


def _create_match(entry, matched_entry, is_register_entry, match_type):
    """
    Helper function to create a Match object.
    """
    if is_register_entry:
        entries_dict = {
            'register_entry': entry,
            'library_entry': matched_entry
        }
    else:
        entries_dict = {
            'register_entry': matched_entry,
            'library_entry': entry
        }
    MatchCandidate.objects.get_or_create(match_type=match_type, **entries_dict)


def match_entry(entry, collection_class):
    """
    Finds and creates matches for a given entry in a collection.
    """
    registers = []
    is_register_entry = True

    if isinstance(entry, LibraryEntry):
        registers.extend(entry.register.all())
        is_register_entry = False
    elif isinstance(entry, RegisterEntry):
        registers.append(entry.register)

    for register in registers:
        relevant_entries = collection_class.objects.filter(
            register=register.id)
        scores = [{
            "id":
            collection_entry.id,
            "title_score":
            fuzz.ratio(entry.title, collection_entry.title),
            "author_score":
            fuzz.ratio(entry.author, collection_entry.author)
        } for collection_entry in relevant_entries]

        # Find entries with the same title in the collection
        matched_titles = list(filter(lambda s: s["title_score"] == 100,
                                     scores))

        for matched_entry in matched_titles:
            # Check if the author also matches for an exact match
            if matched_entry["author_score"] == 100:
                _create_match(entry,
                              relevant_entries.get(pk=matched_entry["id"]),
                              is_register_entry, "EXC")
            else:
                _create_match(entry,
                              relevant_entries.get(pk=matched_entry["id"]),
                              is_register_entry, "PAR")

        # Find entries with similar title
        unmatched_titles = list(
            filter(lambda s: s not in matched_titles, scores))
        match_threshold = 80
        fuzzy_titles = list(
            filter(lambda s: s["title_score"] > match_threshold,
                   unmatched_titles))
        for matched_entry in fuzzy_titles:
            # Check if the author also similar
            if matched_entry["author_score"] > match_threshold:
                _create_match(entry,
                              relevant_entries.get(pk=matched_entry["id"]),
                              is_register_entry, "FUZ")
            else:
                _create_match(entry,
                              relevant_entries.get(pk=matched_entry["id"]),
                              is_register_entry, "FZP")
        logger.debug(f"Entry: {entry}")
        logger.debug(f"Relevant collection entries: {relevant_entries}")
        logger.debug(f"All scores: {scores}")
        logger.debug(f"Matched titles: {matched_titles}")
        logger.debug(f"Unmatched titles: {unmatched_titles}")
        logger.debug(f"fuzzy titles: {fuzzy_titles}")


class Register(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField("register start date")
    end_date = models.DateField("register end date")
    pages = models.IntegerField(default=0)
    file = models.FileField(upload_to="register_pdfs")

    def __str__(self):
        return self.name


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
    date = models.DateField("date of entry")
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    volumes = models.CharField(max_length=100, blank=True)
    edition = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(LibraryEntry, self).save(*args, **kwargs)
        match_entry(self, RegisterEntry)

    def __str__(self):
        return f"{self.author}: {self.title}"


class RegisterEntry(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    date = models.DateField("date of entry")
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    volumes = models.CharField(max_length=100, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    register_page = models.IntegerField(default=0)
    human_checked = models.BooleanField(default=False)
    library_entry = models.ForeignKey(LibraryEntry,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)

    def save(self, *args, **kwargs):
        super(RegisterEntry, self).save(*args, **kwargs)
        match_entry(self, LibraryEntry)

    def __str__(self):
        return f"{self.author}: {self.title}"


class MatchCandidate(models.Model):

    class MatchType(models.TextChoices):
        EXACT = "EXC", _("Exact match")
        PARTIAL = "PAR", _("Partial match")
        FUZZY = "FUZ", _("Fuzzy match")
        FUZPA = "FZP", _("Fuzzy partial match")
        NONE = "NON", _("No match")

    match_type = models.CharField(max_length=3,
                                  choices=MatchType,
                                  default=MatchType.NONE)
    register_entry = models.ForeignKey(RegisterEntry, on_delete=models.CASCADE)
    library_entry = models.ForeignKey(LibraryEntry,
                                      on_delete=models.CASCADE,
                                      null=True)
    human_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(MatchCandidate, self).save(*args, **kwargs)
        if (self.human_checked and not self.register_entry.human_checked
                and self.match_type != self.MatchType.NONE):
            self.register_entry.human_checked = True
            self.register_entry.library_entry = self.library_entry
            self.register_entry.save()
        elif not self.human_checked and self.register_entry.human_checked:
            self.register_entry.human_checked = False
            self.register_entry.library_entry = None
            self.register_entry.save()

    def __str__(self):
        return (f"{self.register_entry} | {self.library_entry} |"
                f"{self.library_entry.source_library}")
