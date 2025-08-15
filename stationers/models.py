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
    entry_date = models.DateField("date of entry")
    entry_author = models.CharField(max_length=100)
    entry_title = models.CharField(max_length=500)
    entry_volumes = models.CharField(max_length=100, blank=True)
    entry_edition = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.entry_author}: {self.entry_title}"
