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
        Map.set_center(35.4066, -0.1566, 12)
        
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
        ###############################################################################
        #############################Test inputs#######################################
        ###############################################################################
        global boundary
        boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Kipkelion_west")
        global start_date
        start_date="2020-01-01"#Set start_date(yy/mon/day)
        global end_date
        end_date="2020-03-31"#Set End_date(yy/mon/day)

        season = ee.Filter.date(start_date,end_date);#Filter image based on the time frame(start_date and end_date)
        global sentinel_2A
        sentinel_2A = ee.ImageCollection('COPERNICUS/S2')\
        .filterBounds(boundary)\
        .filter(season)\
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE",10))\
        .median()\
        .select('B1','B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8', 'B10', 'B11')\
        .clip(boundary)

        ###############################################################################
        #############################End Test inputs#######################################
        ###############################################################################
             
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
            boundary = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Kipkelion_west")
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


#Normalized Difference Vegetation Index: NDVI.
class LULC(TemplateView):
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
        # try:
        Map.center_object(boundary,9);
        
        global season
        season = ee.Filter.date(start_date,end_date);#Filter image based on the time frame(start_date and end_date)
#-------------SENTINEL_2A DATA----------------------#  
        Fused_images = sentinel_2A#Creation of composite image of sentinel 1 and sentinel 2A
        fused_vis = {
        'min':0,
        'max'  : 2500,
        'bands' : ['B2', 'B3','B4']#Band selection.
        }
        
        feature_collection = ee.FeatureCollection("projects/ee-mosongjnvscode/assets/KipkelionWtraining_points")
        training = ee.FeatureCollection(feature_collection)
        #Create a buffer:
        buffered_data = training.map(lambda f: f.buffer(5))
        # Map.addLayer(training1,{},"buffer")
        label = 'cropland'#Unique property(cropland) with different unique values..
        bands=["B4","B3","B2"]
        global Input
        Input=Fused_images.select(bands)
        trainImage=Input.sampleRegions(**{
        'collection':training,
        'properties':[label],
        'scale':10
        })

        trainingData=trainImage.randomColumn()

        trainSet=trainingData.filter(ee.Filter.lessThan('random',0.75))
        testdata=trainingData.filter(ee.Filter.greaterThanOrEquals('random',0.75))


        #visualization parameters applied on the Random forest classifier

        init_params = {"numberOfTrees":10, # the number of individual decision tree models
        "variablesPerSplit":None,  # the number of features to use per split
        "minLeafPopulation":1, # smallest sample size possible per leaf
        "bagFraction":0.5, # fraction of data to include for each individual tree model
        "maxNodes":None, # max number of leafs/nodes per tree
        "seed":0}  # random seed for "random" choices like sampling. Setting this allows others to reproduce your exact results even with stocastic parameters
        global classifier

        classifier = ee.Classifier.smileRandomForest(**init_params).train(trainImage, label, bands)
        # Classify the image.

        #Application of the random forest classifier for the purpose of image classification.
        global classified
        classified=Input.classify(classifier)
        palette = [
 'green',#//Forest(0)
  'yellow', #//Bareland(1)
  'brown',#//Coffee(2)
  'black',#//Settlements(3)
  'gray', #Grassland(4)
        ];
        Map.addLayer(classified,
        {'min': 0, 'max': 4, 'palette': palette},
        'classification')


        legend_dict = {
        'Forest': 'green',
        'Bareland':'yellow',
        'Coffee':'brown',
        'Settlement':'black',
        'Grassland':'gray',
   

        }
        Map.add_legend(title="Classification💥", legend_dict=legend_dict)
                
        Total_studyArea = boundary.geometry().area()
        Total_AreaSqKm = ee.Number(Total_studyArea).round()
        print('Estimated Total areas', Total_AreaSqKm.getInfo())
        # except Exception as e:
        #     # Handle the exception. You can customize this part based on how you want to display the error.
        #     error_message = f"An error occurred:Please review the previous steps!!!!"
        #     context['error_message'] = error_message
        # else:
        #         sucess_message = f"Succefully loaded LULC for your ROI"
        #         context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['LULC'] = figure
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
            


#Normalized Difference Vegetation Index: NDVI.
class NDVI(TemplateView):
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
    
            global NDVI
            NDVI = sentinel_2A.normalizedDifference(['B8', 'B4'])#normalized difference is computed as (first − second) / (first + second).
            ndvivis_parametres = {'min':0, 'max':1, 'palette': ['FFFFFF','FF0000','FFFF00','008000', '006400','00FFFF','0000FF'] }#NDVI visualization parameters
            Map.addLayer(NDVI, ndvivis_parametres, 'NDVI(Normalized Difference Vegetation Index)')#Add Normalized Difference Vegetation Index to the layers
        
            vis_params = {
                'min': 0,
                'max': 1,
                'palette':['FFFFFF','FF0000','FFFF00','008000', '006400','00FFFF','0000FF'],
            }
            Map.add_colorbar(vis_params,label='Crop Health Analysis')
            legend_dict = {
                    'Non Vegatation(-1 to 0):': 'FF0000',
                    'Low Vegetation (0 to 0.2):': 'A52A2A',
                    'Moderate Vegetation (0.2 to 0.5):': 'FFFF00',
                    'High Vegetation (0.5 to 1):': '008000',}
            Map.add_legend(title="NDVI Legend", legend_dict=legend_dict)  
                    
            Total_studyArea = boundary.geometry().area()
            Total_AreaSqKm = ee.Number(Total_studyArea).round()
            print('Estimated Total areas', Total_AreaSqKm.getInfo())
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!!"
            context['error_message'] = error_message
        else:
                sucess_message = f"Succefully loaded NDVI for your ROI"
                context['sucess_message'] = sucess_message
            
        
        Map.add_child(folium.LayerControl())
        figure.render()
        areaestimate1=Total_AreaSqKm.getInfo()
        
        context['areaestimate1'] = areaestimate1
        context['NDVI'] = figure
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
            

#2). Enhanced Vegetation Index: EVI.
class EVI(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
  #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
       #Add GPS (Global Postion System)
        plugins.LocateControl().add_to(Map)
  #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        try: 
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
        
                EVI = sentinel_2A.expression(
                '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
                        'NIR' : sentinel_2A.select('B8').divide(10000),
                        'RED' : sentinel_2A.select('B4').divide(10000),
                        'BLUE': sentinel_2A.select('B2').divide(10000)})
                EVI_vispar={'min':-1, 'max':1, 'palette': ['yellow', 'brown','green']}#EVI visualization parameters
                Map.addLayer(EVI,EVI_vispar,"EVI(Enhanced Vegetation Index)")#Add Enhanced Vegetation Index to the layers
                
                
                vis_params = {
                        'min': 0,
                        'max': 1,
                        'palette':['yellow', 'brown','green'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='EVI')
                
                legend_dict = {
                        'Non-crops': '1D26B3',
                        'Unhealthly crops': 'F51294',
                        'Moderately healthy crops': '020206',
                        'Very healthy crops': '008000',}                
                Map.add_legend(title="EVI Legend 🌿", legend_dict=legend_dict)
                
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!"
            context['error_message'] = error_message
        else:
                success_message = f"EVI Runned Successfully for Your Region"
                context['success_message'] = success_message
        Map.add_child(folium.LayerControl())

        figure.render()
        context['EVI'] = figure
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
                        
                        
#Soil Type
class soil(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        figure = folium.Figure()
        Map = geemap.Map()
        Map.add_to(figure)
 #mouse position
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(Map)
      #Add GPS (Global Postion System)
        plugins.LocateControl().add_to(Map)
 #Add measure tool 
        plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Map)

        # try:  
                    
        GeologicalMap=ee.FeatureCollection("projects/ee-mosongjnvscode/assets/Kipkelion_West_Soils")
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
                '0000FF', '008000', 'FF0000'
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
            'Loam': '0000FF',
            'Sandy Clay Loam': '008000',
            'Clay Loam': 'FF0000',
        
            }
        Map.add_legend(title="Soil Type🦖", legend_dict=legend_dict)
                
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

#2). DEM(Digital Elevation ):
class DEM(TemplateView):
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

        try:
                Map.center_object(boundary,17);
                srtm=ee.Image("USGS/SRTMGL1_003")
                elev = srtm.select('elevation');
                # Get slope
                slope = ee.Terrain.slope(elev);

                # Clip Srtm DEM by geometry
                DEM_slope= slope.clip(boundary);
                slope_palette1 = ['0C7600','4CE500','B2FF18','FFFF00','FFAE00','ff6d66','FF0000']
                Map.addLayer(DEM_slope,{'palette':slope_palette1},"Digital Elevation Model")
                
                vis_params = {
                    'min': 0,
                    'max': 7000,
                    'palette':['0C7600','4CE500','B2FF18','FFFF00','FFAE00','ff6d66','FF0000'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='Digital Elevation Model(DEM)')
                legend_dict = {
                       'Lowland (Up to 200 M)': '0C7600',
                       'Mountainous Areas: (Up to 500 M)': '4CE500',
                       'High Plateaus:(Around 2,000 M)': 'B2FF18',
                       'Extreme Elevations(Over 5000 M)': 'FF0000',}
                Map.add_legend(title="DEM Legend 🌏", legend_dict=legend_dict)
                
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!"
            context['error_message'] = error_message
        else:
                success_message = f"DEM Runned Successfully for Your Region"
                context['success_message'] = success_message
        Map.add_child(folium.LayerControl())
        figure.render()
       
        context['DEM'] = figure
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
    
#2). Rainfall
class Rainfall(TemplateView):
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

        try:
                Map.centerObject(boundary,12)
                imgcol = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")

                #The shapefile is available here:
                #

                #Time range
                img_col = imgcol.filter(ee.Filter.date ('2000-01-01', '2005-01-30'))


                image = img_col.mean().clip(boundary)
                precipitationVis = {
                'min': 1.0,
                'max': 17.0,
                'palette': ['001137', '0aab1e', 'e7eb05', 'ff4a2d', 'e90000'],
                }
                Map.addLayer(image,precipitationVis,"Rainfall")

                
                vis_params = {
                    'min': 0,
                    'max': 1444.34,
                    'palette':['001137','0aab1e','e7eb05','ff4a2d','e90000'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='Precipitation(mm/d)')
                legend_dict = {
                       'Light Precipitation': '001137',
                       'Moderate Precipitation': '0aab1e',
                       'Heavy Precipitation': 'e7eb05',
                       'Very Heavy Precipitation': 'ff4a2d',
                       'Extreme Precipitation': 'e90000',}
                Map.add_legend(title="Precipitation Legend 🌧", legend_dict=legend_dict)
                
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!"
            context['error_message'] = error_message
        else:
                success_message = f"Rainfall Runned Successfully for Your Region"
                context['success_message'] = success_message
        Map.add_child(folium.LayerControl())
        figure.render()
       
        context['Rainfall'] = figure
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
   
#3). Temperature
class Temperature(TemplateView):
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

        try:
                Map.centerObject(boundary,12)
            # Load a Landsat 8 image
                landsat8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
                    .filterBounds(boundary) \
                    .filterDate('2020-01-01', '2020-12-31') \
                    .sort('CLOUD_COVER') \
                    .first()\
                    .clip(boundary)

                # Function to calculate LST
                def calculateLST(image):
                    # Convert thermal band (Kelvin) to Celsius
                    lstCelsius = image.select(['B10']).subtract(273.15)

                    # Add thermal band to the image
                    return image.addBands(lstCelsius.rename('LST'))

                # Apply the function to the Landsat 8 image
                lstImage = calculateLST(landsat8)

                # Display the result on the map
                Map.centerObject(boundary, 8)
                Map.addLayer(lstImage.select('LST'), {
                    'min': 0,
                    'max': 40,
                    'palette': ['blue', 'purple', 'cyan', 'green', 'yellow', 'red']
                }, 
                             'LST')



                
                vis_params = {
                    'min': 0,
                    'max': 40,
                    'palette':['blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='Temperature(°C)')
                legend_dict = {
                       'Freezing Range: Below 0°C': 'blue',
                       'Cold Range: 0°C': 'purple',
                       'Cool Range: 10°C': 'cyan',
                       'Moderate Range: 20°C': 'green',
                       'Warm Range: 25°C': 'yellow',
                       'Hot Range:Above 30°C': 'red',
                        }
                Map.add_legend(title="Temperature(°C) 🥵", legend_dict=legend_dict)
                
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!"
            context['error_message'] = error_message
        else:
                success_message = f"Temperature Runned Successfully for Your Region"
                context['success_message'] = success_message
        Map.add_child(folium.LayerControl())
        figure.render()
       
        context['Temperature'] = figure
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


#DSS_Model
class DSS_Model(TemplateView):
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

        try:
                Map.centerObject(boundary,12)
            # Load a Landsat 8 image
                landsat8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
                    .filterBounds(boundary) \
                    .filterDate('2020-01-01', '2020-12-31') \
                    .sort('CLOUD_COVER') \
                    .first()\
                    .clip(boundary)

                # Function to calculate LST
                def calculateLST(image):
                    # Convert thermal band (Kelvin) to Celsius
                    lstCelsius = image.select(['B10']).subtract(273.15)

                    # Add thermal band to the image
                    return image.addBands(lstCelsius.rename('LST'))

                # Apply the function to the Landsat 8 image
                lstImage = calculateLST(landsat8)

                # Display the result on the map
                Map.centerObject(boundary, 8)
                Map.addLayer(lstImage.select('LST'), {
                    'min': 0,
                    'max': 40,
                    'palette': ['blue', 'purple', 'cyan', 'green', 'yellow', 'red']
                }, 
                             'LST')



                
                vis_params = {
                    'min': 0,
                    'max': 40,
                    'palette':['blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
                }
                colors = vis_params['palette']
                vmin = vis_params['min']
                vmax = vis_params['max']
                Map.add_colorbar(vis_params,label='Temperature(°C)')
                legend_dict = {
                       'Freezing Range: Below 0°C': 'blue',
                       'Cold Range: 0°C': 'purple',
                       'Cool Range: 10°C': 'cyan',
                       'Moderate Range: 20°C': 'green',
                       'Warm Range: 25°C': 'yellow',
                       'Hot Range:Above 30°C': 'red',
                        }
                Map.add_legend(title="Temperature(°C) 🥵", legend_dict=legend_dict)
                
        except Exception as e:
            # Handle the exception. You can customize this part based on how you want to display the error.
            error_message = f"An error occurred:Please review the previous steps!!!"
            context['error_message'] = error_message
        else:
                success_message = f"DSS Runned Successfully for Your Region"
                context['success_message'] = success_message
        Map.add_child(folium.LayerControl())
        figure.render()
       
        context['DSS_Model'] = figure
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
