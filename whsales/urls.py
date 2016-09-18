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
    url(r'^$', views.listings_list, name='listings_panel'),
    url(r'^admin/', admin.site.urls),
    url(r'^me$', views.my_listings, name='user_listings'),
    url(r'^listing/(\d*)$', views.listing_view, name='listing_view'),
    url(r'^listing/(\d*)/sell$', views.mark_sold, name='mark_sold'),
    url(r'^listing/(\d*)/delete$', views.delete_listing, name='delete_listing'),
    url(r'^sold$', views.listings_sold, name='listings_sold'),
    url(r'^post$', views.post_listing, name='add_listing'),
    url(r'^search$', views.search, name='search'),
    url(r'^about$', views.about, name='about'),
    url(r'^wanted$', views.wanted_list, name='wanted_panel'),
    url(r'^wanted/add$', views.add_wanted, name='add_wanted'),
    url(r'^wanted/me$', views.my_wanted, name='user_wanted'),
    url(r'^wanted/(\d*)$', views.wanted_view, name='wanted_view'),
    url(r'^wanted/(\d*)/fulfill$', views.fulfill_wanted, name='mark_fulfilled'),
    url(r'^wanted/(\d*)/delete$', views.delete_wanted, name='delete_wanted'),
    url(r'^core/', include('singlecharcore.urls')),
]

