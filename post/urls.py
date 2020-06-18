from django.urls import path, include
from post import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "post"

urlpatterns = [
    path("item/", views.ItemListAdd.as_view(), name="item_add_list"),
    path("item/<str:itemId>/", views.ItemRUD.as_view(), name="item_rud"),
    path("my-items/", views.UserItemList.as_view(), name="my_items"),
    path("items", views.ItemFilterView.as_view(), name="category_items"),
    path("item-property", views.PropertyFilterView.as_view(), name="properties_items"),
]
# Adding static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
