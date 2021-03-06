"""dyplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .view import load_state, main, word, words, settings as sett

urlpatterns = [
    url(r'^$', main),
    url(r'^load_state$', load_state),
    url(r'^words$', words),
    url(r'^word$', word),
    url(r'^settings$', sett),
    url(r'^admin/', admin.site.urls),
    url(r'^lemmatize/', include('lemmatize.urls')),
    url(r'^timing/', include('timing.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
