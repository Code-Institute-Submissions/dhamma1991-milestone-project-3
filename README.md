# Milestone Project 3 – DESERTISLAND Music App built with the Flask framework

## Table Of Contents

[1. Introduction](#1-introduction)

----------

[2. UX](#2-ux)

[2.1. User Stories](#21-user-stories)

[2.2. Wireframes](#22-wireframes)

----------

[3. Features](#3-features)

[3.1. Navbar](#31-navbar)

[3.2. Homepage (index.html)](#32-homepage-index.html)

[3.3. Charts (tracks.html](#33-charts-tracks.html)

[3.4. ‘Like’ System](#34-like-system)

[3.5. Track Detail](#35-track-detail)

[3.6. Edit Functionality](#36-edit-functionality)

[3.7. Delete Functionality](#37-delete-functionality)

[3.8. Track Submission](#38-track-submission)

[3.9. And and Edit Track Forms](#39-and-and-edit-track-forms)

[3.10. Add Genre](#310-add-genre)

[3.11. Database Stats](#311-database-stats)

[3.12. About Page](#312-about-page)

----------

[4. Features Left to Implement](#features-left-to-implement)

[4.1 'First' and 'Last' buttons on the chart page](#41-first-and-last-buttons-on-the-chart-page)

[4.2. Custom pagination](#42-custom-pagination)

[4.3. User Authentication System](#43-user-authentication-system)

----------

[5. How Existing Features Fulfil User Requirements](#how-existing-features-fulfil-user-requirements)

[5.1. Hardcore Sharer](#hardcore-sharer-features)

[5.2. Chart Observer](#chart-observer-features)

[5.3. Music Socialiate](#music-socialite-features)

----------
[6. Technologies Used](#technologies-used)

----------

[7. Testing](#Testing)

[7.1. Code Validation](#code-validation)

[7.2. User Stories Testing](#user-stories-testing)

[7.3. Other Testing](#other-testing)

[7.4. Browser and Responsiveness Testing](#browser-and-responsiveness-testing)

[7.5. Known Issues](#known-issues)

----------

[8. Deployment](#deployment)

----------

[9. Credits](#credits)

[9.1. Images](#images)

[9.2. Acknowledgements](#acknowledgements)

--------------------
## 1. Introduction
This project is a music database app called DesertIsland, where users submit their favourite music, which can then be voted on by other users. Built primarily with Flask on the backend, Materialize on the frontend, and MongoDB handling the database, the app features a chart system which dynamically alters the ranking of songs based on user feedback in the form of ‘Likes’. Each submitted track has an associated music video (from YouTube), so users are able to check out other’s submissions before they cast a vote. The charts can be filtered by decade, showing only tracks from the 90s for example, and can also be sorted by various criteria, and is not simply limited to showing the most popular tracks first. Users may also edit and delete submissions, and view detailed information about a submission.
## 2. UX
DesertIsland is aimed at music fans. The likely user is someone with a higher than average interest in music, and a desire to share their music taste with the world. The app serves as a way for users to see how much others share their taste in music, and also allows more casual users to see ‘what’s hot’, and what music fans generally agree on as good music.
### 2.1. User Stories
Three types of users have been identified as the typical user types for this app.
#### 2.1.1. Hardcore Sharer
The hardcore sharer is someone who would make multiple submissions to DesertIsland. This type of user would be typically one who also engages heavily in social media in general. This user type would want a clear and easy way to submit music, and ideally, a way for them to track their uploads and the number of Likes they have acquired. 
#### 2.1.2. Chart Observer
This type of user may or may not also be a hardcore sharer. They will however have an above average interest in music, and be curious as to how the rankings of music on the app look, seeing whether they agree or disagree with other’s votes. This type of user would need to see a clearly organised charts page.
#### 2.1.3. Music Socialiate
This type of user is someone who is interested in the broader community surrounding music. They would likely be interested in social share capabilities, forums, and perhaps a messaging and ‘friend’ system. This type of user has not been catered for in the first release of the app, and the features they would require are planned for an updated release.
### 2.2. Wireframes
Prior to work beginning on the app, wireframes were created to aid the design process and provide direction during actual coding. These can be found in the "wireframes" folder in the root directory of the project.

The wireframes are not a complete picture of how the app in its finished form looks. I do find wireframes very helpful in establishing the colour scheme and overall aesthetics of the app, as well as providing the general structure and layout of pages. However, often during development I find that features need to be added which were not foreseen, or layouts tweaked in order to accommodate content in practicality. The wireframes merely serve as a ‘launch pad’ for the app. In addition, some pages do not feature an overly complex layout, in which case they have no wireframe. In other cases, I can picture the design in my head without concrete sketches.

Along with designs for the app itself, within the wireframes directory you may find a sketch for the database schema.
## 3. Features
DesertIsland is a website built from multiple HTML pages, with the backend handled by the Python Flask framework. The bulk of the custom backend code within the project can be found within the app.py file.
### 3.1. Navbar
The main nav for the app is located at the top of every page, implemented by using Materialize classes. The nav is fairly basic, consisting of the DesertIsland brand logo and some links. On smaller viewports the nav collapses, with the links replaced by a menu icon. If the user clicks or taps on the icon, a sidenav appears on the left of the viewport where the user is able to view the navlinks. The user is able to close the sidenav by tapping or clicking off of the sidenav, or by clicking the close icon in the top right of the sidenav.

The Materialize nav system by default does not include a close icon for the sidenav. I added this manually by adding a Material close icon, which is wired up to a method provided by Materialize called sideNav(‘hide’).
### 3.2. Homepage (index.html)
The homepage serves as the landing page for the app. An eye-catching image of Jimi Hendrix is used to draw the attention of users. The text on the image serves as a very brief, catchy, description as to what the app’s function is.

The image makes use of Materialize’s parallax effect, meaning the image and the page scroll at different ‘speeds’. This effect is intended to help give the app a modern appearance.

Care was taken to ensure that the legibility of the text over what was a very colourful image was maintained.  A darker opaque overlay on the image was used in order to maintain contrast between the image and the white text, this was achieved with CSS.

The image is set to be 100% of the viewport’s height. This means that no matter the device on which the app is being viewed, the user will see just the navbar and the image. I like the consistency this provides between platforms.

Different images are loaded depending on the size of the viewport, with smaller (and more efficient) images loaded for smaller viewports. A HTML <picture> element is used to this effect. In order for this to work, the Materialize JS handling the parallax effect had to be modified, since by default it looks for an <img> element to add the parallax effect to, and not <picture>. These minor modifications can be found in the uncompressed version of the materialize.js file within the project. 

I’m aware that modifying a library’s code may be an undesirable action to take, considering the implications when it’s time to update. However, due to the fairly basic modifications undertaken to materialize.js, I decided that for this project it was a reasonable step to take.

The next section on the homepage is the current top 3 tracks on DesertIsland. This list is determined by some code within app.py that retrieves a list of tracks ordered by upvotes, limited to the top 3 results. Each track in displayed with its rank number (i.e. 1st, 2nd), the artist name, track title, and a linked YouTube video. The rank number, artist, and track title text is a clickable link which can take the user to track-detail.html. This page serves as the detailed view for each object (track) in the database.

Below the list of top 3 tracks there is a link to the charts page with the text ‘View The Full Charts’. This takes the user to the charts page. Below this link is another parallax image. This one contains a call to action, the text ‘Help Us Find The Most Loved Music Of All Time’, which contains a link through to add-track.html. 

At the bottom of the page is the footer, containing the same nav links as the top navbar as well as some copyright info. Note the copyright date is auto-generated using JavaScript.
### 3.3. Charts (tracks.html)
The charts page essentially gives an overview of the objects in the tracks collection within the database. Each of these objects represents a track submitted by a user. You can view a sketch of the database schema within the wireframes directory within the project.

A for loop within tracks.html is used to render a number of <section> elements, with each <section> element representing a track. The list of tracks is determined by the [filter](#filter-system) and [sort](#sorting-system) systems. Each track contains the following:

1.	The rank number of the track
2.	Artist
3.	Title
4.	Like button and Like count
5.	The name of the user who submitted
6.	Date of submission
7.	Edit and Delete buttons
8.	An embedded YouTube video

#### 3.3.1. Rank Number of the Track
This is determined by combining the index of the track loop, added to the current pagination. For example, if the user clicks ‘Next’ to view tracks 6 through 10, the rank number ‘6’ is determined by adding the loop index of that track (1) to the current pagination value (in this case 5). If the user clicks ‘Next’ again to see tracks 11 through 15, then the pagination values of 10 will be added to the loop indexes on the page to get the values 11 to 15.
#### 3.3.2. Artist and Track Title
Determined by the ‘tracks’ passed through from the backend.
#### 3.3.3. Like Button and Like Count
The ‘Like Button’ is technically a form, with a submit button that goes to the upvote_track view within app.py. This view increments the upvote_count of the selected track by 1. The upvote button knows which track to modify by being tied to track.id. The icon used to represent a ‘Like’ (a thumbs-up icon common to the internet) is a Material Icon. Some JavaScript ensues that once the user ‘Likes’ a track, the scroll of the page stays on the track they just Liked. The JavaScript also depends on a bit of Flask functionality, you can read more details on this in the [Like Scroll Script section](#like-scroll-script) of this readme.
#### 3.3.4. Name of User Who Submitted and Date Submitted
Retrieved from the track object and passed through to the template similarly to the artist and track title.
#### 3.3.5. Edit and Delete Buttons
The Edit and Delete buttons take the user to the edit pages or delete confirmation pages respectively for the tracks. More information about the Edit and Delete functionality can be found [here for Edit](#edit-functionality) and [here for Delete](#delete-functionality).
#### 3.3.6. Embedded YouTube Video
The embedded YouTube videos that load initially are not technically videos at all, but image thumbnails. When the user clicks on the thumbnail, the YouTube video loads in its place. This was done to save on the user’s bandwidth, since loading 5 YouTube videos on a page simultaneously is very likely to affect the overall load time of the page. The image is made to look like a video by using css to generated a play icon.

This functionality is accomplished using a very nice piece of JavaScirpt courtesy of [this article](https://webdesign.tutsplus.com/tutorials/how-to-lazy-load-embedded-youtube-videos--cms-26743). I modified the CSS provided by the article (CSS that styles the YouTube image) to fit with SCSS syntax, but the modifications to the JavaScript itself were minor. The images are responsive, and scale down to always fit the viewport’s width, scaling up to a maximum of 730px width, which fits with the layout of the page on larger viewport sizes. The video that loads in place of the image when the image is clicked on is sized to match the image’s size.
#### 3.3.7. Pagination System
There are 5 tracks per page. If more than 5 tracks meet the criteria of the user’s current filter, then they will be available via pagination. In order to navigate through the tracks, the user can click the ‘Next’ and ‘Previous’ buttons located at the bottom of the charts page just above the footer. The Next and Previous buttons display dynamically; the Next button will not display if the user has reached the end of the list of tracks, and the Previous button will not display if the user is at the beginning of the list. 

The pagination system is implemented using session variables, which get passed through to the template. This means that in some use cases, the pagination gets saved, meaning the user won’t always go back to the first 5 tracks. For example, if the user clicks the ‘Next’ button 3 times, and then decides to edit track 20, they probably do not want to be taken back to the first 5 tracks once they finish editing and return to the charts page. Rather, the pagination they were on is saved, and they go back to the 5 tracks they were viewing before clicking ‘Edit’.
#### 3.3.8. Filter System
Users are able to filter the tracks on the chart page by decade. Users are able to choose between the various decades by manipulating the decade filter box at the top of the page. The decades available range from music released before 1950, to each decade up to and encompassing the present decade.

The decade filter system uses a combined jQuery/Flask solution in order to get the correct list of tracks for the user and ensure the decade filter displays the correct text, matching the user’s selection.

The decade filter on the frontend is a HTML select element populated by an option for each decade. A jQuery event listener awaits a change on the select, and goes to get_tracks (the view that goes to the charts page), passing through the value the user selected via the select box to the get_tracks view. This value is then used to determine which tracks to show, by filtering the results of tracks_collection.find()  by the decade, using the value for the ‘Year’ field of the tracks objects.

I personally find the switch statement used by the jQuery to pass the decade value to get_tracks a bit cumbersome. However, the value of the select box cannot be passed directly into url_for(get_tracks), since JavaScript cannot be evaluated in Jinja. An alternative would be to [use AJAX](https://stackoverflow.com/questions/36143283/pass-javascript-variable-to-flask-url-for), but AJAX was beyond the scope of this project.

Once get_tracks has been called and the charts page re-rendered with the updated list of tracks, a further bit of jQuery ensures that the value of the decade select is set to the current decade. By default, the select box would again be set to ‘Show All’.
#### 3.3.9. Sorting System
Users are able to sort the tracks on the chart page either by number of Likes (either ascending or descending) or Date Added (again either by ascending or descending). The sort dropdown at the top of the charts page, situated just below the decade filter dropdown, handles this functionality. The design of the sort dropdown was influenced by the design of the sort option for posts on Reddit.

The sorting dropdown is achieved differently to the decade filter, despite both systems using dropdowns. The sort dropdown makes uses of the Materialize framework’s dropdown component, unlike the decade select which is just a HTML select element rendered with Materialize.

When the user clicks on a sorting option, they get taken to its respective sorting view, of which there are 4, within app.py. All the sorting view does is tell get_tracks, which the sorting view redirects to, which sorting order to use when the tracks are being determined within get_tracks. The get_tracks view then loads the charts page and shows the tracks.

A bit of jQuery ensures that the text on the sorting dropdown matches the user’s actual sorting, or else similarly to the decade filter, the wrong option will be displayed on the dropdown. 
#### 3.3.10. No Tracks Message
If there is a decade that currently has no uploaded tracks (e.g. there are no tracks from pre-1950 on the database), the user will be shown a message telling them that no tracks match that period, with a link to take them to the add-track form. This is to avoid the app looking broken or otherwise incomplete, as without the message the user would just see a lot of white space between the sort dropdown and the footer.

This functionality is accomplished with a conditional check by the Jinja within the template, checking that tracks_count (established within app.py) is greater than 0. If tracks_count is greater than 0, the tracks get shown. Otherwise, the ‘no tracks’ message gets shown.
### 3.4. ‘Like’ System
A core part of the app is the Like system, which records the number of times a user has clicked on the Like button for a given track. 

This system was previous referred to as the ‘Upvote’ system, inspired by the system found on Reddit. This was changed during some initial testing; all of the four people who took part in the testing, bar one, did not know what an Upvote was, something I had (previously) assumed was obvious. This led me to decide, for the benefit of usability, to replace the word ‘Upvote’ with ‘Like’, in order to make DesertIsland’s system more in-tune with the systems of ubiquitous applications like Facebook and Instagram.

‘Upvote’ can still be found referred to in the code in the backend, as well as in the wireframes, with only references to it in the frontend being replaced by ‘Like’. I didn’t see the need to invest the time or effort in changing the backend code, especially considering that ‘Upvote’ and ‘Like’ are synonyms.

Users are able to Like a track in two places on the app. The first place is on the charts page, which each track being rendered a long with a Like button. The second place is on the detail page for each track.

A check within the upvote_track view ensures that once a Like has been submitted, the user goes back to the right place; it would be confusing if a user Liked a track from the charts page, to then be taken to that page’s track-detail.

When a user submits a track, the track starts off with 1 Like already in place. This is due to the assumption that a user who uploads a track already Likes it.
#### 3.4.1. Like Scroll Script
The Like Scroll Script is a bit of functionality added fairly late-on in the development process. The need for it arose during testing with a user called User X (you can read about that test [here](#other-manual-testing).

Prior to implementation of this script, the app would scroll back to the top of the page once the user had Liked a track on the charts page. This is not ideal, since if a user Likes a track towards the bottom of the charts page, they will lose where they were on the page. This has the potential to cause confusion.

In order for this script to have the desired effect, firstly, each track in the list of 5 needs a unique identifier, or else the JavaScript has nothing to cling on to. This is achieved by using Jinja to give each <section> element containing the tracks a unique id attribute, consisting of the id of the tracks from the database.

Next, when the user clicks Like, the id of the track is sent forward to get_tracks, and then passed through to the template and the JavaScript. The method scrollToView() is then called on the element with the id which gets passed through to the template.

It should be noted that the script has no effect if, once the user has Liked a track, that track ends up getting ‘promoted’ to the next level of pagination, e.g. if a track was rank 6, and the Like promotes it to rank 5, the user will be seeing tracks ranked 6-10, so the track they just liked will not be one of those. The pagination is not affected by this script.
### 3.5. Track Detail
The track detail page serves as a detailed view for each database item(i.e. each track). This page can be reached for each track from the charts page, with the rank number, artist and track title text serving as a clickable link.

The track-detail page shows the same information about each track as the chart page, with the addition of the user description for the track, as well as the genre and year released.

The user is also able to edit, delete, and Like tracks from the track-detail page.
### 3.6. Edit Functionality
Each track on the database can be edited, by any user. In the real world this would not be ideal, with the potential for abuse of the system becoming almost guaranteed. However, without an authentication system which is beyond the scope of this project, tying an edit to a particular user would be difficult.

Users are able to edit tracks by clicking on the Edit button for the track on both the charts page and on the detailed page for each track. This will take the user to an edit form. The form on the page allows the user to edit the details for a track.

There are a few fields that the user is not allowed to edit. One is the user_name field. The idea behind this is that I don’t want users ‘stealing’ other user’s submissions, and making the user_name field uneditable is probably the closest I can come to achieving this without implementing an authentication system. The date_added field and date_added_raw field are also not editable, this being something that would not make sense to edit. Lastly, the upvotes field is not editable, it being so would introduce a potential avenue for abuse of the system.

Other than the form, the edit track page also includes a link to Wikipedia, since some of the details asked for by the form might be information not readily available to the user (e.g. year of release).

The edit page and the add-track page are quite similar. One of the big differences is that the edit page comes with the form already filled in with the details for the track that the user has decided to edit. This is achieved by grabbing the track from the database using its ID passed through by the Edit button, and then filling in the details of the track within the edit form using Jinja.

Once the user has finished editing, or if they cancel their edit by clicking the Cancel Edit button, they are taken back to the charts page, retaining the pagination they were on before they went to edit the track. This is the case even if the user edits a track from a track-detail page. Ideally, in such a case the user would go back to the track-detail page once they had taken an action on the edit page, and not to the charts page. This is a current limitation of the app.

The edit form, along with the add-track form, is discussed more in detail [here](#add-and-edit-track-forms).
### 3.7. Delete Functionality
Each track in the database is able to be deleted. Any user can delete any track, including ones they did not submit. Without an authentication system, I’m unsure as to how to implement a delete system which limits deletions of tracks to the users who submitted them.

Tracks can be deleted from 2 places, either from the charts page or on the detail page for each track.

When the user clicks on the Delete button, they are first taken to a confirmation page. This page is intended to avoid user errors (i.e. misclicks on the Delete button).

Once the user deletes a track, or changes their mind and clicks the ‘No, Cancel’ button, they are taken back to the charts page. If the user clicks ‘No, Cancel’, they are always taken back to the charts page, even if they clicked ‘No, Cancel’ from a track-detail page. Ideally, if coming from a track-detail page, they would be taken back to that track-detail page when cancelling the delete, and not to the charts page. This is a current limitation of the app.
### 3.8. Track Submission
Users are able to submit a track to DesertIsland by using a form found on add-track.html. Users can get to this page by clicking the nav links in either the main nav or the footer. There is also a link on the call to action text on the bottom parallax image on index.html, and also if the user sets a decade filter that returns no tracks, they will be shown a link to add-track.html there as well.

The content on add-track.html is quite similar to the content found on edit-track.html. The forms used on both pages is discussed in detail [here](#add-and-edit-track-forms).
### 3.9. Add and Edit Track Forms
The forms on both the edit and add track pages are essentially the same. The primary difference is that when the user goes to add a track, they are presented with a blank form, whereas the edit form will have the selected track’s info already filled in. There is also a difference in where the form takes the user after it has been submitted. In the case off add-track, the user will go to the charts page with sorting order set to ‘Date Added (Newest)’ so that they can see their newly uploaded track at the top of the list, with pagination and decade filter set at defaults. In the case of an edit, the user will be taken back to the charts page, but with the current pagination, decade filter, and sorting order that they had before going to the edit.

The forms are constructed using Materialize classes. Materialize icons are used in order to improve the forms’ aesthetics, as well as make fields more recognisable.

Validation on the forms is handled client-side. Firstly, all fields must be entered and there can be no blank fields. Some fields also have a maxlength attribute assigned. I took care in choosing these values, especially for the track_title and artist fields. As can be seen on [this webpage](http://klck1400.com/seeing_is_believing/2933), some song titles can be very long. However, since pop music in general is designed to be short and catchy (with short and catchy song titles) it is not expected that many overly long track titles will appear on DesertIsland, since more popular music generally doesn’t feature them. Artist names tend to be a bit shorter, and the maxlength attribute for this input was inspired by [this article](https://musicmachinery.com/2012/01/07/have-artist-names-been-getting-longer/).

There is also some more complex validation on the ‘Year Released’ field, implemented using regex. Firstly, this input is limited to 4 characters. This covers all years from 1000AD up. Secondly, the first character of this field must be either a ‘1’ or ‘2’. This covers all years from 1000AD to 2999AD (providing a measure of future proofing). The limitation of this system is that any music that was released before 1000AD is not covered, although such music is not expected to be added in great numbers to DesertIsland due to the app’s focus on contemporary music.

Further client-side validation is achieved using JavaScript. An event listener is attached to the forms looking for a submit event. When a submit event occurs, the default is prevented and the custom functionality is implemented.

A part of the JavaScript involves checking for a correct YouTube video URL. This is a script that I found on [this stackoverflow thread](https://stackoverflow.com/questions/28735459/how-to-validate-youtube-url-in-client-side-in-text-box) which uses regex to check for the correct input of a YouTube video URL. 

The rest of the form validation JavaScript deals with adding/removing Materialize classes based on whether or not the form inputs are valid based on the attributes set within the HTML. With the JavaScript, the form cannot be submitted unless all fields are valid.

If the fields are valid, but upon submission it is found that a duplicate entry exists for a YouTube URL, the form will be rejected, the user will go back to add or edit track, and a message will be shown to them using the Flask flash framework that the insert was unsuccessful due to a duplicate video found in the database. This duplicate-checking functionality was added using an index within MongoDB. Deciding what fields should be unique, and which should not, was a challenge I discussed in [known issues](#less-than-optimal-duplicate-upload-checking-system).

It should be noted that failing the database index-based validation will reset the forms to their default state; in the case of add-track that means a blank form, and for edit-track, the details of the track as they currently exist in the database. 

In the case of add-track, this could be considered desired functionality; if the track already exists in the database, it makes sense to clear the form so that the user is ready to enter the details for a different track. In the case of edit-track, there are probably not many use cases where the user will need to edit the youtube_url; the client side validation should take care of input errors, and this is a field that is very likely to be copied and pasted. 

There is always the possibility that the user will copy/paste the wrong URL. If that happens, and the URL the user intended to paste already exists in the database, the user may find that the track they wanted to upload already exists. I'm not sure how to go about preventing a scenario like this, and may be something inherent in the nature of the app.
### 3.10. Add Genre
Most of the fields on the add and edit track forms are text inputs. The one exception is the genre input, which is a select box. The select box is populated with values from the genres collection in the database. If the user wishes to add their own genre, they can do so by clicking the ‘Add a Genre’ option, which is always the bottom option of the dropdown. This option is coloured differently to the actual genres, making it more apparent to the user.

By default, Materialize selects do not include links. I had to add this manually using jQuery. The jQuery listens for a change event on the select, and if the value of the select corresponds to the value of the add genre link, the user is taken to add-genre.html.

The add-genre.html page consists of a small form, with one input where the user can enter the name of their new genre. Upon submission of the form, the backend checks that the genre does not already exist. Indexing is used to ensure that the genre names ‘Soul’ and ‘soul’ for example are equivalent, so that if ‘Soul’ exists in the genres collection, ‘soul’ will be rejected. If the user’s genre is rejected because it is a duplicate, they will be taken back to add-genre.html, with a Flask flash message telling them that the genre already exists.

Care had to be taken that, upon successful submission of a new genre, that the user ends up in the right place. If they added a new genre from add-track, they will go back to add-track. Likewise, adding a new genre from edit-track will take the user back to edit-track. If the user manually goes to the add_genre URL (i.e. by entering it into the address bar and not using the link within the genre select) they will be taken to a blank add-track form upon submission of the genre.

Limitations of this system are discussed in [known issues](#the-genre-select).
### 3.11. Database Stats
The user may navigate to stats.html using either the main nav or the footer, which gives the user an overall picture of the content of the database. These values are collected through various calculations within the stats view of app.py. The current stats displayed are:

1.	The number of tracks uploaded on the database
2.	The decade with the most tracks uploaded
3.	The artist with the most uploaded tracks
4.	The genre represented by the most tracks
5.	The total number of Likes on the app
6.	The artist with the most likes

Within app.py, comments within the stats view give a more detailed breakdown of how these stats are calculated. 
### 3.12. About Page
This is a simple HTML page within the app, reachable by either the main nav or the footer. This page gives a very brief overview of the company behind DesertIsland, and an email link for users to get in touch.
## 4. Features Left to Implement
Some features are left open to the idea of implementation but were not featured in this release.
### 4.1. ’First’ and ‘Last’ buttons on the charts page
At the moment, users must rely on the Next and Previous buttons only, in order to work their way through the pagination of content on charts.html. It would be ideal if there was an easy way for users to go back to viewing the first (or last) 5 tracks. It is currently possible to go back to the first top 5 by clicking on the Sort option and selecting the same Sort option again, refreshing the page, or by clicking the Charts link on the nav to reload the page, but it would be ideal if there was a dedicated button or link to do this.
### 4.2. Custom pagination
Related to the above, currently the charts content is limited to 5 tracks per page, with no option to change this. It would be ideal if users could select their own pagination value, being able to choose perhaps 5, 10, or 20 tracks per page. I’ve noticed that in a lot of apps around the web where there is pagination of content, it is general practice to allow the user to customise the number of items per page.
### 4.3. User Authentication System
In my opinion, this app would not be in any way ‘real world’ worthy unless it had a user authentication system. This would enable far more functionality to be implemented.

Firstly, users could track their uploads. Each user account would be associated with a number of uploads, which could be visible to the user on a dedicated profile page. This would allow the number of Likes a user was getting to be tied to their account, allowing a ‘rep’ system to be developed, similarly to Reddit. I think this would increase the appeal of the project, allowing users to get the psychological satisfaction from getting ‘Likes’, something a lot of real world apps exploit in order to gain a userbase.

Secondly, edits and deletions could be tied to individual user accounts. The current system (of anyone being able to edit or delete any track) is simply not viable in the real world, and leaves the app open to being exploited and possibly destroyed by a single malicious user.

In addition, a user authentication system would enable more ‘social’ features. This could be a messaging system within the app that allows users to communicate with each other, as well as possibly a ‘friend’ or ‘follower’ system, which users could use to engage with fellow DesertIsland users to discuss uploads and music in general. 
## 5. How Existing Features Fulfil User Requirements
This section details how the features implemented in the current release of the project meet the requirements of the users discussed in the UX section.
<a name="hardcore-sharer-features">
### 5.1. Hardcore Sharer
</a>
This type of user has multiple places where they are able to get to add-track.html. This link is available in the nav and in the footer across the app, in the 2nd parallax image text on index.html, and also if the user’s decade filter selection comes up with no tracks on tracks.html.

Without an authentication system, this type of user currently does not have a way to track their uploads or Likes. This is a feature that could be added in a future release.
<a name="chart-observer-features">
### 5.2. Chart Observer
</a>
This type of user is served by tracks.html. The charts page allows them to clearly see where tracks sit in the various sorting orders. The decade filter allows them to refine the criteria and see what tracks are most popular in which decade. The charts page is designed to be as user-friendly as possible, so if the user spots something wrong with the listing of a track, they can edit that track, and then go back to the same 5 tracks they were viewing before the edit.
<a name="music-socialite-features">
### 5.3. Music Socialiate
</a>
The app currently does not possess any kind of social functionality, which was considered beyond the scope of the requirements for this project. Social functionality would be something added onto a future release.
## 6. Technologies Used
### [HTML5](https://www.w3.org/standards/webdesign/htmlcss)
The project's markup uses HTML5 and makes as much use of HTML5 semantics as possible using W3C standards.
### [CSS3](https://www.w3.org/standards/webdesign/htmlcss)
The markup is styled using CSS3.
### [SASS Pre-Processing](https://sass-lang.com/)
SASS pre-processing (using SCSS syntax) is used to render the project’s style.css file, making the process of creating CSS easier.
### [Materialize 0.100.2](https://getbootstrap.com/docs/3.3/)
Materialize is a front-end framework based on Google’s philosophy of “material design”. Materialize is used throughoout the app in order to simplify the process of generating the visual look and feel of the project.

A note on versions: the current stable version of Materialize is 1.0.0. This project makes use of an older version, 0.100.2. I was able to get client-side form validation for the add and edit track forms working only on the older version, and none of the learning materials I could find were applicable to the current version of Materialize, hence I was at a loss as to what exactly the problem was. I’m not sure what changed about 1.0.0. to complicate it in regard to form validation, but since the differences between the visual style and capabilities of 1.0.0 and 0.100.2 are small, I decided to stick with the older version.
### [Material Icons](https://material.io/tools/icons/?style=baseline)
Included as part of the Materialize framework. Provides a useful set of icons that can be used to represent actions and items.
### [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
JavaScript is scattered throughout the project to enable DOM manipulation. Its primary purpose is to enable the user of jQuery, but there are some examples of pure JavaScript found within the app (e.g. the copyright date script found at the bottom of base.html, the YouTube lazy loading script, and the tracks.html scrollIntoView() script).
### [jQuery 3.2.1](https://jquery.com)
The latest version of jQuery (at the time of writing) is 3.4.1. An older version was used in keeping with the version stipulated by [Materialize](http://archives.materializecss.com/0.100.2/getting-started.html).

jQuery is utilised by the project for a number of areas of functionality:

1. Materialize depends on jQuery for its JavaScript components
2. The link within the genre select on the add and edit track forms, which takes the user to add-genre.html.
3. The client-side form validation script.
4. Enables the proper functionality of the decade filter and track sort on tracks.html.

jQuery also enables user of [jQuery UI](#jquery-ui-112)
### [jQuery UI 1.12](https://code.jquery.com/ui/)
jQuery UI is a curated set of user interface interactions, effects, widgets, and themes built on top of the jQuery. 

For DesertIsland, jQuery UI is used to implement the tooltip that is attached to the YouTube URL input on the add and edit track forms.
### [Flask 1.0.2](http://flask.pocoo.org/)
Flask is a micro web framework used to support the development of the app and provide much of the backend functionality.
### [MongoDB](https://www.mongodb.com/)
MongoDB is a cross-platform document-oriented database program used to manage DesertIsland’s data.
### [PyMongo](https://api.mongodb.com/python/current/)
PyMongo enables working with MongoDB using Python
### [Flask-PyMongo 2.2](https://flask-pymongo.readthedocs.io/en/latest/)
Flask-PyMongo is a Python package that makes it easier to get Flask to work with PyMongo
### [Font Squirrel](https://www.fontsquirrel.com/tools/webfont-generator)
Used in order to turn .ttf fonts into webfonts (used in this project for the adumuregular font).
### [Real Favicon Generator](https://realfavicongenerator.net/)
This tool was used to construct favicons for the project. How favicons are rendered is different depending on the browser or platform used, and this tool simplifies the process by providing the appropriate markup and icon for each platform.
### [ImageResize.org](https://imageresize.org/)
Used for adjustment of the app’s images
### [Git](https://git-scm.com/)
Used for version control
### [GitHub](https://github.com/)
Used as the online hosting service for the git repository.
### [Heroku](https://dashboard.heroku.com/login)
Used to deploy the app on the web.
### [mLab](https://mlab.com/welcome/)
The online host for the database.
## 7. Testing
### 7.1. Code Validation
The W3C code validators for [HTML](https://validator.w3.org/) and [CSS](https://jigsaw.w3.org/css-validator/) were used to check markup validity. The validators helped me fix a few errors in the markup, one example for the HTML validation being a descendant 'button' element within an 'a' element that I’d used to construct the ‘Cancel’ button on a number of pages (which was fixed simply by replacing the 'button' with a 'div'). After these and other fixes, both the index.html and style.css files pass the testers with no errors.
### 7.2. User Stories Testing
Manual testing was conducted simulating the three types of users that have been previously identified in the [UX](#ux) section. This testing was conducted by myself (the developer). Manual testing was also conducted by other people, of which one tester was observed and documented, although this testing did not attempt to simulate the user stories identified in the UX section. The downside of conducting user testing simulations personally is that, as the developer of the app, I know it better than anyone else, and that familiarity might mask issues that would otherwise be apparent to another person. On the other hand, personally adopting another person’s perspective when testing did prove useful, and led me to implement new features in response to some issues discovered. 

The user categories simulated were:

1. Hardcore Sharer

2. Chart Observer

The 3rd category of user, the Music Socialite, was not simulated since the areas of functionality it was deemed necessary to implement in order to cater to this user were not added to the current release.

The results of these tests were as follows:
<a name="hardcore-sharer-testing">
#### 7.2.1. Hardcore Sharer
</a>
Upon loading the app, I am taken to index.html. I am able to appreciate the (rather cool) picture of Jimi Hendrix for a moment, before scrolling down. I see the current top 3 tracks, and the link ‘View The Full Charts’ which I click on. I take a look at the charts for a moment, navigating through the pagination using the ‘Next’ and ‘Previous’ buttons. I then decide I want to submit a track, and click the ‘Submit a Track’ link in the nav. I enter a new track, making use of the Wikipedia link in order to get the ‘Year Released’. Upon submitting the track, I am taken back to the charts page, where I can see my track is at the top of the list.

At this point in the testing, I realised that for the user to see their newly submitted track at the top of the charts might be confusing. If the user has yet to realise that the charts page automatically changes the sorting option to ‘Date Added (Newest)’ when the user submits a track, then the user may end up wondering why their track is suddenly number 1.

In order to help counter this, I decided to add a sub-heading to the charts page. This sub-heading is part of the h1 element on tracks.html, and is generated by passing  the value of sorting_order_text and decade_filter_text to the template, the values of these variables being determined at the same time as the sorting_order and decade_filter are calculated.

Carrying on with the test, I noticed I made a typo in the artist name of the track I just uploaded. I click the ‘Edit’ button of the track and am taken to the edit form. I make the edit, submit the edit and then I am taken back to the charts page.

I repeat the add track process a few times. During one of the submissions I am caught out by the validation, as I accidentally add ‘3002’ instead of ‘2002’ for the Year Released. The form will not submit, as the ‘Year Released’ input will only accept a 1 or 2 as the first character of the input. A logical bit of validation, as there is no music currently released in the 4th millennium. The validation allows me to correct my mistake before I submit the track.
<a name="chart-observer-testing">
#### 7.2.2. Chart Observer
</a>
I initially follow a similar process to the Hardcore Sharer, landing on index.html and taking a moment to explore the homepage. I then go to the charts page by clicking the link in the nav. I explore the charts for a few moments by clicking the ‘Next’ and ‘Previous’ buttons. I then decide to change the decade filter and take a look at the tracks from the 1990s. I can see the top track changes, and I recognise both it and other tracks as being from the 90s. I am able to change the decade to the 70s and 80s in the same way. I spot a track I like and click the Like button.

At this point I realised that there is no feedback from the app that a Like was successful. It could be apparent to the user anyway, especially if a track which previously had 1 Like now has 2, but this requires reliance on the user’s memory and attention, and also relies on the track not ending up in a different pagination as a result of the user’s Like, meaning it will not be a part of the 5 tracks the user is currently viewing.

I decided to use Flask’s messaging framework to feedback to the user that a track was Liked, to avoid any confusion. This message simply thanks the user for voting.

I Like a few more tracks. I find the message popping up after I Like a track to be useful, since there is no other visual feedback on the page except the number of likes changing. The fact the scroll is kept, so I don’t lose sight of the track I just Liked, is useful. It should be noted I conducted this simulation after the testing with User X which can be read about in the [Other Manual Testing section](#other-manual-testing). It was the testing with User X that led to the scroll script being added.
### 7.3. Other Manual testing
Apart from testing the app personally, I also made use of other people to test the app, most of whom were not developers. Feedback from these users was positive, with all agreeing that the site works well. With one of these tests I was able to sit with the person and observe and record them using the app. We can call this person User X.

Upon landing on the app, the first thing User X did was test the nav links. All links worked and there were no dead pages. The user then went to the charts page and began Liking tracks. At this point during the app’s development, the scroll functionality, which keeps the user scrolled to the track they just Liked (with the exception of if the track has changed its pagination), was not implemented. User X, who was Liking a few tracks, said out loud that they found it irritating that the page kept scrolling back to the top, even when the track the user Liked was at the bottom of the list of 5 tracks.

This feedback led me to implement the scrollToView() based JavaScript that is currently active on the app.

After User X had Liked a few tracks, I asked them to submit a new track. The user was able to do this without difficulty, although they did at first fail the form validation by not adding a track description. It took the user a moment to realise this, although in the end they did spot the red validation message asking them to add a description.

This concluded the test with User X.
### 7.4. Browser and Responsiveness Testing
The app was primarily tested on Google Chrome version 74.0.3729.169 on a Windows PC with a default maximised screen size of 1936px. 

In addition to Google Chrome's developer tools where mobile devices can be simulated, an iPhone 7 running iOS v11.3 was used to test the app with its native Safari browser. The website was also tested on Firefox v66.0.3, Safari v12.1.1 (on a MacBook Pro 15-inch Retina) and Edge v42.17134.1.0.

The app was developed mobile first. I tend to always work on projects with the browser set to simulate a mobile device. I build the app from there, and when it looks right on the smaller viewports I make any changes it needs to work on the larger viewports.

No issues were detected on any of the tested browsers in terms of either layout or functionality.

In addition to modern browser testing, the app was tested on IE version 11.0.9600.19130. On this browser, none of the charts were rendered. After some searching, I found that DC.js is tested in IE but that [mine wasn’t the only issue] https://stackoverflow.com/questions/50047687/dc-js-im-facing-issues-rendering-the-dc-js-dashboards-in-ie-11) and that issues relating to DC.js working with IE [have been documented](https://github.com/dc-js/dc.js/issues/1334).

Due to IE being a legacy browser, and with Windows 10 (and Edge) becoming more and more common, I adopted to not support IE in any of its incarnations. To this effect, a user trying to view the app on IE will see a page similar to the no-js functionality, asking them to upgrade their browser.
### 7.5. Known Issues
There are several issues with the app that were not tackled in the current release, mainly because of the time it would have taken to implement fixes.
#### User loses form data when adding genre
At the moment, uses who partially complete either the add or edit track form, and then go to add a genre, will have lost the data they have already inputted into the add or edit form when returning to the form. This could be considered an annoying feature of the forms at present, especially since the Genre input is likely to be the 3rd or 5th input the user goes to (due to the layout of the forms), meaning they’ll lose the data they’ve inputted before that.

It should be noted that the user doesn’t return to a blank form when going back to the edit page. They data for the track the user wanted to edit will still be there, just any changes the user has made since going to the edit form will not have been saved.

This could perhaps be fixed by storing the form data in a session when the user goes to the add-genre page, and then restoring the form to how it was before the user went to add a genre.
#### Less than optimal duplicate upload checking system
It is desirable in most types of databases to avoid duplicate data entry, and this app is no exception. I did however struggle to develop a system that would make this really watertight, namely due to the nature of the data being dealt with. For example, it isn’t possible to prevent duplicates on the basis of track_title, since there are a great number of songs out there which share the same name, but are by different artists and share no relation.

A compound index, implemented using MongoDB, checking that both the track_title and artist are unique would be a better solution, but even this is not fully watertight; many artists make several versions of the same song, perhaps recorded at different times, or remastered, or even live versions. In addition, relying on the artist and track_title relies on the user entering them in precisely the right format; the database would not detect that “The Rolling Stones” and “Rolling Stones” are actually referring to the same artist, unless extensive checks were made that handled scenarios like these.

It was therefore decided to go with the youtube_link. This is the one thing that can be guaranteed to render unique entries for the database, at least in regards to the YouTube videos. And although this doesn’t prevent, say, the exact same recorded version of “Hey Jude” by The Beatles showing up in the database, simply with two different YouTube uploads, I felt like it was the best solution I could come up with without some very extensive work being undertaken on MongoDB.
#### Capitalization of user uploads
There is currently no uniform way that the app handles user input in regards capitalization. For example, if the user enters “the beatles” and “yellow submarine” as a track submission, the app will render the text as “the beatles – yellow submarine” when ideally in this case the app would use the correct grammar of “The Beatles – Yellow Submarine”. 

The app is currently wholly reliant on the user getting the capitalization correct for their uploads. It could be argued that there is no easy fix for this. For example, some artists purposely use irregular capitalizations as part of their name (e.g. the band KoRn or the rapper KRS-One). Forcing a capitalization system on the user’s inputs thus has the potential to backfire, by not accurately handling how the capitalization should be represented.

As some defence against this issue, there is text above the add and edit track forms asking the user to check their spelling and grammar. The system itself however currently has no powers to enforce this.
#### The genre select
The genre select is q form input element on both the add and edit track forms. The main issue with this element is that if the list of genres on the database grows too large, the select will become cumbersome and unwieldy to use. As it is, the genre select is fine with about 20 genres, but if users eventually added something like 500 genres (which is possible given the diverse nature of music) then a different solution would have to be implemented.

A second problem here is that users have to manually look for the genre they want to add within the select. An ideal solution would be find and search functionality, so that a user could begin typing the name of the genre they want, and the genres matching the user’s search would come up via predictive search.
#### Redundant ‘date_added_raw’ and ‘date_added’ fields
This refers to the schema of the database. Currently, there are two fields used to store data on the date that a track was uploaded. The field ‘date_added_raw’ is the Python format, whereas ‘date_added’ is a human-readable format. I’m aware it’s probably best to just store this data in raw format in the database, and then make it human-readable in the template or within app.py, thus eliminating the need for an extra field. This is how I would develop the app now, however, when I made the database this was very early on in the development process and my knowledge of Flask, MongoDB and databases in general is not what it is after making the project. I decided to keep the database schema in its current state in order to save time.
## 8. Deployment
The project is deployed on Heroku, available [here](https://dhamma-desertisland.herokuapp.com/). The deployment process was (thankfully) mostly headache free. All that had to be done was setting the environment variables (the same as the local vars with the exception of flask’s secret key).

Anyone wishing to run the app locally would just need to account for the following env variables:

FLASK_SECRET_KEY

MONGO_DBNAME

MONGO_URI
## 9. Credits
### 9.1. Images
#### Brand logo
https://www.canva.com/media/MACy4VY-bGc
#### The top parallax image on index.html
https://www.rollingstone.com/wp-content/uploads/2018/11/jimi-hendrix-performing-in-1969.jpg?crop=900:600&width=440
#### The bottom parallax image on index.html
https://image.redbull.com/rbcom/010/2015-09-10/1331746937069_2/0100/0/1/dj-nu-marks-gets-his-toys-out.jpg
### Acknowledgements
I received inspiration for this project mainly from Reddit. The design of the sort dropdown on tracks.html especially was inspired by Reddit’s design https://www.reddit.com/
#### Code Acknowledgements
Other developer’s code that I have reused is indicated within the code itself by comments.



