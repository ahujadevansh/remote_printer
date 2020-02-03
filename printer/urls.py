from django.urls import path
from . import views as printer_views

app_name = 'printer'

urlpatterns = [

    path('print-request-create/', printer_views.PrintRequestCreateView.as_view(), name='print_request_create'),
    path('user-print-request-list/', printer_views.UserPrintRequestListView.as_view(), name='user_print_request_list'),
    path('print-request/<int:pk>/', printer_views.UserPrintRequestDetailView.as_view(),
         name='print_request_detail'),
    path('print-request-delete/<int:pk>/', printer_views.PrintRequestSoftDeleteView.as_view(),
         name='print_request_delete'),
    path('print-request-cancel/<int:pk>/', printer_views.PrintRequestCancelView.as_view(),
         name='print_request_cancel'),
    path('print-request-reject/<int:pk>/', printer_views.PrintRequestRejectView.as_view(),
         name='print_request_reject'),
    path('print-request-reapply/<int:pk>/', printer_views.PrintRequestReapplyView.as_view(),
         name='print_request_reapply'),
]
