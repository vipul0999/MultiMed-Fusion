from django.urls import path
from .views import DoctorChatbotView

urlpatterns = [
    path('doctor-chat/', DoctorChatbotView.as_view(), name='doctor_chat'),
]
