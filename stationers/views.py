from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Register, Entry, LibraryEntry, Matches


class IndexView(generic.ListView):
    template_name = "stationers/index.html"
    context_object_name = "register_list"

    def get_queryset(self):
        return Register.objects.order_by("-start_date")


def register_detail(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    register_entries = Entry.objects.filter(register=register_id)
    for entry in register_entries:
        entry.match_entry()
    n_register_entries = len(register_entries)
    n_library_entries = len(LibraryEntry.objects.filter(register=register_id))
    n_matches = len(
        Matches.objects.filter(register_entry__register=register_id))
    context = {
        "register": register,
        "n_entries": n_register_entries,
        "n_library_entries": n_library_entries,
        "n_matches": n_matches,
    }
    return render(request, "stationers/register_detail.html", context)


def entry_list(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    register_entries = Entry.objects.filter(register=register_id)
    context = {"register": register, "entries": register_entries}
    return render(request, "stationers/entry_list.html", context)


def associated_library_entry_list(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    library_entries = LibraryEntry.objects.filter(register=register_id)
    context = {"register": register, "library_entries": library_entries}
    return render(request, "stationers/associated_library_entry_list.html",
                  context)


def match_list(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    register_matches = Matches.objects.filter(
        register_entry__register=register_id)
    context = {"register": register, "matches": register_matches}
    return render(request, "stationers/match_list.html", context)
