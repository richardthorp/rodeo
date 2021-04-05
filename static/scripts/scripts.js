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
            $(ingredientItems[i]).tooltip({ title: "Please use this input first!" }).tooltip('show');
            setTimeout(() => {
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
            $(instructionItems[i]).tooltip({ title: "Please use this input first!" }).tooltip('show');
            setTimeout(() => {
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

$("document").ready(function () {
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
$(".recipe-card-title").each(function () {
    if ($(this).text().length >= 28) {
        $(this).addClass('shrink-header');
    }
})

/* Get the name of the file selcted in the file input on add and edit recipe page and render to page */
$("#picture_upload").change(function () {
    $("#selected-file").text($("#picture_upload").val().split("\\").pop())
})
$("#new_picture_upload").change(function () {
    $("#selected-file").text($("#new_picture_upload").val().split("\\").pop())
})


// Make 'favourite-recipe' checkbox auto submit when clicked
$(".trigger-form-send").on('click', function () {
    console.log($(this));
    $(this).submit();
});

/* Enable bootsrap popovers and 'dismiss on next click' */
$(function () {
    $('[data-toggle="popover"]').popover({ html: true });
    $('[data-toggle="tooltip"]').tooltip();
})

$('.popover-dismiss').popover({
    trigger: 'focus'
})

/* Add slide down and slide up animation to flashed messages */
$(".flashed-messages").hide().slideDown('slow', function () {
    setTimeout(function () {
        $(".flashed-messages").slideUp();
    }, 4000)
});

/* Render average rating stars to page */
$("document").ready(function () {
    $(".ratings-container").each((index, node) => {
        /* Get rating passed to each ratings-container in templates */
        let rating = parseFloat(node.innerText)
        /* Find the difference between given rating and potential rating. Round the number down, 
        as half stars are handled in the rating while loop */
        let remainder = Math.floor(5 - rating);
        let ratingHtml = "";
        /* Generate the HTML to render solid stars and half stars */
        while (rating > 0) {
            ratingHtml += "<span class='star coloured-star'><i class='fas fa-star'></i></span>"
            rating--;
            if (rating == 0.5) {
                ratingHtml += "<span class='star coloured-star'><i class='fas fa-star-half-alt'></i></span>";
                rating = 0;
            }
        }
        /* Generate the HTML to render empty stars */
        while (remainder > 0) {
            ratingHtml += "<span class='star blank-star'><i class='far fa-star'></i></span>"
            remainder--;
        }
        node.innerHTML = ratingHtml;
    })
})

/* Render user rating stars (radio form inputs) */
$("document").ready(function () {
    let userRating = parseInt($(".user-rating").text());
    let userRatingHtml = "";
    for (let i = 1; i < 6; i++) {
        /* Add checked attribute to the input that is equal to the users rating */
        if (i == userRating) {
            userRatingHtml += `<input type="radio" id="star${i}" name="rating" value="${i}" checked/>
                           <label for="star${i}" title="text"><i class="fas fa-star"></i></label>`
        } else {
            userRatingHtml += `<input type="radio" id="star${i}" name="rating" value="${i}" />
                           <label for="star${i}" title="text"><i class="fas fa-star"></i></label>`
        }
    }
    $(".user-rating").html(userRatingHtml);
})

/* Get current year and render in copyright section of footer */
$(".copyright span").text(function() {
    let y = new Date()
    let year = y.getFullYear();
    return year;
})

/* Render appropriate image or file input on edit_recipe */
$("input[name='image_options']").change(function () {
    if ($("#keep_image")[0].checked === true) {
        $("#keep-image-preview").show();
        $("#default-image-preview").hide();
        $(".add-image-div").hide();
    } else if ($("#default_image")[0].checked === true){
        $("#default-image-preview").show();
        $("#keep-image-preview").hide();
        $(".add-image-div").hide();
    }
    else {
        $(".add-image-div").show();
        $("#keep-image-preview").hide();
        $("#default-image-preview").hide();
    }
})

/* Use recipe name as alt attribute on user uploaded images */
$("document").ready(function () {
    $('.user-image').each(function() {
        let recipeTitle = $(this).parent().siblings('.recipe-card-title').text();
        $(this).attr('alt', recipeTitle);
    })
})