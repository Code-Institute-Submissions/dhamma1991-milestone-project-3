// Grab the form inputs as variables
var form  = document.getElementsByTagName('form')[0],
    track_title = document.getElementById('track_title'),
    artist = document.getElementById('artist'),
    youtube_link = document.getElementById('youtube_link'),
    year = document.getElementById('year'),
    genre = document.getElementById('genre'),
    user_name = document.getElementById('user_name'),
    description = document.getElementById('description'),
    error = document.querySelector('.error');
    
/* With thanks to Manik Anora's answer in this stackoverflow thread https://stackoverflow.com/questions/28735459/how-to-validate-youtube-url-in-client-side-in-text-box
    for this excellent function */
function validateYouTubeUrl() {    
    var url = $(youtube_link).val();
    
    if (url != undefined || url != '') {        
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2].length == 11) {
            return;
        } else {
            $("#youtube_link").removeClass("valid");
            $("#youtube_link").addClass("invalid");
            $("#youtube_link_label").addClass("active");
            $("#youtube_link").prop("aria-invalid", "true");
            event.preventDefault();
        }
    }
}

form.addEventListener("submit", function (event) {
  // Each time the user tries to send the data, check
  // if the fields are valid.
  // If any field is not valid, apply the appropriate Materialize styles and
  // prevent the form from being submitted
  // The actions taken here are broadly the same for all form field inputs with the exception of
  // the YouTube URL input, which uses the validateYouTubeUrl function defined above.
    if (!track_title.validity.valid) {
        $("#track_title").removeClass("valid");
        $("#track_title").addClass("invalid");
        $("#track_title_label").addClass("active");
        $("#track_title").prop("aria-invalid", "true");
        event.preventDefault();
    }
    if (!artist.validity.valid) {
        $("#artist").removeClass("valid");
        $("#artist").addClass("invalid");
        $("#artist_label").addClass("active");
        $("#artist").prop("aria-invalid", "true");
        event.preventDefault();
    }
    
    validateYouTubeUrl();

    if (!year.validity.valid) {
        $("#year").removeClass("valid");
        $("#year").addClass("invalid");
        $("#year_label").addClass("active");
        $("#year").prop("aria-invalid", "true");
        event.preventDefault();
    }
    
    // If the genre select has an empty value (is still on placeholder)
    // or the user has 'Add a Genre' selected (possible if the user 
    // uses the back button on their browser to exit add-genre.html)
    if (!$('#genre').val() || $('#genre').val() == 'add-genre-link') {
        $("#genre").removeClass("valid");
        $("#genre").addClass("invalid");
        $("#genre_label").addClass("active");
        $("#genre").prop("aria-invalid", "true");
        event.preventDefault();
        $('select').material_select();
    }
    
    /* Check that user_name exists before checking it is valid
        user_name will not exist in the case of the edit track form,
        in which case this if block prevents an error from occuring in the console
        in the browser */
    if (user_name) {
        if (!user_name.validity.valid) {
            $("#user_name").removeClass("valid");
            $("#user_name").addClass("invalid");
            $("#user_name_label").addClass("active");
            $("#user_name").prop("aria-invalid", "true");
            event.preventDefault();
        }
    }
    
    if (!description.validity.valid) {
        $("#description").removeClass("valid");
        $("#description").addClass("invalid");
        $("#description_label").addClass("active");
        $("#description").prop("aria-invalid", "true");
        event.preventDefault();
    }
}, false);

$('#genre').change(function() {
    $("#genre").removeClass("invalid");
    $("#genre").addClass("valid");
    $("#genre_label").addClass("active");
    $("#genre").prop("aria-invalid", "true");
    event.preventDefault();
    // With the select box, ensure the select is initialised again
    $('select').material_select();
})