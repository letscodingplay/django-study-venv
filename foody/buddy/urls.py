from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("show", views.ShowMonth.as_view(), name="show_month"),
    path("show/day", views.ShowDay.as_view(), name="show_day"),
    path("barcode", views.getBarcodeData.as_view()),
]