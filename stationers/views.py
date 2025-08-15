from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Register, Entry


class IndexView(generic.ListView):
    template_name = "stationers/index.html"
    context_object_name = "register_list"

    def get_queryset(self):
        return Register.objects.order_by("-register_start_date")


def register_detail(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    n_register_entries = len(Entry.objects.filter(register=register_id))
    context = {"register": register, "entries": n_register_entries}
    return render(request, "stationers/register_detail.html", context)


def entry_list(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    register_entries = Entry.objects.filter(register=register_id)
    context = {"register": register, "entries": register_entries}
    return render(request, "stationers/entry_list.html", context)
