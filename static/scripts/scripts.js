// Check that all the boxes have some text in them before rendering a new text input
$("#add-ingredient-row").on('click', function () {
    ingredientItems = $(".ingredients-container .form-input").siblings('input');
    for (let i = 0; i < ingredientItems.length; i += 1) {
        if (ingredientItems[i].value == "") {
            return;
        } 
    }
    // Get number to add to name attribute in form
    inputNumber = ingredientItems.length + 1;
    ingredientHTMLString = `<input class='form-input' id=ingredient_${inputNumber} name='ingredient_${inputNumber}' type='text' value=''>`;
    quantityHTMLSting = `<input class='form-input' id=quantity_${inputNumber} name='quantity_${inputNumber}' type='text' value=''>`;
    $(".ingredients-container").append(ingredientHTMLString);
    $(".quantity-container").append(quantityHTMLSting);
});


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
                        required="" style="resize: none; overflow-y: hidden;"></textarea>`
    $(".instructions-container").append(instructionHTMLString);
    $(".auto-resize").autoResize();
});

// autoResize jQuery plugin written by James Padolsey http://james.padolsey.com
$(".auto-resize").autoResize();



