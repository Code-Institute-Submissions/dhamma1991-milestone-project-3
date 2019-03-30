// There are many ways to pick a DOM node; here we get the form itself and the email
// input box, as well as the span element into which we will place the error message.

var form  = document.getElementsByTagName('form')[0],
    track_title = document.getElementById('track_title'),
    artist = document.getElementById('artist'),
    youtube_link = document.getElementById('youtube_link'),
    year = document.getElementById('year'),
    error = document.querySelector('.error');

form.addEventListener("submit", function (event) {
  // Each time the user tries to send the data, we check
  // if the email field is valid.
  if (!track_title.validity.valid || !artist.validity.valid || !youtube_link.validity.valid || !year.validity.valid)  {
    // And we prevent the form from being sent by canceling the event
    event.preventDefault();
  }
}, false);