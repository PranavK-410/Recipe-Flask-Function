# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 23:22:46 2017

@author: asfak
"""

import pandas as pd
import numpy as np
import json
import os


def ParseData(filepath):
    
    '''
    Parse recipes to a DataFrame. Each recipy is stored in a JSON file, all of which must be
    located under a /data/metadata27638 filepath.
    
    The function takes as an input the corresponding filepath, iterates through all JSON
    files present inside the folder, and creates a DataFrame. 
    '''
    
    # Root directory
    cwd = os.path.dirname(os.path.abspath("__file__"))
    os.chdir(cwd + "/data/metadata27638")

    # List all json files in filepath
    files = os.listdir()
    
    # Initialize lists to store JSON key values
    recipies = []
    name = []
    course = []
    cuisine = []
    ingredients = []
    flavors = []
    kcal = []
    nutrients = []
    kcal_all = []
    prepTime = []
    time = []
    
    # Define DataFrame to store values        
    columns = ["Name", "Image_Title", "Course", "Cuisine", "Ingredients", "Flavors", "kcal", \
               "Nutrients", "kcal_dict", "PreparationTime", "TotalTime"]
    df = pd.DataFrame(index = range(len(files)), columns = columns)
    
    
    # Iterate through files
    for i in range(len(files)):
        
        if (i+1) % 1000 == 0:
            print("{} files processed so far".format(i+1))
        
        # Open file
        with open(files[i], encoding = "utf8") as data_file:
            data = json.load(data_file)
            recipies.append(data)
            
        # Add name
        name.append(data["name"])
        
        # Add Course    
        course.append(data["attributes"]["course"][0])
        
        # Add cuisine
        cuisine.append(data["attributes"]["cuisine"][0])
        
        # Add ingeredients
        ingredients.append("".join(data["ingredientLines"]))
        
        # Add flavor dict    
        try:
            flavors.append(data["flavors"])
        except KeyError:
            flavors.append({})
            
        # Add kcal
        try:
            nutrition = data["nutritionEstimates"]
            kcal.append(np.sum([i["value"] for i in nutrition]))
        except:
            kcal.append(np.NaN)
            
        # Add nutrients
        try:
            nutrition = data["nutritionEstimates"]
            elem = [i["description"] for i in nutrition]
            elem_remove_NoneType = list(filter(None.__ne__, elem))
            nutrients.append("--".join(elem_remove_NoneType))
        except:
            nutrients.append("")
            
        # Add kcal_dict    
        try:
            kcal_dict = {}
            
            for i in range(len(data["nutritionEstimates"])):
                kcal_dict[data["nutritionEstimates"][i]["description"]] =  data["nutritionEstimates"][i]["value"]
                
            kcal_all.append(kcal_dict)
        except KeyError:
            kcal_all.append({})
            
        
        # Add preparation time
        try:
            prepTime.append(data["prepTime"])
        except KeyError:
            prepTime.append(0)
            
        # Add time in secs
        time.append(data["totalTimeInSeconds"])
        
        
    # Change working directory
    os.chdir(filepath + "/data/images27638")
    
    # Picture titles
    pic_files = os.listdir()
        
        
    
    # Fill in DataFrame values
    df["Name"] = name
    df["Image_Title"] = pic_files
    df["Course"] = course
    df["Cuisine"] = cuisine
    df["Ingredients"] = ingredients
    df["Flavors"] = flavors
    df["kcal"] = kcal
    df["Nutrients"] = nutrients
    df["kcal_dict"] = kcal_all
    df["PreparationTime"] = prepTime
    df["TotalTime"] = time
    
    
    # Change directory to root
    os.chdir("../..")
    
    # Change directoryto clustering folder
    os.chdir(os.path.join(filepath,"Clustering"))
    return df


    # Export DataFrame to excel
#    writer = pd.ExcelWriter("C:/Users/asfak/Desktop/New folder/FoodRecipies.xlsx")
#    df.to_excel(writer, "Sheet 1", index = False)
#    writer.save()
