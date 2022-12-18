from django.urls import path
from .views import (
    InstanceUpdateView,
    ProcessCreateListView,
    TicketCreateListView,
)

urlpatterns = [
    path('process', ProcessCreateListView.as_view(), name='process-list-create'),
    path('ticket', TicketCreateListView.as_view(), name='ticket-list-create'),
    path('instance/<int:pk>', InstanceUpdateView.as_view(), name='instance-update-view')
]
