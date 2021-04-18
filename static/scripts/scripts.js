/* autoResize jQuery plugin written by James Padolsey http://james.padolsey.com 
   autoResize() used to make textarea input expand with text input*/
$(".auto-resize").autoResize();

/* RENDER NEW ROWS IN ADD_RECIPE AND EDIT RECIPE FORMS WHEN PLUS BUTTON CLICKED */
$("#add-ingredient-button").on('click', function () {
    ingredientItems = $(".ingredients-container .form-input");
    /* Check that all the boxes in the ingredient container have some text in them before rendering a new text input */
    for (let i = 0; i < ingredientItems.length; i += 1) {
        /* If there's a text input without text, trigger tooltip and exit function */
        if (ingredientItems[i].value == "") {
            $(ingredientItems[i]).tooltip({ title: "Please use this input first!" }).tooltip('show');
            setTimeout(() => {
                $(ingredientItems[i]).tooltip('dispose');
            }, 2500)
            return;
        }
    }
    /* All inputs have text, get number to add to name attribute in form and render a new input to ingredients container*/
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


/* ADD EXISTING VALUES TO EDIT_RECIPE PAGE AND OVER-WRITE WTFORMS NAME ATTRIBUTES */
$("document").ready(function () {
    /* Get value passed to the placeholder attibute in template and 
    use as inner text value. This is because value attribute in template cannot be used
    to set text in the textarea input. Then, overwrite name attribute provided by WTForms and set equal 
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

/* ADD SELECTED-IMAGE CLASS TO 'CHECKED' IMAGE OPTIONS INPUT IN EDIT RECIPE */
$("document").ready(function(){
    $("input[name='image_options']").change(function () {
        if ($("#keep_image")[0].checked === true) {
            $("#keep-image-option").addClass('selected-image-option').removeClass('image-option');
            $("#default-image-option").addClass('image-option').removeClass('selected-image-option');
            $("#add-image-option").addClass('image-option').removeClass('selected-image-option');
        } else if ($("#default_image")[0].checked === true){
            $("#default-image-option").addClass('selected-image-option').removeClass('image-option');
            $("#keep-image-option").addClass('image-option').removeClass('selected-image-option');
            $("#add-image-option").addClass('image-option').removeClass('selected-image-option');
        }
        else {
            $("#add-image-option").addClass('selected-image-option').removeClass('image-option');
            $("#keep-image-option").addClass('image-option').removeClass('selected-image-option');
            $("#default-image-option").addClass('image-option').removeClass('selected-image-option');
        }
    })
})

/* VALIDATE FILE UPLOAD SIZE IN ADD AND EDIT RECIPE FORMS  */
/* Check that the selected file in the image upload input on add_recipe is below 1mb.
If not, remove the file from the input and fire an alert */
$("#picture_upload").change(function () {
    if ((this).files[0].size > 1000000){
        (this).value = null;
        alert('File size too big, please choose a smaller file.')
    }else {
        /* The file is below 1mb. Get the name of the file selected in the file input on 
        and render to page */
        $("#selected-file").text($("#picture_upload").val().split("\\").pop());
    }
})

/* This is the same as the function above, but for the edit_recipe page */
$("#new_picture_upload").change(function () {
    if ((this).files[0].size > 1000000){
        (this).value = null;
        alert('File size too big, please choose a smaller file.')
    }else
    $("#selected-file").text($("#new_picture_upload").val().split("\\").pop())
})

/* MAKE 'FAVOURITE-RECIPE' CHECKBOX AUTO SUBMIT WHEN CLICKED (TOGGLE FAVOURITE) */
$(".trigger-form-send").on('click', function () {
    console.log($(this));
    $(this).submit();
});

/* IF THE RECIPE CARD TITLE CONTAINS 28 OR MORE CHARACTERS, APPLY SHRINK-HEADER CSS CLASS */
$(".recipe-card-title").each(function () {
    if ($(this).text().length >= 28) {
        $(this).addClass('shrink-header');
    }
})

/* ENABLE BOOTSTRAP POPOVERS AND 'DISMISS ON NEXT CLICK' */
$(function () {
    $('[data-toggle="popover"]').popover({ html: true });
    $('[data-toggle="tooltip"]').tooltip();
})

$('.popover-dismiss').popover({
    trigger: 'focus'
})

/* ADD SLIDE DOWN AND SLIDE UP ANIMATION TO FLASHED MESSAGES */
$(".flashed-messages").hide().slideDown('slow', function () {
    setTimeout(function () {
        $(".flashed-messages").slideUp();
    }, 4000)
});

/* RENDER AVERAGE RATING STARS TO PAGE */
$("document").ready(function () {
    $(".ratings-container").each((index, container) => {
        /* Get rating passed to each ratings-container in templates */
        let rating = parseFloat(container.innerText)
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
        container.innerHTML = ratingHtml;
    })
})

/* RENDER USER RATING STARS TO PAGE */
$("document").ready(function () {
    let userRating = parseInt($(".user-rating").text());
    let userRatingHtml = "";
    /* Due to the CSS reversing the row of ratings, the for loop needs a descending counter */
    for (let i = 5; i > 0; i--) {
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

/* GET CURRENT YEAR AND RENDER IN COPYRIGHT SECTION OF FOOTER */
$(".copyright span").text(function() {
    let y = new Date()
    let year = y.getFullYear();
    return year;
})

/* SET NEW_IMAGE RADIO OPTIONS TO 'CHECKED' WHEN FILE LOADED IN FILE INPUT */
function fileLoaded(input){
    if (input.files[0]){
        $("#new_image").trigger('click');
    }
}

/* USE RECIPE NAME AS ALT ATTRIBUTE ON USER UPLOADED IMAGES */
$("document").ready(function () {
    $('.user-image').each(function() {
        let recipeTitle = $(this).parent().siblings('.recipe-card-title').text().trim();
        $(this).attr('alt', recipeTitle);
    })
    $('.recipe-page-image').each(function() {
        let recipeTitle = $(this).siblings('h1').text().trim();
        $(this).attr('alt', recipeTitle);
    })
})
