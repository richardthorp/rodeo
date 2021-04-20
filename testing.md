# Testing
## Testing against User Stories
#### **To be able to navigate through the website in an intuitive and easy fashion.**

The website conforms to standard website UX principles. All pages have a navigation bar which provides clear links to the main pages of the website. Any links or buttons feature cursor hover effects to make clear that they are interactive elements. Where appropriate, a 'back to...' button is provided to ensure the user can quickly and easily return to search results or lists of recipes. 

#### **To discover popular recipes involving hot sauce**

When visiting the website, the first page presented to the user displays a small amount of content before offering 2 or 3 (depending on screen size) of the website highest rated recipes. Below this is a link to browse all of the recipes available on the website which are by default presented with the highest rated recipes first.

#### **To discover new recipes involving hot sauce**
Whilst browsing any of the pages that list the recipes, the option to sort the recipes by newest first is available via a clear 'sort by: newest' link.

#### **To be able to quickly and easily search the recipes to find specific ingredients or meal types**
Whilst browsing any of the pages that list the recipes, a search text input and options to filter the recipes are available above the listed recipes. The search feature will search the relevent recipes for that page (ie. on **'added_recipes.html'**, only recipes that the user has added) for any matching words in the recipe name and ingredient fields.
As well as this, the user has the option to filter the recipes by type ('vegetarian', 'vegan' or 'meat') and the further filter by options such as 'quick', 'healthy' and 'gluton free'.

#### **To contribute my own recipes to the website community**
Once a user is registered and logged in, they are directed to **'my_recipes.html'**. Whist this page is mainly dedicated to displaying recipes that the user has added to their favourites, the link to **'add_recipe.html'** is clearly displayed towards the top of the page. Once on **'add_recipe.html'**, a simple form is available for the user to fill out and submit their recipe to the database. This recipe is then immediately available to view on the website.

#### **To be able to quickly edit or delete recipes that I have contributed**
Once a user has added their recipe to the database via **'add_recipe.html'**, they are directed to the **'recipe_page.html'** page for that recipe. At the top of this page are links to 'edit' and 'delete' the recipe. By clicking on the 'edit' button, the user is returned to the same form that they filled out in **'add_recipe.html'**, with all the existing recipe information in the form ready to be edited. By clicking on the 'delete' button, a modal is triggered which asks the user "Are you sure you want to delete this recipe? This cannot be undone!". At this point the user can either immediately delete the recipe from the database, or return to the recipe page.
The 'edit' and 'delete' buttons are also available to the user at the bottom of each recipe card in the **'added_recipes.html'** page.

#### **To be able to save recipes that interest me and be able to access them quickly**
If the user is logged in, any page that displays a recipe or recipe cards features the 'FAVOURITE RECIPE?' heart icon. Once clicked, the recipe can be accessed quickly through the 'MY RECIPES' link in the navigation bar or footer. If the recipe is already in the users 'MY RECIPES' page, clicking the heart icon will remove the recipe from the list. 

#### **To be able to rate recipes and have those ratings influence the information hierarchy throughout the website**
If the user is logged in, whilst on a **'recipe_page.html'** page, the option to rate the recipe out of 5 stars is available. Once a user rating is sent, the average rating for that recipe is updated to reflect the new score. This in turn will move the recipe up or down the lists presented in **'all_recipes.html'**, **'my_recipes.html'** and **'added_recipes.html'**.

#### **To be able to log in and log out of the website easily**
If the user in not logged in, a link to **'login.html'** is available in the navigation bar, and if the user is logged in a link to the **'logout'** function is presented.

#### **For the data presented to me to be specific to me.**
By adding favourite recipes to the **'my_recipes.html'** list, as well as adding their own recipes, users can curate their own selection of recipes that can be accessed by logging in to the website.