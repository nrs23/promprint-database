from django.urls import path

from . import views

app_name = "stationers"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:register_id>/", views.register_detail, name="detail")
]
