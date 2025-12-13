from django.urls import path
from . import views
urlpatterns = [

   path("header/", views.header, name = "header"),

   path("home/", views.home, name = "home"),

   path("generos/", views.generos, name = "generos"),

   path("post/", views.post, name = "post"),

   path("newPost/", views.newPost, name = "newPost"),

   path("nosotros/", views.nosotros, name = "nosotros"),

   path("perfil/", views.perfil, name = "perfil"),

   path("editPerfil/", views.editPerfil, name = "editPerfil"),

   path("sidebar/", views.sidebar, name = "sidebar"),

   path("login/", views.login, name = "login"),

   path("registro/", views.registro, name = "registro"),

   path("cerrarSesion/", views.cerrarSesion, name="cerrarSesion"),

   path('check-session/', views.check_session, name='check_session'),

   path('editPost/<int:post_id>/', views.editPost, name='editPost'),

   path('elimPost/<int:post_id>/', views.elimPost, name='elimPost'),

]