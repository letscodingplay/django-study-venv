from django.urls import path

from . import views

app_name='buddy'

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("show", views.AskBirth.as_view(), name="ask_birth"),
    path("show/score/<int:pk>", views.ShowScore.as_view(), name="show"),
    path("barcode", views.getBarcodeData.as_view()),
    path("insert", views.Insert.as_view(), name="insert"),
    path("show/all", views.ShowAll.as_view(), name="all"),
]