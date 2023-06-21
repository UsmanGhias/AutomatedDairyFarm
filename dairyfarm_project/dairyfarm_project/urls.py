from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.views import CowViewSet, FarmViewSet, MilkProductionReportView
from django.conf import settings
from django.conf.urls.static import static





from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
router = routers.DefaultRouter()
router.register('cows', CowViewSet, basename='cow')
router.register('farms', FarmViewSet, basename='farm')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include('api.urls')),  # Include the DRF URLs here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
