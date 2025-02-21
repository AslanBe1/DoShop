from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from config import settings
from config.settings import MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Uzum/', include('shops.urls'), name='shops'),
    path('Customers/', include('customers.urls')),
    path('user/', include('User.urls'), name='users'),
    path('social-auth/',
         include('social_django.urls', namespace='social'))

] + static(MEDIA_URL, document_root=settings.MEDIA_ROOT)
