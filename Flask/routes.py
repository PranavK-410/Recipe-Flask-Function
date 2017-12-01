import os, random
import pandas as pd
from flask import Flask, render_template, url_for, request, make_response, jsonify


app = Flask(__name__)

#variable to test yes/no button options
#vote = "like"

@app.route('/')

def render():
		
	return render_template("about.html")




@app.route('/pick/')

def pickImage():	

	#path to images
	script_dir = os.path.dirname(__file__)
	rel_path = "static/images27638"
	dirPath = os.path.join(script_dir,rel_path)

	#path to csv file
	script_dir_csv = os.path.dirname(__file__)
	rel_path_csv = "static/RecipeWithImages.csv"
	dirPath_csv = os.path.join(script_dir_csv,rel_path_csv)
	
	
	r_image = random.choice(os.listdir(dirPath))
	imagePath = "../static/images27638/" + r_image

	img_and_recipe = pd.read_csv(dirPath_csv, encoding="cp1252")
	rec = img_and_recipe.loc[img_and_recipe["Image_Title"] == r_image]["Name"].item()
	ingr = img_and_recipe.loc[img_and_recipe["Image_Title"] == r_image]["Ingredients"].item()
	#vote = "yes"


	return render_template("Recipes.html", imgPath=imagePath, recipeName=rec, recipe=ingr)


"""
#Checking for different output depending on button pressed
@app.route('/pick2/')

def pickImage2():	

	#path to images
	script_dir = os.path.dirname(__file__)
	rel_path = "static/images27638"
	dirPath = os.path.join(script_dir,rel_path)

	#path to csv file
	script_dir_csv = os.path.dirname(__file__)
	rel_path_csv = "static/RecipeWithImages2.csv"
	dirPath_csv = os.path.join(script_dir_csv,rel_path_csv)
	
	
	r_image = random.choice(os.listdir(dirPath))
	imagePath = "../static/images27638/" + r_image

	img_and_recipe = pd.read_csv(dirPath_csv, encoding="cp1252")
	rec = img_and_recipe.loc[img_and_recipe["Image_Title"] == r_image]["Name"].item()
	ingr = img_and_recipe.loc[img_and_recipe["Image_Title"] == r_image]["Ingredients"].item()
	#vote = "yes"


	return render_template("Recipes.html", imgPath=imagePath, recipeName=rec, recipe=ingr)
"""
"""
@app.route('/favourites/')

def favouriteRec():

	best = []
"""


if __name__ == '__main__':
	app.run(port=5000, host='0.0.0.0')