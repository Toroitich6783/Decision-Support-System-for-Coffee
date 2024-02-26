"""DSSCoffeeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DSSCoffeeAPP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.map.as_view(), name='map'),
    path('MyField',views.MyField.as_view(),name="MyField"),
    path('MyField2',views.MyField2.as_view(),name="MyField2"),
    path('MyField3',views.MyField3.as_view(),name="MyField3"),
    path('Acres',views.Acres.as_view(),name='Acres'),
    path('Hectares',views.Hectares.as_view(),name='Hectares'),
    path('Kilometers',views.Kilometers.as_view(),name='Kilometers'),
    path('areameters',views.areameters.as_view(),name='areameters'),
    path('Sentinel_Imagery',views.Sentinel_Imagery.as_view(),name='Sentinel_Imagery'),
    path('soil',views.soil.as_view(),name='soil'),
    path('NDVI',views.NDVI.as_view(),name='NDVI'),
    path('EVI',views.EVI.as_view(),name='EVI'),
    path('DEM',views.DEM.as_view(),name='DEM'),
    path('LULC',views.LULC.as_view(),name='LULC'), 
    path('Rainfall',views.Rainfall.as_view(),name='Rainfall'),
    path('Temperature',views.Temperature.as_view(),name='Temperature'), 

     

 
     
]
