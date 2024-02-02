from django.shortcuts import render
from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView 

import matplotlib.pyplot as plt
colormaps=plt.cm.datad.keys()

#Importation of variAous Libraries or packages...
from os import path as op
import geemap
import ee
import folium
import geemap.foliumap as geemap
# import matplotlib.pyplot as plt
from django.http import HttpResponse
from folium import plugins
from folium.plugins import Draw

from .forms import DateForm
from datetime import datetime

# Create your views here.
#HomeMap
class map(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()   
        Map = geemap.Map()
        Map.add_to(figure)
        Map.set_center(36.4335, -0.1131, 12)
        
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
 

        global basemaps
        basemaps = {
        'Google Maps': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Maps',
                overlay = False,
                control = True
                ),
                'Esri Satellite': folium.TileLayer(
                tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr = 'Esri',
                name = 'Esri Satellite',
                overlay = True,
                control = True
                ),'Google Satellite Hybrid': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Satellite',
                overlay = False,
                control = True
                ), 
                }     
        basemaps['Google Satellite Hybrid'].add_to(Map)
        basemaps['Esri Satellite'].add_to(Map)
             
        Map.add_child(folium.LayerControl())
        figure.render()
        context['map'] = figure
        return context
    
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

# Test Fields:
#ROI: MyField2
class MyField(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Homa_Bay")
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")
            legend_dict = {
                        'ROI Boundary': '000000',
            }
            Map.add_legend(title="Region of Intrest", legend_dict=legend_dict)  
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded  Homa Bay ROI"
                context['sucess_message'] = sucess_message

        Map.add_child(folium.LayerControl())
        figure.render()
        
        context['MyField'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

#ROI: MyField2
class MyField2(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Siaya")
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")
            legend_dict = {
                        'ROI Boundary': '000000',
            }
            Map.add_legend(title="Region of Intrest", legend_dict=legend_dict)  
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Siaya ROI"
                context['sucess_message'] = sucess_message
                

        Map.add_child(folium.LayerControl())
        figure.render()
        
        context['MyField2'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
#ROI: MyField2
class MyField3(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Homa_Bay")
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")
            legend_dict = {
                        'ROI Boundary': '000000',
            }
            Map.add_legend(title="Region of Intrest", legend_dict=legend_dict)  
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded  Homa Bay ROI"
                context['sucess_message'] = sucess_message

        Map.add_child(folium.LayerControl())
        figure.render()
        
        context['MyField3'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

# Area Estimation: Meters
class areameters(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated areas(Acres)', Total_AreaSqKm.getInfo())
        
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['areameters'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Acres
class Acres(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField") 
         
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(4046.86).round()
        print('Estimated areas(Acres)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Acres'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Hectares
class Hectares(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(10000).round()
        print('Estimated areas(Hectares)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Hectares'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

# Area Estimation: Kilometers
class Kilometers(TemplateView):
    ee.Initialize()
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        
        Map.center_object(boundary,9);
        Map.addLayer(boundary,{},"MyField")
          
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).divide(1000000).round()
        print('Estimated areas(KM)', Total_AreaSqKm.getInfo())
        
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Kilometers'] = figure
        return context
    def get(self, request, pk=''):
            form = DateForm()
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
            form = DateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                start_date = datetime.strftime(start, "%Y-%m-%d")
                end_date = datetime.strftime(end, "%Y-%m-%d")
                print(start_date)
                print(end_date)
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)
            
#Sentinel 2A Data.
class Sentinel_Imagery(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
        # GPS
        plugins.LocateControl().add_to(Map)
        #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)
        try:
            global boundary
            Map.center_object(boundary,9);
            Map.addLayer(boundary,{},"ROI")

            Map.addLayer(boundary,{},"Boundary")
        
            Map.center_object(boundary,9);
            
            global season
            season = ee.Filter.date(start_date,end_date);#Filter image based on the time frame(start_date and end_date)
 #-------------SENTINEL_2A DATA----------------------#  
            global sentinel_2A
            sentinel_2A = ee.ImageCollection('COPERNICUS/S2')\
            .filterBounds(boundary)\
            .filter(season)\
            .median()\
            .select('B1','B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8', 'B10', 'B11')\
            .clip(boundary)
            
            sentinel_2Avispar={"min":0, "max":4000,"bands": ['B4','B3','B2']}#Visualization parameters used.

            Map.addLayer(sentinel_2A,sentinel_2Avispar,"Sentinel Imagery")
                    
        
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded Sentinel 2A for your region"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['Sentinel_Imagery'] = figure
        return context
    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


#1). Soil Type
class soil(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
        Map.set_center(-7.799, 53.484, 7)
 #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
      #Add GPS (Global Postion System)
        plugins.LocateControl().add_to(Map)
 #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        # try:  
            
        # Map.centerObject(boundary,17)
        
        GeologicalMap=ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Ireland_SoilData")
        Map.centerObject(GeologicalMap,12)
        states = GeologicalMap

        vis_params = {
            'color': '000000', 
            'colorOpacity': 1,
            'pointSize': 3,
            'pointShape': 'circle',
            'width': 2,
            'lineType': 'solid', 
            'fillColorOpacity': 1
        }

        palette = [       
                '0000FF', '008000', 'FF0000', 'FFA500', '800080',
                            '00FFFF', 'FFC0CB', 'FFFF00', 'A52A2A'
                ]
        # Map
        # Convert the Earth Engine FeatureCollection to GeoJSON
        geojson_data = GeologicalMap.getInfo()
        Map.add_styled_vector(states, column="Name", palette=palette, layer_name="Soil Type", **vis_params)


        # Add GeoJSON layer to the map with GeoJsonTooltip
        folium.GeoJson(
            geojson_data,
            name='Soils Map',
            tooltip=folium.GeoJsonTooltip(fields=['Name'], labels=True, sticky=False),
            style_function=lambda feature: {
            'fillColor': 'green',  # Set the fill color
            'color': 'none',      # Set the border color
            'weight': 0,           # Set the border weight
            'fillOpacity': 0     # Set the fill opacity
        }
        ).add_to(Map)


        
        #Adding legend:
        legend_dict = {
            'Sand Loam': 'blue',
            'Loam': 'green',
            'Clay Loam': 'red',
            'Loam': 'orange',
            'Water': 'purple',
            'Loam': 'orange',
            'Loam': 'yellow',
            'Sandy Loam': 'purple',
            'Laom': 'cyan',
            }
        Map.add_legend(title="Soil Type ♠", legend_dict=legend_dict)
                
        # except Exception as e:
        #     # Handle the exception. You can customize this part based on how you want to display the error.
        #     error_message = f"An error occurred:Please review the previous steps!!!"
        #     context['error_message'] = error_message
        # else:
        #         success_message = f"Soil Type Runned Successfully for Your Region"
        #         context['success_message'] = success_message
        Map.add_child(folium.LayerControl())
        figure.render()
        context['soil'] = figure
        context['form'] = DateForm()
        return context
    def post(self, request, pk=''):
        form = DateForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            global start_date
            start_date = datetime.strftime(start, "%Y-%m-%d")
            global end_date
            end_date = datetime.strftime(end, "%Y-%m-%d")
            print(start_date)
            print(end_date)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    def get(self, request, pk=''):
        form = DateForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)