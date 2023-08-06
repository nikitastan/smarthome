from django.urls import path

from measurement.views import SensorAPIView, MeasurementAPIView

urlpatterns = [
    path('sensor/', SensorAPIView.as_view()),
    path('sensor/<int:pk>/', MeasurementAPIView.as_view()),
    path('measurement/', MeasurementAPIView.as_view()),
]