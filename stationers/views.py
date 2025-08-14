from django.shortcuts import get_object_or_404, render

from .models import Register, Entry


def index(request):
    register_list = Register.objects.order_by("-register_start_date")

    context = {"register_list": register_list}
    return render(request, "stationers/index.html", context)


def register_detail(request, register_id):
    register = get_object_or_404(Register, pk=register_id)
    register_entries = Entry.objects.filter(register=register_id)
    return render(request, "stationers/register_detail.html",
                  {"register": register, "entries": register_entries})
