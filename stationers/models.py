from django.db import models


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
