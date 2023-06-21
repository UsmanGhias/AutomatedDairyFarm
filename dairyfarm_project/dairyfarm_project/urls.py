
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.views import CowViewSet, FarmViewSet, MilkProductionReportView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = routers.DefaultRouter()
router.register('cows', CowViewSet, basename='cow')
router.register('farms', FarmViewSet, basename='farm')




urlpatterns = [
    path('api/', include(router.urls)),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/', admin.site.urls)
   

    #path('reports/milk-production/', MilkProductionReportView.as_view(), name='milk_production_report'),
    
]