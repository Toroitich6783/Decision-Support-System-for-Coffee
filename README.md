<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  
  <h3 align="center">Decision-Support-System-for-Coffee</h3>

</div>

<!-- ABOUT THE PROJECT -->
## About The Project

This a python project aimed on addressing maximizing satelite data. This is by the use of Google Earth engine python API known as Earth Engine(EE) with an GEEMAP: A Python package for interactive geospatial analysis and visualization with Google Earth Engine.


<!-- GETTING STARTED -->
## Getting Started

This is a step by step guide/instructions on setting up this project locally.
To get a local copy up and running follow these simple example steps.


### Prerequisites

To set up this project successfully, Make sure you have python install and miniconda or anaconda installed.
* Python:
https://www.python.org/
  
* Downloading conda: Anaconda/Miniconda:
  https://docs.conda.io/projects/conda/en/stable/user-guide/install/download.html
  

### Installation

_Below is a procedural guidelines to install and setting up the this project._

1. Thus,To use geemap, you must first sign up for a Google Earth Engine account.

2. Clone the repo
   ```sh
   git clone https://github.com/Toroitich6783/Decision-Support-System-for-Coffee.git
   ```
3. create a python virtual env:
   ```sh
   conda create -n gee python=3.10
   ```
   gee is the name of virtual env you can use any other name
   Make sure you have python install and miniconda or anaconda installed.
4. After creating the virtual env activate the virtual env:
   ```sh
   conda activate gee
   ```
5. Then for an easy and faster way to install  geemap is by the use of Mamba library.
   so, yo have to install Mamba library.
   ```sh
   conda install -n base mamba -c conda-forge
   ```
6. Then finally, will install the the geospatial libraries that are commonly used using a single  command line known as "geospatial"
   ```sh
    mamba install -c conda-forge geospatial
   ```
   The geospatial package only helps you install commonly used packages for geospatial analysis and data visualization with only one command, making it easier to set up a conda environment for geospatial analysis and avoid dependency conflicts during installation. The geospatial package itself does not have any meaningful functions yet. After installation, you can continue to the commonly used geospatial packages as usual.
7. Extra will install a psycopg2 lib; This is for data retrival from Postgresql DataBase.
   ```sh
    pip install psycopg2
   ```
8. Finally, Install Django package to access the Django-python framework capabilities and features.
   ```sh
    pip install Django
   ```
9. Navigate to the clone project then to run. From the terminal section ensure to have the right path then start a django server by using the folllowing command.
   ```sh
   python manage.py runserver 'port number'
   ```
   use your desired port number but the default is 8000.

10. Finally, follow the development server at  127.0.0.1:8000/, to a default browser.

    <p align="right"><a href="#readme-top">back to top</a></p>





