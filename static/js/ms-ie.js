// Script partly based on the accepted answer here: https://stackoverflow.com/questions/19999388/check-if-user-is-using-ie

var ua = window.navigator.userAgent;
var msie = ua.indexOf("MSIE ");

if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./)) {
    //Add ie class if user is using Internet Explorer
    var body = document.getElementsByTagName('body')[0];
    body.classList.add('ms-ie');
}