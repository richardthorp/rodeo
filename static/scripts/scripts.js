rowCount = 3;

$("#add-ingredient-row").on('click', function(){
    if ($(".ingredients-container .form-input").last()[0].value != "" && $(".quantity-container .form-input").last()[0].value != "") {
        ingredientHTMLString = `<input class='form-input' id=ingredient_${rowCount} name='ingredient_${rowCount}' type='text' value=''>`;
        quantityHTMLSting = `<input class='form-input' id=quantity_${rowCount} name='quantity_${rowCount}' type='text' value=''>`;
        $(".ingredients-container").append(ingredientHTMLString);
        $(".quantity-container").append(quantityHTMLSting);
        rowCount += 1;
    }
});

$(".auto-resize").autoResize();