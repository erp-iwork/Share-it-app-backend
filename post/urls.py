from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from post import views

app_name = "post"

urlpatterns = [
    path("item/", views.ItemListAdd.as_view(), name="item_add_list"),
    path("item/<str:itemId>/", views.ItemRUD.as_view(), name="item_rud"),
    path("my_items/", views.UserItemList.as_view(), name="my_items"),
    path("items", views.ItemFilterView.as_view(), name="category_items"),
    path("item_property", views.PropertyFilterView.as_view(), name="properties_items"),
    path("category/", views.CategoryList.as_view(), name="category"),
]
# Adding static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
