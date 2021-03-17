/* autoResize jQuery plugin written by James Padolsey http://james.padolsey.com 
   autoResize() used to make textarea input expand with text input*/
$(".auto-resize").autoResize();

/* RENDER NEW ROWS IN THE ADD_RECIPE FORM WHEN PLUS BUTTON CLICKED */
$("#add-ingredient-button").on('click', function () {
    ingredientItems = $(".ingredients-container .form-input").siblings('input');
    /* Check that all the boxes in the ingredient container have some text in them before rendering a new text input */
    for (let i = 0; i < ingredientItems.length; i += 1) {
        if (ingredientItems[i].value == "") {
            return;
        } 
    }
    /* Get number to add to name attribute in form */
    inputNumber = ingredientItems.length + 1;
    ingredientHTMLString = `<input class='form-input small-input' id=ingredient_${inputNumber} name='ingredient_${inputNumber}' type='text' value=''>`;
    $(".ingredients-container").append(ingredientHTMLString);
});

/* This function is the same as above, but the jQuery selector needs to target textarea inputs with a name attribute
   due to the autoResize plugin creating hidden textarea inputs when called  */
$("#add-instruction-button").on('click', function () {
    instructionItems = $(".instructions-container .form-input").siblings('textarea[name]'); 
    for (let i = 0; i < instructionItems.length; i += 1) {
        if (instructionItems[i].value == "") {
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

/* Get the name of the file selcted in the file input and render to page */
$("#picture_upload").change(function() {
    $("#selected-file").text($("#picture_upload").val().split("\\").pop())
}) 

// Make 'favourite-recipe' checkbox auto submit when clicked
$(".trigger-form-send").on('click', function(){
    console.log($(this));
    $(this).submit();
});

// $(".trigger-form-send").on('click', function(){
//             $(this).parent().submit();
//     });

/* Get the placeholder values passed to the edit_recipe template textarea inputs
   and render it within the textarea */

// $("document").ready(function(){
//     let instructions = $(".edit-recipe-instruction")
//     Object.values(instructions).forEach(instruction => {
//         instruction.innerText = (instruction.getAttribute("placeholder"));
//     });
// });

/* If the recipe card title contains 28 characters or more, apply the shrink-header CSS class */
$(".recipe-card-title").each(function(){
    if ($(this).text().length >= 28){
        $(this).addClass('shrink-header');
    }
})

/* Enable bootsrap popovers and 'dismiss on next click' */
$(function () {
    $('[data-toggle="popover"]').popover({html: true});
    $('[data-toggle="tooltip"]').tooltip();
})

$('.popover-dismiss').popover({
  trigger: 'focus'
})