from django.urls import path
from backend import views

urlpatterns = [

    path('home/',views.home,name="home"),
    path('category/',views.category,name="category"),
    path('savecategory/',views.savecategory,name="savecategory"),
    path('display/',views.display,name="display"),
    path('saveproducts/',views.saveproducts,name="saveproducts"),
    path('product/',views.product,name="product"),
    path('deletepro/<int:dataid>/',views.deletepro,name="deletepro"),
    path('editpro/<int:dataid>/', views.editpro, name="editpro"),
    path('updatepro/<int:dataid>/', views.updatepro, name="updatepro"),
    path('addtable/', views.addtable, name="addtable"),
    path('updatestatus/<int:dataid>/', views.updatestatus, name="updatestatus"),
    path('display_tablebooking/', views.display_tablebooking, name="display_tablebooking"),
    path('display_rating/', views.display_rating, name="display_rating"),






]