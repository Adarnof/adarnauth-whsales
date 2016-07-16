"""whsales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from whsales import views

urlpatterns = [
    url(r'^$', views.listings_panel, name='listings_panel'),
    url(r'^admin/', admin.site.urls),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^list$', views.listings_list, name='listings_list'),
    url(r'^list/me$', views.my_listings, name='user_listings'),
    url(r'^listing/(\d*)$', views.listing_view, name='listing_view'),
    url(r'^listing/(\d*)/sell$', views.mark_sold, name='mark_sold'),
    url(r'^listing/(\d*)/delete$', views.delete_listing, name='delete_listing'),
    url(r'^sold$', views.listings_sold, name='listings_sold'),
    url(r'^tokens$', views.select_token, name='select_token'),
    url(r'^tokens/add$', views.add_token, name='add_token'),
    url(r'^tokens/(\d*)/post$', views.post_listing, name='add_listing'),
    url(r'^search$', views.search, name='search'),
    url(r'^about$', views.about, name='about'),
    url(r'^eve_sso/', include('eve_sso.urls')),
]

