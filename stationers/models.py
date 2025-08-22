from django.db import models
from django.utils.translation import gettext_lazy as _


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
        # Find entries with the same title in the collection
        matched_titles = collection_class.objects.filter(
            register=register.id, title__iexact=entry.title)

        for matched_entry in matched_titles:
            # Check if the author also matches for an exact match
            if matched_entry.author.lower() == entry.author.lower():
                _create_match(entry, matched_entry, is_register_entry, "EXC")
            else:
                _create_match(entry, matched_entry, is_register_entry, "PAR")


class Register(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField("register start date")
    end_date = models.DateField("register end date")
    pages = models.IntegerField(default=0)
    file = models.FileField(upload_to="register_pdfs")

    def __str__(self):
        return self.name


class RegisterEntry(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    date = models.DateField("date of entry")
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    volumes = models.CharField(max_length=100, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    register_page = models.IntegerField(default=0)
    confirmed_match = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(RegisterEntry, self).save(*args, **kwargs)
        match_entry(self, LibraryEntry)

    def __str__(self):
        return f"{self.author}: {self.title}"


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


class MatchCandidate(models.Model):

    class MatchType(models.TextChoices):
        EXACT = "EXC", _("Exact match")
        PARTIAL = "PAR", _("Partial match")
        FUZZY = "FUZ", _("Fuzzy match")
        NONE = "NON", _("No match")

    match_type = models.CharField(max_length=3,
                                  choices=MatchType,
                                  default=MatchType.NONE)
    register_entry = models.ForeignKey(RegisterEntry, on_delete=models.CASCADE)
    library_entry = models.ForeignKey(LibraryEntry,
                                      on_delete=models.CASCADE,
                                      null=True)

    def __str__(self):
        return (f"{self.register_entry} | {self.library_entry} |"
                f"{self.library_entry.source_library}")
