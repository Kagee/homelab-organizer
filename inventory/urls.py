from django.urls import path

from .import views
from .views import StockItemCreate, StockItemDetail, StockItemList

urlpatterns = [
    path("", views.index, name="inventory-index"),
    path('stockitem/create', StockItemCreate.as_view(), name="stockitem-create"),
    path('stockitem/detail/<int:pk>', StockItemDetail.as_view(), name="stockitem-detail"),
    path('stockitem/list', StockItemList.as_view(), name="stockitem-list"),
    path('stockitem/create/<str:id_orderitems>',
         StockItemCreate.as_view(),
         name="stockitem-create-from"
         ),
]
