## This document discusses, technically, how you implemented your project
# and why you made the design decisions you did.
# Your design document should be at least several paragraphs in length.

# Whereas your documentation is meant to be a user’s manual,
# consider your design document your opportunity to give the staff a
# technical tour of your project underneath its hood.


3 database tables:
    users (login info, etc)
    posts (title, summary, typeOfWork, etc)
    messeges (sender_id, receiver_id, message_id, message)


Sections of this design document

    1. maps
    2. tables
    3. messaging
    4. error checking


1. Maps
    When coming up with my website, I wanted maps to be the primary method
    of finding peoples postings since if you are looking to help your neighbors,
    you will just isolate your search to your area.

    It was a bit tricky working with Google's MAPS API and services, but once
    it is working it works well. I used two of google's services:
    Maps JavaScript API and the Geocoding API

    The JavaScript provides the visual map with clickable markers. I integrated
    call-out windows on-click for the markers, each containing information about
    it's post.

    I used the Geocoding API to transform the user's input address into LAT & LNG
    coordinates. I did this so I could randomly offset the coordiantes slightly before placing
    the marker on the map. This was done so other people couldn't pin-point where
    you live from the marker.

2. Tables
    I used significant tables in 2 places. On the index page showing the list of posts
    and in the messages page to display messages to/from users.
    They are not too sophisticated, but they do have the functionality of sorting
    by clicking on headers.

3.  messaging
    For the messaging feature I created a SQL table that stored information about the
    post from which the message started, both users' id, message content, and a message_id

    The users have the option of writing the first message on the post page and then any follow
    on messages on the post page or in the messages page.

    On the post page, only users that are logged in can see the "Send Message" button.
    On the messages page, users can see all messages that they have written and have been
    written to them. They can also reply to any message in the table by pressing the "Reply"
    button and submitted the Modal form.

4. error checking
    Error checking is super important and makes a big difference on the useability of a website
    I did not get around to doing much of it, so users can quite easily break things by typing
    in wrong values. (but not SQL injections)


