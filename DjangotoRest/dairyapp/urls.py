from django.urls import path, include
from dairyapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Vendor URLs
    path('api/addvendor/', views.AddVendorView.as_view(), name='addvendor'),
    path('api/vendors/', views.AllVendorView.as_view(), name='allvendor'),
    path('api/ledger/<int:pk>/', views.LedgerView.as_view(), name='ledger'),
    path('api/ledger/', views.LedgerSaveView.as_view(), name='ledger_save'),
    path('api/ledger/<int:pk>/delete/', views.LedgerDeleteView.as_view(), name='ledger_delete'),

    # Customer URLs
    path('api/addcustomer/', views.AddCustomerView.as_view(), name='addcustomer'),
    path('api/customers/', views.AllCustomerView.as_view(), name='allcustomer'),
    path('api/customer_ledger/<int:pk>/', views.CustomerLedgerView.as_view(), name='customer_ledger'),
    path('api/customer_ledger/', views.CustomerLedgerSaveView.as_view(), name='customer_ledger_save'),
    path('api/customer_ledger/<int:pk>/delete/', views.CustomerLedgerDeleteView.as_view(), name='customer_ledger_delete'),
    path('api/customer_page/', views.CustomerPageView.as_view(), name='customer_page'),
]
