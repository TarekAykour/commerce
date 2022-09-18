from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("deletewatchlist/<int:id>", views.deletewatchlist, name="deletewatchlist"),
    path("addbid/<int:id>", views.addbid, name="addbid"),
    path("addcomment/<int:id>",views.addcommment,name="addcomment"),
    path("categories", views.categories, name="categories"),
    path("closeauction/<int:id>", views.closeauction, name="closeauction"),
    path("openauction/<int:id>", views.openauction, name="openauction"),
    path("deleteauction/<int:id>", views.deleteauction, name="deleteauction"),
    path("searchcategory", views.categories, name="searchcategory")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
