


from os import name
from django.urls import path
from .views import display, process_image, registerPage,loginPage,logoutUser 
urlpatterns = [
    path('register/',registerPage, name="register"),
	path('login/',loginPage, name="login"),  
	path('logout/',logoutUser, name="logout"),
    path('', display , name='display'),
    path('result/', process_image , name='result'),
    # path("pdfFile/", pdfFile , name="pdfFile"),
]

