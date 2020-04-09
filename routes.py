import random
import pandas as pd
from flask import Flask, render_template


app = Flask(__name__)


# Initialising preference matrix
d = {'Variable': ['Dummy'], 'Count': [0]}
preferencesdf = pd.DataFrame(data=d)
d2 = {'ClusterNumber': ['Cluster0','Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7'], 'Count': [1,1,1,1,1,1,1,1]}
clusterpreference = pd.DataFrame(data=d2)

# Reading the Excel file containing the recipe clusters
recipearray = pd.read_excel("static/RecipeSubsetFlask.xlsx")

# Pick a random image for our initial image page
previousRecipe = recipearray.iloc[random.randint(1,100)] 

# Initialising empty lists to store the variables of images that have been liked
favouriteImage = []
favouriteRecipeName = []
favouriteRecipe = []
listIndex = 0

##################### Updating user preferences #####################

def selectRandomRecipe(recipesrange):
    output=recipesrange.iloc[random.randint(0, recipesrange.shape[0]-1)]
    return output


def splitFeaturesInRecipe(recipe):
    my_string=recipe[7]
    #print('String:',my_string)
    items=[x.strip() for x in my_string.split(',')]
    items[0]=items[0][2:-1]
    for i in range(1,len(items)-1,1):
        items[i]=items[i][1:-1]
    items[len(items)-1]=items[len(items)-1][1:-2]
    return items

def updatepreferences(recipe,vote,preferences,clusterpreferences):
    if vote=='Y' or vote=='y' or vote=='yes' or vote=='Yes' or vote=='YES':
        #print('HEEERE:',recipe)
        cluster=recipe[8]
        clusterpreferences.iat[cluster,1]=clusterpreferences.iat[cluster,1]+5
        randomRecFeatures=splitFeaturesInRecipe(recipe)
        for i in range(0,len(randomRecFeatures),1):
            isInPreferences=False
            j=0
            while j<len(preferences):# or isInPreferences==False:   len(preferences)
                if randomRecFeatures[i]==preferences.iat[j,1]:
                    isInPreferences=True
                    preferences.iat[j,0]=preferences.iat[j,0]+1
                    j=j+1 
                else:
                    j=j+1    
            if isInPreferences==False:
                preferences.loc[len(preferences.index)+1]=[1,randomRecFeatures[i]]
    #else:
        #print('Nothing happened.')
    return preferences,clusterpreferences



def chooseClusterByProbability(clusterpreferences):
    #code needed
    r=random.randint(1,11) #to decide of it should be completely random or not
    if r<12:
        weights=[]
        for j in range(0,clusterpreferences.shape[0],1): #should this be -1??
            weights.append(clusterpreferences.iat[j,1])
    
        totals = []
        running_total = 0
    
        for w in weights:
            running_total += w
            totals.append(running_total)
    
        rnd = random.random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                output = i
                break
    else:
        output=random.randint(0, 7)
      
    #print('Cluster chosen is:',output+1)
    return output

def pullRecipesFromCluster(clusternumber,recipelist):
    RecipeList=recipelist.loc[recipelist['Cluster'] == clusternumber]
    return RecipeList

def chooseSimilar(recipesfromcluster,preferences):
    bestscore=0
    count=0
    rand=random.randint(0, recipesfromcluster.shape[0]-1)
    outputrecipe=recipesfromcluster.iloc[rand]
    while count<20:
        score=0
        rand=random.randint(0, recipesfromcluster.shape[0]-1)
        currentrecipe=recipesfromcluster.iloc[rand]
        currentrecipeSplit=splitFeaturesInRecipe(currentrecipe)
        for i in range(0,len(currentrecipeSplit),1):
                j=0
                while j<len(preferences):# or isInPreferences==False:   len(preferences)
                    if currentrecipeSplit[i]==preferences.iat[j,1]:
                        score=score+preferences.iat[j,0]
                        j=j+1 
                    else:
                        j=j+1    
        if bestscore<score:
            bestscore=score
            outputrecipe=currentrecipe
        count=count+1
    return outputrecipe

##################### Main flask body #####################

@app.route('/')

def render():
    
    """
    Function to render the homepage of our WebApp 
    """
		
    global previousRecipe
    
    return render_template("about.html")

    #print('Previous 1:',previousRecipe)

@app.route("/initial/")

def initialDisplay():
    
    """
    Function to display the first image. Since there are no preferences yet
    it is picked randomly.
    """
    
    global previousRecipe
    global recipearray
    global imagePath
    global rec
    global ingr
    
    
    firstImage = previousRecipe[1]
    imagePath = "../static/images/" + firstImage
    rec = previousRecipe[0]
    ingr = previousRecipe[4]

    return render_template("Recipes.html", imgPath=imagePath, recipeName=rec, recipe=ingr)

	

@app.route('/Like/')

def pickImage():

    """ 
    When a user clicks the Like button this function updates 
    the preferences matrix accordingly.
    At the same time we append the necessary Recipe variables to
    the corresponding favourites lists.
    """
    
    global previousRecipe
    global preferencesdf
    global clusterpreference
    global recipearray   
    
    global imagePath
    global rec
    global ingr

    global favouriteImage
    global favouriteRecipeName
    global favouriteRecipe
    
    #print('Preferences:',clusterpreference)
    
    # Update preferences
    preferencesdf,clusterpreference=updatepreferences(previousRecipe, "Y",preferencesdf,clusterpreference)
    clusternumber=chooseClusterByProbability(clusterpreference)
    recipesFromCluster=pullRecipesFromCluster(clusternumber,recipearray)
    similarRecipe=chooseSimilar(recipesFromCluster,preferencesdf)
    
    # Append favourite variables
    favouriteImage.append(imagePath)
    favouriteRecipeName.append(rec)
    favouriteRecipe.append(ingr)

    r_image = similarRecipe[1]
    imagePath = "../static/images/" + r_image
    rec = similarRecipe[0]
    ingr = similarRecipe[4]
    
    previousRecipe=similarRecipe
    
    return render_template("Recipes.html",
                           imgPath=imagePath,
                           recipeName=rec,
                           recipe=ingr)




#Checking for different output depending on button pressed
@app.route('/Skip/')

def pickImage2():	
    
    """ 
    When a user clicks the Skip button the
    preference matrix remains the same and 
    a different image is pulled accordingly.
    """

    global previousRecipe
    global preferencesdf
    global clusterpreference
    global recipearray   
    
    global imagePath
    global rec
    global ingr

    global favouriteImage
    global favouriteRecipeName
    global favouriteRecipe
    
    # Update preferences
    preferencesdf,clusterpreference=updatepreferences(previousRecipe, "N",preferencesdf,clusterpreference)
    clusternumber=chooseClusterByProbability(clusterpreference)
    recipesFromCluster=pullRecipesFromCluster(clusternumber,recipearray)
    similarRecipe=chooseSimilar(recipesFromCluster,preferencesdf)

    r_image = similarRecipe[1]
    imagePath = "../static/images/" + r_image
    rec = similarRecipe[0]
    ingr = similarRecipe[4]
    previousRecipe=similarRecipe

    return render_template("Recipes.html",
                           imgPath=imagePath,
                           recipeName=rec,
                           recipe=ingr)


@app.route('/favourites/')

def favouriteRec():
    
    """
    Every time a user Likes an image, the corresponding
    elements are appended to the favourites lists. By clicking
    on the Favourites button, the user is directed to the Favourites
    page where they can skim through their previously liked recipes.
    """
    

    global favouriteImage
    global favouriteRecipeName
    global favouriteRecipe
    global listIndex
    
    # As long as the user has not liked any recipes, if they click on favourites
    # an error page is displayed.
    if (len(favouriteImage)==0):
        
        return render_template("error.html")
    
    else:
            
        fimgPath = favouriteImage[listIndex]
        frecipeName = favouriteRecipeName[listIndex]
        frecipe = favouriteRecipe[listIndex]
    
        listIndex += 1
    
        if (listIndex >= len(favouriteImage)):
            listIndex = 0
            
        return render_template("Favourites.html", imgPath = fimgPath, recipeName=frecipeName, recipe=frecipe)
    
    


if __name__ == '__main__':
	app.run(port=5000, host='0.0.0.0')
