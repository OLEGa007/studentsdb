"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from students import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from .settings import DEBUG

from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.groups import GroupUpdateView, GroupAddView
from students.views.journal import JournalView
from students.views.contact_admin import ContactAdmin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jsi18n/.js$', JavaScriptCatalog.as_view(packages=['students']), name='javascript_catalog'),

    # Students urls
    url(r'^$', views.students_list, name='students_list'),
    url(r'^add/$', views.students_add, name='students_add'),
    url(r'^(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
        name='students_edit'),
    url(r'^(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(),
        name='students_delete'),

    # Groups urls
    url(r'^groups/$', views.groups_list, name='groups_list'),
    url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(),\
        name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', views.groups_delete,
        name='groups_delete'),

    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    # Contact Admin Form
    # url(r'^contact_admin/$', views.contact_admin, name='contact_admin'),
    url(r'^contact_admin/$', ContactAdmin.as_view(), name='contact_admin'),

    # User Related urls
    url(r'^users/logout/$',
        auth_views.logout,
        kwargs={'next_page': 'students_list'},
        name='auth_logout'),
    url(r'^register/complete/$',
        RedirectView.as_view(pattern_name='students_list'),
        name='registration_complete'),
    url(r'^users/', include('registration.auth_urls')),
    url(r'^users/',
        include('registration.backends.simple.urls',
                namespace='users')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if DEBUG:
    # serve files from media folder
    # urlpatterns += ['', url(r'^media/(?P<path>.*)$',
    # django.views.static.serve, {'document_root' : MEDIA_ROOT})]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
