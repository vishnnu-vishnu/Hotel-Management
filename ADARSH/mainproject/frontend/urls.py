from django.urls import path
from frontend import views

urlpatterns = [
    path('',views.frontpage,name="frontpage"),
    path('menupage/',views.menupage,name="menupage"),
    path('booktable/',views.booktable,name="booktable"),
    path('aboutpage/',views.aboutpage,name="aboutpage"),
    path('loginpage',views.loginpage,name="loginpage"),
    path('signupsave/',views.signupsave,name="signupsave"),
    path('loginuserpage/',views.loginuserpage,name="loginuserpage"),
    path('savetable/',views.savetable,name="savetable"),
    path('cartpage/', views.cartpage, name="cartpage"),
    path('filterpage/<cate>/',views.filterpage,name="filterpage"),
    path('savetocart/', views.savetocart, name="savetocart"),
    path('singleproduct/<int:dataid>/', views.singleproduct, name="singleproduct"),
    path('deletecart/<int:dataid>/', views.deletecart, name="deletecart"),
    path('formfilling/', views.formfilling, name="formfilling"),
    path('saveform/', views.saveform, name="saveform"),
    path('logoutfun/', views.logoutfun, name="logout"),
    path('profilepage/', views.profilepage, name="profilepage"),
    path('editprofile/<int:dataid>/', views.editprofile, name="editprofile"),
    path('updateprofile/<int:dataid>/', views.updateprofile, name="updateprofile"),
    path('savecheckout/', views.savecheckout, name="savecheckout"),
    path('create_order/', views.create_order, name='create_order'),
     path('payment/', views.PaymentCallbackView.as_view(), name='product-list'),
     path('delete_latest_checkout/', views.delete_latest_checkout, name='delete_latest_checkout'),
     path('tracking/', views.tracking, name='tracking'),
     path('signuppage', views.signuppage, name='signuppage'),
     path('submit_review', views.submit_review, name='submit_review'),





]