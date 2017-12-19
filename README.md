# COMPGC27 Programming for Business Analytics - Group Project - Group 3

This repository contains the source code for the Group Project of "COMPGC27 Programming for Business Analytics" course for UCL MSc in Business Analytics (academic year 2017-2018).

## Group Members
* [Yolande Kaptein] (https://github.com/yolaCaptain)
* Akis Thomas
* Hadrien de Vaucleroy
* [Akis Karamaziotis] (https://github.com/AkisKa)
* [Phedon Dervis] (https://github.com/Pderv049)
* Achilleas Sfakianakis

## Description

In this project, we created an application that reccomends recipes based on user's appetite and mood for food at a particular time. The dataset we were based on is the famous ["Yummly dataset"] (http://lherranz.org/datasets/) containing 28k food-related data points, icluding recipe name, ingredients, cuisine and course type, along with the corresponding images. Project was implemented using Python's micro web framework, Flask and consists of two main parts: An initial clustering that groups recipes based on the aforementioned features and a live backend model, which uses these clusters along with user input to create a preference matrix and display recipes that are close to the users taste. For detailed information, you can check the full report.

## Repository Structure
The *Clustering* folder contains a python script to parse all json files from the metadata folder of the initial dataset and a Jupyter Notebook that presents the whole clustering procedure. The *Flask* folder contains the code for the web application, organized into appropriate directories, following the standard Flask template. Just note that the "RecipeSubsetFlask.csv" file inside Static folder, just contains the recipes and the corresponding clusters, as derived from the Jupyter notebook.


## Run localy
In order to run the application localy, just download the Flask folder, open a terminal and type the following commands:

```python
cd Flask
python routes.py
``` 

Then type at your browser http://localhost:5000/ and press Enter.
