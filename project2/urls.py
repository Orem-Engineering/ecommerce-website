
from django.contrib import admin
from django.urls import path,include
# media imports 
from django.conf.urls.static import static
from django.conf import settings
# Admin site header and tittle
admin.site.site_header = "OREM ECCOMERCE STORE"
admin.site.site_title=" OREM STORE ADMIN"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),
    path('baseauthentication/',include('baseauthentication.urls'))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
