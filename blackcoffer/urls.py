from django.urls import path

from blackcoffer import views
from blackcoffer.views import ChartDataView

urlpatterns = [
    path('data/', views.get_data, name='get_data'),
    path('country_plot/', views.country_plot, name='country-plot'),
    path('get_charts/', ChartDataView.as_view(), name='chart-data'),
]
