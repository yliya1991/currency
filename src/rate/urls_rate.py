from django.urls import path

from rate import views

from django.conf.urls import (handler400, handler403, handler404, handler500)

app_name = 'rate'


urlpatterns = [
    path('list/', views.RateList.as_view(), name='list'),
    path('download-csv/', views.RateDownloadCSV.as_view(), name='download-csv'),
    path('download-xlsx/', views.RateDownloadXLSX.as_view(), name='download-xlsx'),
    path('latest-rates/', views.LatestRatesView.as_view(), name='latest-rates'),
]

