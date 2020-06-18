from django.urls import path, include
from .views import ItemListAdd, ItemRUD
from django.conf import settings
from django.conf.urls.static import static

app_name = "post"

urlpatterns = [
    path("item/", ItemListAdd.as_view(), name="item_add_list"),
    path("item/<str:itemId>/", ItemRUD.as_view(), name="item_rud"),
]
# Adding static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
