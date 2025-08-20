from django.urls import path

from . import views

app_name = "stationers"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:register_id>/", views.register_detail, name="detail"),
    path("<int:register_id>_all/", views.entry_list, name="entry_list"),
    path("<int:register_id>_associated/", views.associated_library_entry_list,
         name="library_entry_list"),
    path("<int:register_id>_matches/", views.match_list, name="match_list"),
]
