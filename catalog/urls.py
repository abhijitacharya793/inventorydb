from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('manufacturers/', views.ManufacturerListView.as_view(), name='manufacturers'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('manufacturer/<int:pk>', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),
]

urlpatterns += [
    path('myitems/', views.LoanedItemsByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('item/<uuid:pk>/renew/', views.renew_item_inventoryhead, name='renew-book-inventoryhead'),
]

urlpatterns += [
    path('manufacturer/create/', views.ManufacturerCreate.as_view(), name='manufacturer_create'),
    path('manufacturer/<int:pk>/update/', views.ManufacturerUpdate.as_view(), name='manufacturer_update'),
    path('manufacturer/<int:pk>/delete/', views.ManufacturerDelete.as_view(), name='manufacturer_delete'),
]
