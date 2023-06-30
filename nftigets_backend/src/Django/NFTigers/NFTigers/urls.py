"""NFTigers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from nfts.views import NftsApiView, CategoriesApiView, SchoolClassApiView
from auctions.views import AuctionsApiView
from users.views import UsersApiView, WalletApiView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auctions/', AuctionsApiView.as_view()),
    path('api/nfts/', NftsApiView.as_view()),
    path('api/users/', UsersApiView.as_view()),
    path('api/wallet/', WalletApiView.as_view()),
    path('api/categories/', CategoriesApiView.as_view()),
    path('api/classes/', SchoolClassApiView.as_view())
]
