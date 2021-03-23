/* autoResize jQuery plugin written by James Padolsey http://james.padolsey.com 
   autoResize() used to make textarea input expand with text input*/
$(".auto-resize").autoResize();

/* ADD RECIPE AND EDIT RECIPE FORM SCRIPTS */

/* RENDER NEW ROWS IN ADD_RECIPE AND EDIT RECIPE FORMS WHEN PLUS BUTTON CLICKED */
$("#add-ingredient-button").on('click', function () {
    ingredientItems = $(".ingredients-container .form-input");
    /* Check that all the boxes in the ingredient container have some text in them before rendering a new text input */
    for (let i = 0; i < ingredientItems.length; i += 1) {
        if (ingredientItems[i].value == "") {
            $(ingredientItems[i]).tooltip({title: "Please use this input first!"}).tooltip('show');
            setTimeout(()=>{
                 $(ingredientItems[i]).tooltip('dispose');
            }, 2500)
            return;
        } 
    }
    /* Get number to add to name attribute in form */
    inputNumber = ingredientItems.length + 1;
    ingredientHTMLString = `<input class='form-input small-input' id=ingredient_${inputNumber} name='ingredient_${inputNumber}' type='text' value=''>`;
    $(".ingredients-container").append(ingredientHTMLString);
});

/* This function is the same as above, but the jQuery selector needs to target textarea inputs with an id attribute
   due to the autoResize plugin creating hidden textarea inputs when called  */
$("#add-instruction-button").on('click', function () {
    instructionItems = $(".instructions-container .form-input").siblings('textarea[id]'); 
    for (let i = 0; i < instructionItems.length; i += 1) {
        if (instructionItems[i].value == "") {
            $(instructionItems[i]).tooltip({title: "Please use this input first!"}).tooltip('show');
            setTimeout(()=>{
                 $(instructionItems[i]).tooltip('dispose');
            }, 2500)
            return;
        } 
    }
    inputNumber = instructionItems.length + 1
    instructionHTMLString = `<textarea class="form-input auto-resize" id="instruction_${inputNumber}" 
                        name="instruction_${inputNumber}" placeholder="Please enter step ${inputNumber}..."
                        style="resize: none; overflow-y: hidden;"></textarea>`
    $(".instructions-container").append(instructionHTMLString);
    $(".auto-resize").autoResize();
});
   
$("document").ready(function(){
        /* Edit recipe form - get value passed to the placeholder attibute in template and 
        use as inner text value. Overwrite name attribute provided by WTForms and set equal 
        to id attribute which is made unique with loop index in edit_recipe template */
    $(".edit-recipe-instructions .form-input").siblings('textarea[id]').each((index, instruction) => {
        instruction.innerText = instruction.getAttribute("placeholder");
        instruction.setAttribute('name', instruction.getAttribute("id")); 
    });
    /* Same as above function, but value attribute is set in template and not here*/
    $(".edit-recipe-ingredient").each((index, ingredient) => {
    ingredient.setAttribute('name', ingredient.getAttribute("id"));
        
    });
    /* Remove required attribute from hidden input fields */
    $(".edit-recipe-instructions .form-input").siblings('textarea[tabindex]').each((index, hiddenInput) => {
        hiddenInput.removeAttribute('required');
    })
});

/* If the recipe card title contains 28 characters or more, apply the shrink-header CSS class */
$(".recipe-card-title").each(function(){
    if ($(this).text().length >= 28){
        $(this).addClass('shrink-header');
    }
})

/* Get the name of the file selcted in the file input and render to page */
$("#picture_upload").change(function() {
    $("#selected-file").text($("#picture_upload").val().split("\\").pop())
}) 

// Make 'favourite-recipe' checkbox auto submit when clicked
$(".trigger-form-send").on('click', function(){
    console.log($(this));
    $(this).submit();
});

/* Enable bootsrap popovers and 'dismiss on next click' */
$(function () {
    $('[data-toggle="popover"]').popover({html: true});
    $('[data-toggle="tooltip"]').tooltip();
})

$('.popover-dismiss').popover({
  trigger: 'focus'
})

$("document").ready(function(){
    $(".flashed-messages").hide().slideDown('slow', function(){
        setTimeout(function() {
                $(".flashed-messages").slideUp();
            }, 4000)
    });
});