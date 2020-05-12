from django.urls  import include, path
from . import views

app_name = 'polls'



urlpatterns = [
    path('', views.index, name='index'),
#    path('welcome', views.welcome, name='welcome'),
#    path('register', views.register, name='register'),    
    path('login', views.login, name='login'),        
    path('logout', views.logout, name='logout'),            

    path('modelolistar/<int:clave1>/', views.modelolistar, name='modelolistar'),
    path('modelomenu/<int:clave1>/', views.modelomenu, name='modelomenu'),    
    
    # menus principales ***************************************************
    path('modeloregistro/<int:clave1>/', views.modeloregistro, name='modeloregistro'),
    path('modelocontrato/<int:clave1>/', views.modelocontrato, name='modelocontrato'),
    path('modelomedicion/<int:clave1>/', views.modelomedicion, name='modelomedicion'),
    path('modeloreparto/<int:clave1>/', views.modeloreparto, name='modeloreparto'),

    path('contratomestabla/<int:clave2>/', views.contratomestabla, name='contratomestabla'),
 
    path('registroaccion/<slug:clave2>/<int:clave3>/', views.registroaccion, name='registroaccion'),
    path('contratoaccion/<slug:clave2>/<int:clave3>/', views.contratoaccion, name='contratoaccion'),    
    path('contratomesaccion/<slug:clave2>/<int:clave3>/', views.contratomesaccion, name='contratomesaccion'),
 
    path('modeloboton1/<slug:clave2>/<slug:clave3>/<int:clave4>/', views.modeloboton1, name='modeloboton1'),
    path('modeloboton2/<slug:clave2>/<slug:clave3>/<int:clave4>/', views.modeloboton2, name='modeloboton2'),
    path('modeloboton3/<slug:clave2>/<int:clave3>/', views.modeloboton3, name='modeloboton3'),
    path('modeloboton4/<slug:clave2>/<int:clave3>/', views.modeloboton4, name='modeloboton4'),

    path('repartocalculo/<slug:clave2>/<slug:clave3>/', views.repartocalculo, name='repartocalculo'),
    path('repartografico/<slug:clave2>/<slug:clave3>/', views.repartografico, name='repartografico'),
    path('repartoexcel/<slug:clave2>/<int:clave3>/', views.repartoexcel, name='repartoexcel'),    
    path('repartopdf/', views.repartopdf, name='repartopdf'),    

]