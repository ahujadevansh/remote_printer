from django.urls import path
from . import views as printer_views

app_name = 'printer'

urlpatterns = [

    path('print-request-create/', printer_views.PrintRequestCreateView.as_view(), name='print_request_create'),
    path('print-request-permanent-delete/<int:pk>/', printer_views.PrintRequestDeleteView.as_view(),
         name='print_request_permanent_delete'),
    path('print-request-delete/<int:pk>/', printer_views.PrintRequestSoftDeleteView.as_view(),
         name='print_request_delete'),
    path('print-request-cancel/<int:pk>/', printer_views.PrintRequestCancelView.as_view(),
         name='print_request_cancel'),
    path('print-request-reject/<int:pk>/', printer_views.PrintRequestRejectView.as_view(),
         name='print_request_reject'),
    path('print-request-reapply/<int:pk>/', printer_views.PrintRequestReapplyView.as_view(),
         name='print_request_reapply'),

    path('user-print-request-list/<str:status>/', printer_views.UserPrintRequestListView.as_view(flag=1),
         name='user_print_request_list'),
    path('user-print-request-list-table/<str:status>/', printer_views.UserPrintRequestListView.as_view(flag=0),
         name='user_print_request_list_table'),
    path('user-print-request/<int:pk>/', printer_views.UserPrintRequestDetailView.as_view(),
         name='user_print_request_detail'),


    path('staff-print-request-list/<str:status>/', printer_views.StaffPrintRequestListView.as_view(),
         name='staff_print_request_list'),
    path('staff-print-request-list-table/<str:status>/', printer_views.StaffPrintRequestListView.as_view(flag=0),
         name='staff_print_request_list_table'),
    path('staff-print-request/<int:pk>/', printer_views.StaffPrintRequestDetailView.as_view(),
         name='staff_print_request_detail'),
]
