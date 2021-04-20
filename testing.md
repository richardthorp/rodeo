# Testing
## Testing against User Stories
#### **To be able to navigate through the website in an intuitive and easy fashion.**

The website conforms to standard website UX principles. All pages have a navigation bar which provides clear links to the main pages of the website. Any links or buttons feature cursor hover effects to make clear that they are interactive elements. Where appropriate, a 'back to...' button is provided to ensure the user can quickly and easily return to search results or lists of recipes. 

![The 'back to...' link and navigation bar links](static/images/readme-images/testing-images/navigation.jpg "The 'back to...' link and navigation bar links")

#### **To discover popular recipes involving hot sauce**

When visiting the website, the first page presented to the user displays a small amount of content before offering 2 or 3 (depending on screen size) of the website highest rated recipes. Below this is a link to browse all of the recipes available on the website which are by default presented with the highest rated recipes first.

![The 3 highest rated recipes form the website displayed on index.html](static/images/readme-images/testing-images/index-recipes.jpg "The 3 highest rated recipes form the website displayed on index.html")

#### **To discover new recipes involving hot sauce**
Whilst browsing any of the pages that list the recipes, the option to sort the recipes by newest first is available via a clear 'sort by: newest' link above the recipe cards.

![The 'sort by' links above the recipe cards](static/images/readme-images/testing-images/sort-by.jpg "The 'sort by' links above the recipe cards")


#### **To be able to quickly and easily search the recipes to find specific ingredients or meal types**
Whilst browsing any of the pages that list the recipes, a search text input and options to filter the recipes are available above the listed recipes. The search feature will search the relevent recipes for that page (ie. on **'added_recipes.html'**, only recipes that the user has added) for any matching words in the recipe name and ingredient fields.
As well as this, the user has the option to filter the recipes by type ('vegetarian', 'vegan' or 'meat') and the further filter by options such as 'quick', 'healthy' and 'gluton free'.

#### **To contribute my own recipes to the website community**
Once a user is registered and logged in, they are directed to **'my_recipes.html'**. Whist this page is mainly dedicated to displaying recipes that the user has added to their favourites, the link to **'add_recipe.html'** is clearly displayed towards the top of the page. Once on **'add_recipe.html'**, a simple form is available for the user to fill out and submit their recipe to the database. This recipe is then immediately available to view on the website.

![The 'ADD A NEW RECIPE' button in 'MY RECIPES'](static/images/readme-images/testing-images/add-recipe-button.jpg "The 'ADD A NEW RECIPE' button in 'MY RECIPES'")

#### **To be able to quickly edit or delete recipes that I have contributed**
Once a user has added their recipe to the database via **'add_recipe.html'**, they are directed to the **'recipe_page.html'** page for that recipe. At the top of this page are links to 'edit' and 'delete' the recipe. By clicking on the 'edit' button, the user is returned to the same form that they filled out in **'add_recipe.html'**, with all the existing recipe information in the form ready to be edited. By clicking on the 'delete' button, a modal is triggered which asks the user "Are you sure you want to delete this recipe? This cannot be undone!". At this point the user can either immediately delete the recipe from the database, or return to the recipe page.
The 'edit' and 'delete' buttons are also available to the user at the bottom of each recipe card in the **'added_recipes.html'** page.

![The 'EDIT' and 'DELETE' buttons in a recipe page](static/images/readme-images/testing-images/edit-delete-buttons.jpg "The 'EDIT' and 'DELETE' buttons in a recipe page")

![The 'EDIT' and 'DELETE' buttons in added_recipes.html](static/images/readme-images/testing-images/recipe-card-edit-delete.jpg "The 'EDIT' and 'DELETE' buttons in added_recipes.html")

#### **To be able to save recipes that interest me and be able to access them quickly**
If the user is logged in, any page that displays a recipe or recipe cards features the 'FAVOURITE RECIPE?' heart icon. Once clicked, the recipe can be accessed quickly through the 'MY RECIPES' link in the navigation bar or footer. If the recipe is already in the users 'MY RECIPES' page, clicking the heart icon will remove the recipe from the list. 

![The heart icon as seen in a recipe page](static/images/readme-images/testing-images/heart-icon.jpg "The heart icon as seen in a recipe page")


#### **To be able to rate recipes and have those ratings influence the information hierarchy throughout the website**
If the user is logged in, whilst on a **'recipe_page.html'** page, the option to rate the recipe out of 5 stars is available. Once a user rating is sent, the average rating for that recipe is updated to reflect the new score. This in turn will move the recipe up or down the lists presented in **'all_recipes.html'**, **'my_recipes.html'** and **'added_recipes.html'**.

![The user rating stars and 'add rating' button](static/images/readme-images/testing-images/user-rating-stars.jpg "The user rating stars and 'add rating' button")

#### **To be able to log in and log out of the website easily**
If the user in not logged in, a link to **'login.html'** is available in the navigation bar, and if the user is logged in a link to the **'logout'** function is presented.

![The log out button in the navigation bar](static/images/readme-images/testing-images/log-out-button.jpg "The log out button in the navigation bar")


#### **For the data presented to me to be specific to me.**
By adding favourite recipes to the **'my_recipes.html'** list, as well as adding their own recipes, users can curate their own selection of recipes that can be accessed by logging in to the website.

## **Testing against Brand Objectives**
#### **Increase brand awareness**
By having a website to direct consumers and potential consumers to, the brand has a platform on which to promote itself. With the website focussing heavily on users adding their own recipes and viewing other peoples recipes, the potential for users themselves to promote the brand by sharing recipes with friends and family and across social media is provided.

#### **Increase sales**
At present, there is no requirement to have 'Rodeo Hot Sauce' as an ingredient in the recipes. Whilst this was considered, it was decided that it would not be conducive to encouraging people to use the site by restricting the content in that way. However, by establishing the website as a hub for good quality hot sauce recipes, this would add to the perception of 'Rodeo' being a quality product and brand, and therefore in turn increase sales.  

#### **Generate a sense of community amongst consumers**
By providing a platform for fans of hot sauce to come together and share in their love of hot sauce recipes, the website enables and encourages people to contribute to the community. As mentioned in the 'Potential Future Features' section of the README document, to further this goal it would be beneficial to add an 'add comment' feature to the recipe pages to allow users to interact with each other.

#### **Collect customer data**
By requiring users to register with their email address, the brand can use these addresses to send marketing direct to their target audience.

#### **Improve understanding of consumers**
As mentioned in 'Potential Future Features', a great way to accomplish this objective would be to provide a dashboard for the website owners which displays which types of recipes are being added and which recipes are most popular. Unfortunately, time constraints mean this feature is unfeasable at this time.

#### **A note on Testing against Brand Objectives**
I feel that whilst these objectives have been met to some extent, as the focus of this project is firmly on the access to and manipulation of a shared data set for users, these objectives have not been a priority in the design or implementation of the website.

## Validation
### HTML
The HTML code has been validated against the [W3C Markup Validator](https://validator.w3.org/). This was done by copying the HTML code from Chrome Dev Tool once rendered in the browser, for all pages whilst both logged in and logged out of the website, and pasting the code into the validator. This was neccessary in order to test the code in it's final state after being proccessed by the Jinja templates. The HTML code contains no validity issues.

### CSS and Javascript
The CSS code has been validated against the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) and the JavaScript with the [JS Hint](https://jshint.com/) code analysis tool, with any issues highlighted by the validators fixed. The code contains no validity issues.

### Python
All Python code was written to be PEP 8 compliant. The only error message thrown by the Gitpod linter is 'Instance of 'Registration_form' has no 'errors' member'. I am unsure as to why this error is thrown as the function which uses the Registration_form.errors object has been tested and works as expected. The function has access to the data in the error object and uses the flash function to display a custom error message depending on the content of that object.

![The route function which contains a pylint error](static/images/readme-images/testing-images/form-error.jpg "The route function which contains a pylint error")

## Responsive testing
The website has been developed and tested to ensure a high level of responsiveness. This has been achieved using Google Chrome Dev Tools, testing on different physical devices and by viewing the site on [Am I Responsive?](http://ami.responsivedesign.is/).