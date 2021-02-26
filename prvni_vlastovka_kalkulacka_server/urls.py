"""prvni_vlastovka_kalkulacka_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from rest_framework import routers

from loans import views
from loans.views import serve_contract
from prvni_vlastovka_kalkulacka_server import settings

admin.site.site_header = _('Project Swallow calculator administration')
admin.site.site_title = _('Project Swallow calculator admin')

router = routers.DefaultRouter()
router.register('', views.ApiLoanOfferViewSet)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(
        template_name='admin/login.html',
        extra_context={
            'title': _('Log in'),
            'site_title': _('Project Swallow calculator admin'),
            'site_header': _('Project Swallow calculator administration'),
        },
    )),
) + [
                  path('media/contracts/<str:filename>', serve_contract),
                  path('api/', include(router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
