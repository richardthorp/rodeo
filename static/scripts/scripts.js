/* autoResize jQuery plugin written by James Padolsey http://james.padolsey.com 
   autoResize() used to make textarea input expand with text input*/
$(".auto-resize").autoResize();

/* RENDER NEW ROWS IN THE ADD_RECIPE FORM WHEN PLUS BUTTON CLICKED */
$("#add-ingredient-row").on('click', function () {
    ingredientItems = $(".ingredients-container .form-input").siblings('input');
    /* Check that all the boxes in the ingredient container have some text in them before rendering a new text input */
    for (let i = 0; i < ingredientItems.length; i += 1) {
        if (ingredientItems[i].value == "") {
            return;
        } 
    }
    /* Get number to add to name attribute in form */
    inputNumber = ingredientItems.length + 1;
    ingredientHTMLString = `<input class='form-input' id=ingredient_${inputNumber} name='ingredient_${inputNumber}' type='text' value=''>`;
    quantityHTMLString = `<input class='form-input' id=quantity_${inputNumber} name='quantity_${inputNumber}' type='text' value=''>`;
    $(".ingredients-container").append(ingredientHTMLString);
    $(".quantity-container").append(quantityHTMLString);
});

/* This function is the same as above, but the jQuery selector needs to target textarea inputs with a name attribute
   due to the autoResize plugin creating hidden textarea inputs when called  */
$("#add-instructions-row").on('click', function () {
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

/* If the favourite checkbox is clicked, submit the form */
// $(document).ready(function(){
//     $("#favourite-checkbox-checked").on('click', function(){
//         setTimeout(function(){
//             console.log('value = n')
//             $("#favourite-form").submit();
//         }, 1000);
//     });
    
//     $("#favourite-checkbox-unchecked").on('click', function(){
//         setTimeout(function(){
//             console.log('value = y')
//             $("#favourite-form").submit();
//         }, 1000)
    
//     });
// });

$("#favourite-checkbox-checked").on('click', function(){
            $("#favourite-form").submit();
    });

$("#favourite-checkbox-unchecked").on('click', function(){
            $("#favourite-form").submit();
    });