var form  = document.getElementsByTagName('form')[0],
    track_title = document.getElementById('track_title'),
    artist = document.getElementById('artist'),
    youtube_link = document.getElementById('youtube_link'),
    year = document.getElementById('year'),
    genre = document.getElementById('genre'),
    user_name = document.getElementById('user_name'),
    description = document.getElementById('description'),
    error = document.querySelector('.error');

form.addEventListener("submit", function (event) {
  // Each time the user tries to send the data, we check
  // if the email field is valid.
//   if (!track_title.validity.valid || !artist.validity.valid || !youtube_link.validity.valid || !year.validity.valid)  {
    if (!track_title.validity.valid) {
        $("#track_title").removeClass("valid");
        $("#track_title").addClass("invalid");
        $("#track_title_label").addClass("active");
        $("#track_title").prop("aria-invalid", "true");
        // And we prevent the form from being sent by canceling the event
        event.preventDefault();
    }
    if (!artist.validity.valid) {
        $("#artist").removeClass("valid");
        $("#artist").addClass("invalid");
        $("#artist_label").addClass("active");
        $("#artist").prop("aria-invalid", "true");
        // And we prevent the form from being sent by canceling the event
        event.preventDefault();
    }
    if (!youtube_link.validity.valid) {
        $("#youtube_link").removeClass("valid");
        $("#youtube_link").addClass("invalid");
        $("#youtube_link_label").addClass("active");
        $("#youtube_link").prop("aria-invalid", "true");
        // And we prevent the form from being sent by canceling the event
        event.preventDefault();
    }
    if (!year.validity.valid) {
        $("#year").removeClass("valid");
        $("#year").addClass("invalid");
        $("#year_label").addClass("active");
        $("#year").prop("aria-invalid", "true");
        // And we prevent the form from being sent by canceling the event
        event.preventDefault();
    }
    if (!$('#genre').val()) {
        $("#genre").removeClass("valid");
        $("#genre").addClass("invalid");
        $("#genre_label").addClass("active");
        $("#genre").prop("aria-invalid", "true");
        // And we prevent the form from being sent by canceling the event
        event.preventDefault();
        $('select').material_select();
    }
    if (!user_name.validity.valid) {
        $("#user_name").removeClass("valid");
        $("#user_name").addClass("invalid");
        $("#user_name_label").addClass("active");
        $("#user_name").prop("aria-invalid", "true");
        // And we prevent the form from being sent by canceling the event
        event.preventDefault();
    }
    if (!description.validity.valid) {
        $("#description").removeClass("valid");
        $("#description").addClass("invalid");
        $("#description_label").addClass("active");
        $("#description").prop("aria-invalid", "true");
        // And we prevent the form from being sent by canceling the event
        event.preventDefault();
    }
}, false);

$('#genre').change(function() {
    $("#genre").removeClass("invalid");
    $("#genre").addClass("valid");
    $("#genre_label").addClass("active");
    $("#genre").prop("aria-invalid", "true");
    // And we prevent the form from being sent by canceling the event
    event.preventDefault();
    $('select').material_select();
})