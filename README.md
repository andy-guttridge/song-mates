# Song Mates

[Link to deployed site](https://songmates.herokuapp.com/)

## Purpose

Thanks to modern technology, musicians can make great quality recordings at home. There's never been a better time for musicians to be able to express themselves via the 
medium of digital recording. Great music is often the result of collaboration, and while audio technology enables musicians to work with each other remotely, how do you find people to collaborate with?
 
The purpose of Song Mates is to provide a platform for musicians who want to write, perform and record material to find like minded people to collaborate with, whether that be for a song or an album. It was designed as a 'mobile first' web app from the ground up.

SongMates enables un-authenticated users to:

- Browse and search profiles of other users.
- Register with SongMates.

Authenticated users are able to:

- Create a user profile with an image, and 'About me' section, select up to five genres of music they are interested in from a preset list, and specify up to five instruments and skills to display on their profile.
- Send a 'collaboration request' to other users. This is similar to a connection request on LinkedIn or friend request on Facebook.
- View the profile of users who have sent them collaboration requests, and decide whether to accept or reject the request.
- Send user to user messages directly to other users who are collaborators. Note the term 'messages' refers to user to user messages throughout this documentation, unless otherwise stated (as opposed to Django user messages).
- View incoming and outgoing messages in an inbox/outbox format.
- Mark messages as deleted.
- 'Uncollaborate' with collaborators (this means these two users will no longer be able to message each other).

### CRUD functionality

SongMates features a persistent data store with full Create, Read, Update and Delete functionality.

- Create - authenticated users can create a user account, a profile, collaboration requests and messages (only to their approved collaborators).
- Read - users can view the profiles of other users, and authenticated users can read messages sent to them.
- Update - authenticated users can update their profiles and save the changes, and can approve collaboration requests sent to them (resulting in a new many-to-many relationship in the database).
- Delete - authenticated users can delete their profiles, delete pending collaboration requests (whether cancelling, rejecting or approving them) and delete messages sent by or to them (note that messages appear to be deleted to the user, but are not actually deleted from the database until both the sending and receiving users have marked them as deleted).

## Table of contents
- [Song Mates](#song-mates)
  * [Purpose](#purpose)
    + [CRUD functionality](#crud-functionality)
  * [Table of contents](#table-of-contents)
  * [User stories](#user-stories)
  * [Agile development methodology](#agile-development-methodology)
  * [Design](#design)
  * [Features](#features)
    + [Home page with hero image and text carousel](#home-page-with-hero-image-and-text-carousel)
    + [Navbar with 'info-icons' and collapsible 'burger' menu for mobile](#navbar-with--info-icons--and-collapsible--burger--menu-for-mobile)
    + [Edit profile page](#edit-profile-page)
    + [Find collaborators page](#find-collaborators-page)
    + [Search form](#search-form)
    + [Expandable user profiles with role based information and buttons](#expandable-user-profiles-with-role-based-information-and-buttons)
    + [Pending collaboration requests page with inbox and outbox](#pending-collaboration-requests-page-with-inbox-and-outbox)
    + [Messages page with inbox and outbox](#messages-page-with-inbox-and-outbox)
    + [Sign-in, sign-out and register pages](#sign-in--sign-out-and-register-pages)
    + [Custom Django messages](#custom-django-messages)
    + [Administrator panel](#administrator-panel)
    + [Fully responsive design](#fully-responsive-design)
    + [Future improvements and features](#future-improvements-and-features)
      - [Future improvements](#future-improvements)
      - [Future features](#future-features)
  * [Planning](#planning)
    + [Mockups](#mockups)
    + [Data models](#data-models)
  * [Frameworks, libraries and dependencies](#frameworks--libraries-and-dependencies)
    + [Django 3.2](#django-32)
    + [Psychopg 2](#psychopg-2)
    + [Gunicorn](#gunicorn)
    + [dj-database-url](#dj-database-url)
    + [Django-allauth](#django-allauth)
    + [Cloudinary and django-cloudinary-storage](#cloudinary-and-django-cloudinary-storage)
    + [Crispy Forms](#crispy-forms)
    + [Crispy Bootstrap 5](#crispy-bootstrap-5)
    + [Bootstrap 5](#bootstrap-5)
  * [Testing](#testing)
    + [Manual testing](#manual-testing)
    + [Automated tests](#automated-tests)
    + [Validator testing](#validator-testing)
      - [W3C HTML validator](#w3c-html-validator)
      - [W3C CSS Validator](#w3c-css-validator)
      - [JSHint JavaScript validator](#jshint-javascript-validator)
      - [Python validation](#python-validation)
    + [Lighthouse testing](#lighthouse-testing)
    + [Resolved bugs](#resolved-bugs)
    + [Unresolved bugs](#unresolved-bugs)
  * [Deployment](#deployment)
  * [Credits](#credits)
    + [Code](#code)
    + [Content](#content)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## User stories

Having conceived the basic idea for the site, themes and epics were documented in a spreadsheet (see link below). 
The themes and epics were:

**Theme: Account management**

*Epics: register account, sign-in, sign-out, delete account, user profile*

**Theme: User interaction**

*Epics: user profile, manage connections, message connections*

**Theme: Site administration**

*Epics: manage users*

The epics were then further refined into user stories.

[Link to SongMates user stories spreadsheet](https://docs.google.com/spreadsheets/d/1lfMAhZfRnoHnkIVx8LW1cVvdgnDvWeyrtCgRz0_mvzA/edit?usp=sharing)

The task management app [Wrike](https://www.wrike.com/main/) was used to manage individual tasks required for implementing user stories and other general tasks. It is not possible to share a public link to the Wrike project, but this screenshot illustrates its use:

<p align="center">
    <img src="readme_media/wrike.png" width="300">
</p>

Individual user stories were categorised according to whether they had to be implemented to produce a Minimum Viable Product (MVP), with priority for development to be given to those that were part of the MVP specification. Note that some of the terminology in the user stories varies from final implementation, for example the final website refers to 'collaboration requests' and 'collaborators', whereas the user stories refer to 'connections'.

User acceptance criteria/manual tests for each user story were added to the spreadsheet as development commenced on each user story. User stories with a white background and no acceptance criteria/tests were not part of the MVP and not implemented.

Implementation deviated from some of the original user stories, in response to continual testing as development progressed:

- *'As a user I can be confident that my profile will only be visible to registered users so that my details can only be accessed by potential collaborators registered with the site.'*

    This user story was implemented, however in testing the site it became apparent that making profiles visible to non-authenticated users could serve to increase engagement and interest, leading to more registrations and a richer pool of potential collaborators. Implementation of this user story was  un-done, however a priority for future development would be giving users the option to hide their profiles from non-authenticated users.
- *As a user, I can see an option to cancel pending connection requests on profiles of users to whom I have sent a request so that I can change my mind if I no longer feel I might wish to collaorate with them.*

    This was implemented in a slightly different way. The user story suggests that a button to directly cancel an outgoing collaboration request should be visible on the relevant user profile, however during development it was felt that providing a button indicating both outgoing and incoming pending collaboration requests and linking to an overview of such requests would be more logical and user friendly.
- *As a user I can see a list of my current connections and access their profiles so that I can evaluate their usefulness.*

    It was originally envisaged that this user story would be implemented with a separate navbar link to a list of current collaborators, however during development it was realised that incorporating a simple checkbox into the search form to allow users to display only their current collaborators and further narrow the search if desired would simplify the user experience and reduce site complexity.
- *As a user I can send emails to my connections so that I can facilitate collaboration with them.*

    While this user story was included to provide an easy-to-implement way for users to communicate with each other to achieve a MVP, it was always felt that a user-to-user messaging system would be a better way to facilitate communication between users. This was not included in the spec for a MVP due to concerns around development time. The email functionality was implemented by displaying an email link on the profiles of approved collaborators, but as successful implementation of user stories was proceeding more quickly than anticipated, this was replaced with a messaging system, exceeding the original MVP spec.

## Agile development methodology

GitHub issues, milestones and projects were used to document and track an agile development approach.
An issue was created for each user story. These were labelled as 'MVP' if they were part of the MVP spec. All user stories were then added to a 'Product Backlog' milestone  ([link to Product Backlog with remaining user stories that were not completed](https://github.com/andy-guttridge/song-mates/milestone/1)).

Development was divided into iterations with a timebox of three working days, each with a total value of 16 story points (although the duration in calendar days was variable, due to fitting the three working days around work and other commitments). A milestone and a GitHub project board were created for each iteration, and user stories moved from the Product Backlog and into the iteration. They were labelled as 'must have', 'could have' or 'should have' goals for the iteration, and assigned story point values. Story points for 'must have' user stories never exceeded 9 (60%).

A project Kanban board was used to track progress, with user stories moved between 'Todo', 'In Progress' and 'Done' columns as appropriate. For example, the iteration 3 project board was captured near the start, mid-way through the iteration and at the end:

<p align="center">
    <img src="readme_media/iteration_3_kanban_i.png" width="400">
    <img src="readme_media/iteration_3_kanban_ii.png" width="400">
    <img src="readme_media/iteration_3_kanban_iii.png" width="400">
</p>

The project boards in their final form can be accessed [via this link](https://github.com/andy-guttridge/song-mates/projects?query=is%3Aopen).
There are no project boards for iterations 4 and 6, because they were 'special' three working day iterations dedicated to design/styling work and testing/bug fixing, as opposed to implementing user stories. All the MVP user stories had been successfully implemented by the end of iteration 3.

There were some user stories which were automatically implemented as a consequence of other work (e.g. implementing admin panels for the data models) or by virtue of Django's built in features. These were documented with a special 'mop-up' milestone ([link](https://github.com/andy-guttridge/song-mates/milestone/6)) and closed.

One challenge was that there was considerable uncertainty as to how many story points to allocate to each task. For this reason, the first iteration had tasks equating to more than 16 total, although care was still taken to ensure the number of 'must haves' did not exceed 9 story points. As work progressed, it became apparent that story points had been overestimated for some tasks, with iteration 2 completed ahead of schedule. Iteration 3 was then opened early.

Note that one user story was left off the iteration 3 board in error, but was planned for and completed during that iteration. It was later added to the 'done' column for that iteration to ensure it was documented.

## Design
Research indicated that yellow is a colour traditionally associated with creativity, so a bright yellow was chosen as the basis for the design of the site. A very dark grey (almost black) was chosen as a background to provide a contrast with the yellow. A logo was designed using the Monoton font and an image of a vinyl record for the letter O. Monoton was chosen for the logo and main headings, as the lines in the letters are evocative of the grooves in a record. Rubik Mono One and Rubik were chosen for sub-headings and main text respectively, to provide a contrast to Monoton and ensure legibility at smaller font sizes.

[Adobe color wheel](https://color.adobe.com/) was used to find some contrasting colours for headings and buttons. A hero image of a vinyl record with a yellow label was chosen for the home page. The body of the record has a red colour - this colour was sampled using the Digital Colour Meter in Mac OS, and pasted into Adobe Color Wheel to find a number of contrasting colours. The original red and the colours derived from this were used for the alternating colours of the user profile 'cards' in the 'find collaborators' page, but were given an alpha value of 0.2 in order to blend them in against the dark background.'

The full colour palette is:

`#141414` - main background colour
`#fff3e9` - light background colour used for modals, form fields and tables
`rgba(43, 49, 54, 0.3)` - lighter semi-transparent grey used for the profile 'card' body
`#fef921` - the yellow used for the logo, headings, alerts etc
`rgba(178,56,64,0.2)` - alternating colour used for profile 'card' header and bottom
`rgba(37,129,179,0.2)` - alternating colour used for profile 'card' header and bottom
`rgba(11, 102, 33, 0.2)` - alternating colour used for profile 'card' header and bottom
`rgba(186, 50, 191, 0.2)` - alternating colour used for profile 'card' header and bottom
`#e8e1e8` - used for the bulk of the text against the dark background
`#262526`- dark text colour used against the light background of modals and tables
`#ccebff`- light blue text colour used for some headings

## Features

### Home page with hero image and text carousel

<p align="center">
    <img src="readme_media/hero3.png" width="200">
    <img src="readme_media/hero2.png" width="200">
    <img src="readme_media/hero1.png" width="200">
</p>

An eye catching hero image and three paragraphs of descriptive text, each displayed in turn in a carousel.

### Navbar with 'info-icons' and collapsible 'burger' menu for mobile

<p align="center">
    <img src="readme_media/burger1.png" width="300">
    <img src="readme_media/burger2.png" width="300">
</p>

The SongMates navbar features a collapsibe 'burger' menu for mobile users (although it expands to a full horizontal navbar on wider screens).
The navbar includes two 'info-icons', which show:
  - The number of user messages in the user's inbox (incoming only)
  - The number of pending collaboration requests for the user (incoming and outgoing)

The envelope icon links to the user's message inbox and outbox, while the 'collaborator' icon links to the user's pending collaboration requests inbox and outbox.

### Edit profile page

<p align="center">
    <img src="readme_media/edit_profile1.png" width="200">
    <img src="readme_media/edit_profile2.png" width="200">
    <img src="readme_media/edit_profile3.png" width="200">
    <img src="readme_media/edit_profile4.png" width="200">
</p>

The 'edit-profile' page ('Me' in the navbar) features an 'update profile' form and a 'delete account' form.
Users who have not yet filled out any of their profile are redirected to this page when they first login if they choose 'find collaborators', to encourage them to provide some details.

The update profile form enables the user to update their profile with:

- Am  About Me 'biography' of up to 500 characters. This is where the user can describe their musical interests and goals.
- An image.
- A selection of up to five musical genres from pre-populated lists.
- Up to five free text 'instruments or skills' fields of up to 30 characters

The form is validated so that if something goes wrong with the image upload, the user is prompted to consider whether they have uploaded a non-image file (see custom user messages below).
The form has 'revert' and 'submit' buttons. The revert button reloads the form with the previous data, while submit commits the form to the database.

At the bottom of the edit-profile is the delete account form, enabling the user to close their account. Selecting the button opens a modal dialog, giving the user the choice to dismiss the modal or confirm the deletion.

In the event the user confirms the deletion, their profile is deleted from the database and their user account made inactive (in line with Django best practice which recommends not deleting user accounts in order not to cause broken references within database tables).

### Find collaborators page
<p align="center">
    <img src="readme_media/find_collabs.png" width="200">
    <img src="readme_media/find_collabs3.png" width="200">
    <img src="readme_media/find_collabs2.png" width="200">
</p>

The 'find collaborators' page enables browsing of user profiles. Unregistered users are encouraged to register. Those who are authenticated but who have not yet filled out any of their profile do not have their profiles displayed on this page, and are presented with a message to encourage them to fill it out.

### Search form
<p align="center">
    <img src="readme_media/search_form.png" width="200">
</p>
The find collaborators page includes a search form to enable users to find potential collaborators aligned to their own interests.
The 'show only my collaborators' checkbox lets the user filter the profiles to only those who are approved collaborators. This works in combination with the other search fields, so for example a user could find only their collaborators whose profiles include 'country'. The checkbox is hidden from un-authenticated users.
The genres drop-down allows the user to narrow the search down to those genres they are interested in.
The 'search profiles' field enables the user to perform a free text search on profile biographies and instruments/skills.

### Expandable user profiles with role based information and buttons
<p align="center">
    <img src="readme_media/profile1.png" width="200">
    <img src="readme_media/profile2.png" width="200">       
    <img src="readme_media/profile5.png" width="200">
    <img src="readme_media/profile6.png" width="200">
    <img src="readme_media/profile3.png" width="200">
    <img src="readme_media/profile4.png" width="200">
</p>

Profiles are displayed with a collapsible section which can be expanded by pressing the down arrow. This reveals the 'About me' biography and a number of possible buttons depending on the status of the user and their relationship to the other users.

- If the user is not authenticated, only the 'About me' section is revealed within the collapsible.
- If the authenticated user has an approved collaboration relationship with the other user, this is indicated with a blue collaborator icon next to the other user's name. A 'contact me' icon enables them to send a message to the other user, and an un-collaborate button enables them to end the collaboration. The send message button opens a modal dialog enabling a message to be sent directly from this page. Choosing to un-collaborate opens another modal, asking the user to dismiss or confirm the request.
- If the authenticated user has a pending collaboration request (incoming or outgoing), a 'pending collaboration request' button provides a visual indication and links directly to the collaboration requests page so that action can be taken.
- If the user is authenticated but does not currently have a collaborative relationship with the other user, a 'request to collaborate' button sends the other user a collaboration request.

### Pending collaboration requests page with inbox and outbox
<p align="center">
    <img src="readme_media/collabs1.png" width="200">
    <img src="readme_media/collabs2.png" width="200">
    <img src="readme_media/collabs3.png" width="200">
</p>

The 'pending collaboration requests' page enables the authenticated user to see an overview of incoming and outgoing collaboration requests. They can view the profile of the other user to enable them to decide whether this looks like a worthwhile collaborator by clicking on their name in the 'from' column.

For incoming collaboration requests, the user can decide whether to accept or reject the collaboration request. Selecting reject opens a modal dialog to ask the user to confirm the rejection.

For outgoing collaboration requests, the user can cancel the request.

### Messages page with inbox and outbox
<p align="center">
    <img src="readme_media/messages1.png" width="200">
    <img src="readme_media/messages2.png" width="200">
    <img src="readme_media/messages3.png" width="200">
</p>

Similar to the collaboration requests page, the 'messages' page provides users with an overview of incoming and outgoing messages. They can view users' profiles by clicking on the name in the 'from' column, and can view messages in a modal by selecting the subject of the message in the 'subject' column. For incoming messages, they can reply directly from the modal.

A delete button enables the user to delete messages, after confirming the action in a modal dialog. If the user confirms deletion, the message will no longer be visible to them, but will only be deleted from the database when both the sending and receiving users have marked it as deleted. This is to prevent messages disappearing for one user before they have chosen to delete it.

### Sign-in, sign-out and register pages
<p align="center">
    <img src="readme_media/sign_in.png" width="200">
    <img src="readme_media/sign_out.png" width="200">
    <img src="readme_media/register.png" width="200">
</p>

Sign-in, sign-out and register pages are customised to match the styling of the site.

### Custom Django messages
<p align="center">
    <img src="readme_media/custom_msg1.png" width="200">
    <img src="readme_media/custom_msg4.png" width="200">
    <img src="readme_media/custom_msg3.png" width="200">
    <img src="readme_media/custom_msg2.png" width="200">
</p>

In addition to the standard Django user messages confirming successful sign-in and sign-out, the site features four additional custom messages to give the user feedback on some possible issues:

- The user could attempt to message another user with whom they were a collaborator from the messages inbox, but the previous collaborator has now deleted their profile.
- The user could attempt to message another user with whom they were a collaborator from the messages inbox, but the previous collaborator has now ended the collaboration. In this event, the message will not be sent.
- The user is provided with feedback if a profile search returns no results.
- The user is provided with feedback if something goes wrong with the edit profile form submission. While not the only possible issue, a typical cause of an error would be attempting to upload a non-image file, because most of the fields are straighforward text or multiple choice fields. The message includes a prompt to reflect this.

### Administrator panel
<p align="center">
    <img src="readme_media/admin1.png" width="200">
    <img src="readme_media/admin2.png" width="200">
    <img src="readme_media/admin3.png" width="200">
    <img src="readme_media/admin4.png" width="200">
    <img src="readme_media/admin5.png" width="200">
    <img src="readme_media/admin6.png" width="200">
</p>

The site includes an administrator panel only accessible to users with admin or super-user permissions. This enables:
- User accounts to be created.
- User accounts to be permanently deleted.
- Inactive user accounts to be reactivated.
- User details to be amended.
- Profiles to be created.
- Profiles to be deleted.
- Profiles to be amended, including upload of new images.
- Collaboration requests to be created and deleted.
- User to user messages to be created and deleted. This means site administrators can message any user, even if they are not collaborators.
- Only superusers are able to change the permission levels for other users.

The SongMates admin site is accessed via (https://songmates.herokuapp.com/admin/login/?next=/admin/)

### Fully responsive design
<p>
    <img src="readme_media/desktop.png" width="800">
</p>

While the site is very much 'mobile first', it scales well to larger devices.

### Future improvements and features

#### Future improvements

There are some parts of the site that would benefit from refactoring, which has not been possible due to time constraints.

- There is currently a lot of HTML duplicated between the `find_collabs.html` and `single_profile.html` templates. These could be refactored into a single template, but this would require passing in additional data and adding conditional statements to the template to determine whether it should render as a single profile or multiple profiles (e.g. this would influence whether or not to render search features, the correct heading for the page etc).
- The code to process the search form in the `SearchProfiles` class in `views.py` is overly complex. This would benefit from refactoring as a priority.
- Currently multiple modal dialogs are created within the DOM to faciliate user interaction relating to specific profiles, collaboration requests and messages. These require unique elements and attributes such as forms and buttons, to ensure actions are performed on the correct database objects, that the correct messages are displayed and so on. It would be more efficient to render one modal and populate it for the appropriate action.

#### Future features

A significant number of potential enhancements for the future have been identified.

- Ability for users to rate or rank their collaborators, and have this displayed on profiles for authenticated users.
- Ability to send a message with a collaboration request.
- Ability to send a message when choosing to 'un-collaborate' with a user.
- Organisation of user to user messages into 'threads'.
- Abiity to distinguish between 'read' and 'unread' messages so that only unread messages are counted in the navbar, and the ability for the user to mark messages as read or unread.
- Group messages.
- Live chat.
- Live feedback on character limit on forms.
- Ability to live preview, center and zoom images within the update profile form.
- An option for users to hide their profile from unauthenticated users.
- Enable users to embed SoundCloud and Youtube clips in their profiles.
- Ability for users to report other users to the site admin.
- Mechanism for users to easily contact the site admin.
- 'Masonry' layout of user profile 'cards'.
- A feature to explicitly mark accounts as 'hidden', e.g. for admin accounts, although this can be achieved now by maintaining a completely empty profile.
- Ability to login with social media accounts.
- Enhanced account management functionality, e.g. ability for users to change username, change password, change email account and add email account verifications without having to get in touch with the site admin (currently unused allauth templates have not been removed, with a view to implementing these features in future).
- Automatic reduction of profile image size on upload.
- Automatic deletion of images from cloudinary storage when users change their profile images or delete their profiles.

## Planning

### Mockups

Wireframes were produced, mapping the 'user journey' through the site. These were based on a mobile view of the site, as SongMates is very much a mobile first web app.

<p align="center">
    <img src="readme_media/wire_frames.png" width="800">
</p>
<p align="center">
    <a href="readme_media/wire_frames.pdf" target="_rel">Link to full size wireframes</a>
</p>

The wireframes proved invaluable as a guideline for the implementation phase. In response to the continual testing of the site throughout the development process, some implementation details diverged from the original wireframe plan:

- Users are directed back to the home page when they login.
- The number of instruments/skills fields available on user profiles was reduced from ten to five. The data model was initially created with five fields to keep things manageable during the initial development phase, however testing suggested that more than five could become overwhelming and that five should be sufficient for most users. The corresponding user story was revised accordingly.
- As noted in the user stories section above, it was decided during development to replace the separate 'My collaborators' view with a checkbox on the profile search form, as a way of reducing site complexity and enhancing the user experience.
- The separate 'write new message' and read message views were replaced by modal dialogs, again to reduce site complexity from the user's perspective.
- The button to cancel a collaboration request from an individual user profile was replaced with the 'Pending collaboration request' button mentioned in the user stories section. This led to the creation of a whole new 'collaboration requests' view, which was deemed to be a more comprehensive and useful implementation.
- Account management features such as changing user name, email address etc were not implemented due to time constraints.

### Data models

Data models were originally planned using a spreadsheet prior to implementation, however are presented here in diagram form for clarity. Note that the 'join table' was not created in the Django `models.py` file, but is shown here as a simplified representation of how Django handles many-to-many relationships 'behind the scenes'.

SongMates uses the standard Django user model, although not all the fields are utilised.

Custom models for SongMates are:

- Profile - represents the user's profile. This includes the biog (used for the 'About me' information), the genres, the instruments/skills fields, and an image. The profile model also records collaboration relationships between users, using a many-to-many field.
- CollabRequest - this is a simple model representing collaboration requests sent from one user to another. When a CollabRequest instance is approved or rejected by the receiver, or cancelled by the sender, it is deleted. If approved, this results in a new many-to-many relationship in the Profile table.
- Message - this represents user-to-user messages. This model includes `from_deleted` and `to_deleted` fields, which are used to separately record when the sender and receiver have 'deleted' the message. This enables the message to be hidden from a user when they have marked it as deleted, but for it not to be actually deleted from the database until both users have 'deleted' it.

<p align="center">
    <img src="readme_media/songmates_db_schema.png" width="400">
</p>
<p align="center">
    <a href="readme_media/songmates_db_schema.png" target="_rel">Link to full size DB schema</a>
</p>

## Frameworks, libraries and dependencies

### Django 3.2
[Python web framework](https://www.djangoproject.com/)

### Psychopg 2
[Python PostgreSQL adapater](https://pypi.org/project/psycopg2/)

### Gunicorn
[Python WSGI HTTP server](https://gunicorn.org/)

### dj-database-url
[Django utility to create an environment variable to configure the Django application]((https://pypi.org/project/dj-database-url/))

### Django-allauth
[User account management django application suite](https://django-allauth.readthedocs.io/en/latest/overview.html)

### Cloudinary and django-cloudinary-storage
Libraries to enable storage of static files and media in Cloudinary

https://cloudinary.com/
https://pypi.org/project/django-cloudinary-storage/

### Crispy Forms
[Django app to simplify form rendering](https://django-crispy-forms.readthedocs.io/en/latest/)

### Crispy Bootstrap 5
[Bootstrap 5 templates for Crispy Forms](https://pypi.org/project/crispy-bootstrap5/)

### Bootstrap 5
[Front end CSS and JavaScript library](https://getbootstrap.com/)

## Testing

### Manual testing

Manual tests were devised for each user story, once it was decided a particular story would be implemented. These are documented on the [SongMates user stories spreadsheet](https://docs.google.com/spreadsheets/d/1lfMAhZfRnoHnkIVx8LW1cVvdgnDvWeyrtCgRz0_mvzA/edit?usp=sharing).

All manual tests were found to pass, once the bugs noted above had been fixed.

In addition, the site was subject to continual user testing throughout the development process. This resulted in a number of enhancements to the user experience, which are documented in the user stories and planning sections above.

### Automated tests

A number of unit tests were written to test key interactions between the views and the database models. These can be found in the `tests.py` file in the `songmates_main` directory. These were:

- Test new profile is created when account is registered - passed
- Test profile is deleted when request received from user - passed
- Test the user account becomes inactive when the user requests account deletion - passed
- Test a collaboration request is created correctly when requested by the sender - passed
- Test that when a collaboration request is approved, it results in a many to many relationship for the correct profiles and is then deleted - passed
- Test that when a collaboration request is rejected, no many to many relationship is created between the sending and receiving users and that it is deleted - passed
- Test that when a user decides to end a collaboration, the many to many relationship between the two profiles is correctly removed - passed
- Test that user to user messages are sent correctly when requested by the sender - passed
- Test that user to user messages are correctly marked as deleted when requested by one user, but only deleted when marked as deleted by both users - passed

### Validator testing

#### W3C HTML validator

Given the presence of Django template code in the HTML templates, the rendered HTML was copied from the Chrome browser by right clicking, selecting 'view page source' for each page of the site and then pasting directly into the HTML validator. The following issues were detected:
- Three HTML character codes which were not terminated with a `;`  in the navbar and the footer.
- An element with an opening `<button>` tag and closing `<a>` tag in `find_collabs.html`.
- The `onchange` attribute for the checkbox on the search form was incorrectly spelt `on-change`. This highlighted that this attribute was a 'hangover' from the development process and had been replaced by an event listener added to the element via JavaScript, so was removed altogether.
- The `rows` attribute used on the form in the send message modal in the `find_collabs.html` template had been mispelt.
- Duplicate `id` attributes were found for the modals and forms used to confirm deletion of a collaboration relationship, and for the `form` elements used to send a collaboration request in `find_collabs.html`.
- Modals were being rendered with `id` attributes referencing non-existent forms in `find_collabs.html`. This error was rectified by wrapping the modal code in an `if`...`endif` block within the HTML template, to check whether a modal would be required for that particular user profile.
- A similar issue with modals being rendered with `id` attributes referencing non-existent forms was also present in `messages.html`. This only affected outgoing messages, and was rectified by moving an `endif` to ensure that modals are only rendered if there is an associated form.
- Modals were being rendered inside tables in `collab_requests.html` and `messages.html`. This was fixed by moving the modals into a separate for loop within the HTML template.

The above errors were all rectified.

The validator also produced the following information about closing slashes on void elements  within the `find_collabs` and `edit_profile` templates. These are inserted into the HTML by Django or CrispyForms when the forms defined in `forms.py` are rendered, and since this is not regarded as an error, this was deemed satisfactory:

<img src="readme_media/trailing_slashes_1.png">
<img src="readme_media/trailing_slashes_2.png">

#### W3C CSS Validator
The custom CSS for the site passed through the W3C Jigsaw CSS validator with no issues
<img src="readme_media/css_validation.png">

#### JSHint JavaScript validator
The small amount of custom JavaScript code for the project was passed through the JSHint validator. This detected a number of missing semi-colons and a missing `let` keyword. These issues have been corrected, and the JavaScript now passes validation. Note that JSHint flags an issue with an undefined `bootstrap` variable, however this because JSHint does not have access to the Bootstrap CDN import defined within a `<script>` tag in the `base.html` template. The Google Chrome inspector confirms there are no JavaScript errors with the deployed site.

<img src="readme_media/js_hint.png">

#### Python validation
The PEP8 validator was down at the time this project was developed, therefore Python code was validated using the `pycodestyle` tool, which was installed to the IDE (GitPod). Issues with the custom Python code were fixed on an ongoing basis. All files which contain custom Python code have been verified to have no issues detectabe by `pycodestyle`:

- `songmates/settings.py`
- `songmates/urls.py`
- `songmates/wsgi.py`
- `songmates_main/admin.py`
- `songmate_main/apps.py`
- `songmates_main/forms.py`
- `songmates_main/functions.py`
- `songmates_main/genres.py`
- `songmates_main/models.py`
- `songmates_main/tests.py`
- `songmates_main/urls.py`
- `songmates_main/views.py`
- `songmates_main/templatetags/tags/py`

### Lighthouse testing

A number of issues were found via the Lighthouse report generated by the Google Chrome developer tools.

- The chevron buttons on each profile on the 'Find Collaborators' page did not have accessible names. This was corrected by adding an `aria-label` attribute to these buttons.
- Buttons with the `btn-danger` class were found to have insufficient contrast. This was corrected by making the red colour darker.
- The navbar 'burger' menu button for mobile was found to be too small to provide a suitable touch target. The size was increased.
- The SongMates logo in the navbar was found to be of insufficient resolution. The image was re-exported at double the resolution, and resized back down to 300px width in CSS.

After addresing the above issues, all pages score 100 for accessibility and best practices, and at least 90 for SEO.
Performance scores for some pages are disappointing and seem to be largely related to image loading. The hero image on the homepage was converted from `jpg` to `webp` format, but this made little difference. Lighthouse found the profile images to be inappropriately large - this is difficult to control because they are uploaded by users. A future improvement could be to automatically resize them on upload. A further issue may simply be that the site is hosted using free hosting from Heroku, which is not as fast as a 'paid for' web hosting package.

<img src="readme_media/lighthouse_home.png">
<img src="readme_media/lighthouse_findcollabs.png">
<img src="readme_media/collabrequests.png">
<img src="readme_media/lighthouse_messages.png">
<img src="readme_media/lighthouse_editprofile.png">
<img src="readme_media/lighthouse_signin.png">
<img src="readme_media/lighthouse_signout.png">
<img src="readme_media/lighthouse_signup.png">

### Resolved bugs
- Initially, allauth configuration was set to require the user to login with an email address and for email verification to be required. However, this resulted in a Django 'connection refused' error. This was caused by the fact no email server was availabe to send verification request emails. Settings were changed so that account login is by username rather than email address. 
- Testing of the update profile form showed that profile pictures were not uploading to cloudinary. This was rectifed by adding the `enctype="multipart/form-data"` attribute to the form element.
- While testing the search feature, it was realised that if the user did not select any genres, no profiles would be returned. This was fixed by adding a simple conditional statement to ensure that profiles are not filtered by genre if no genres are selected.
- During testing, it was found that the 'Show my collaborators only' checkbox on the search form was overriding other search results. For example, if a genre of 'Hip-Hop' was selected in the genres menu and the checkbox to show collaborators only was selected, collaborators would show in the search results even if none of them were matched with the 'Hip-Hop' selection. The correct outcome in this case would be no search results. This was bug was caused by an incorrect boolean condition in an if statement and easily fixed.
- Non-authenticated users using the search function resulted in a server error. This was caused by an attempt to reference the user's profile in the `SearchProfile` view. This was fixed by moving the offending code inside a conditional statement checking for an authenticated user.
- Testing uploading an invalid  profile image resulted in an error. This was fixed by adding a try/except block to the view code. A Django message is displayed within the except block in the event of an error.
- The modal dialog for sending a user to user message in the Find Collaborators page was always displaying the name of the first user profile in the list, no matter which user selected to send a message to. This was because Bootstrap modals must have a unique `id` attribute. All the modals had been given the same `id` within the `for` loop that renders profiles. This was also the case for the corresponding `data-bs-modal` attribute of the buttons used to open the modal from each profile. This was fixed by appending the primary key for each user to the modal `id` and button `data-bs-modal` attribute.
- The modal dialogs for rejecting incoming or cancelling outgoing collaboration requests were targetting the incorrect users, meaning that when there were multiple collaboration requests for one user, the incorrect one would be deleted from the database. This was for a similar reason as the above issue with user messages, and was fixed by moving the modals within the for loop and applying unique `id` attributes to the forms and buttons for each collaboration request.
- The 'Show only my collaborators' checkbox on the search form was always returning no results, even when the user did have collaborators. This was fixed by additional checks for empty querysets and whether the checkbox has been selected in the `SearchProfile` class in `views.py`.

### Unresolved bugs
The following bugs were not resolved due to time constraints:
- If user A sends a collaboration request to user B, user B then opens their collaboration requests inbox, and user A then cancels the collaboration request, user B can still accept the collaboration request if they happen not to refresh their browser. This was not deemed a major bug, as the timing and sequence of events would have to be very specific for this to occur, and users can still choose to un-collaborate at any time.
- Entering a search term and selecting a genre in the search form returns all profiles matching the search term if there are no profiles matching the genre. Intended behaviour is that no results would be returned in this circumstance.

## Deployment

SongMates is deployed to Heroku. 
To duplicate deployment to Heroku, follow these steps:

- Fork or clone this repository in GitHub.
- You will need a Cloudinary account to host user images and static files.
- Login to Cloudinary.
- Select the 'dashboard' option.
- Copy the value of the 'API Environment variable' from the part starting `cloudinary://` to the end. You may need to select the eye icon to view the full environment variable. Paste this value somewhere for safe keeping as you will need it shortly (but destroy after deployment).
- Log in to Heroku.
- Select 'Create new app' from the 'New' menu at the top right.
- Enter a name for the app and select the appropriate region.
- Select 'Create app'.
- Select 'Settings' from the menu at the top.
- Select the 'resources' tab. 
- Search for 'Heroku Postgres' in 'Add-ons' search bar.
- Choose the 'Hobby Dev - free' plan.
- When the Heroku Postgres database has been added, select the instance of the database by clicking on 'Heroku Postgres' (to the right of this it will say 'Attached as database').
- Select the 'settings' option at the top (this opens the settings for the database as opposed to the app).
- Select the 'view credentials' button to the right.
- Copy and paste the value given for the database URI somewhere for use in a moment.
- Close the database page (which should have opened in a new tab) and return to your Heroku app.
- Select the 'settings' tab.
- Locate the 'reveal config vars' link and select.
- Enter the following config var names and values:
    - `CLOUDINARY_URL`: *your cloudinary URL as obtained above*
    - `DATABASE_URL`: *your Heroku postgres database URI as obtained above*
    - `PORT`: `8000`
    - `SECRET_KEY`: *your secret key*
- Select the 'Deploy' tab at the top.
- Select 'GitHub' and confirm you wish to deploy using GitHub. You may be asked to enter your GitHub password.
- Find the 'Connect to GitHub' section and use the search box to locate your repo.
- Select 'Connect' when found.
- Optionally choose the main branch under 'Automatic Deploys' and select 'Enable Automatic Deploys' if you wish your deployed site to be automatically redeployed every time you push changes to GitHub.
- Find the 'Manual Deploy' section, choose 'main' as the branch to deploy and select 'Deploy Branch'.
- Your site will shortly be deployed and you will be given a link to the deployed site when the process is complete.

## Credits

### Code

- The steps to connect to a Heroku Postgres database and deploy were adapted from the Code Institute 'I think therefore I blog' tutorial. This includes defining `DATABASE_URL` and `SECRET_KEY` environment variables in an `env.py` file in the local environment and adding corresponding config variables in the Heroku dashboard, using dj_database_url to create a URL from the Heroku database URL in `settings.py`, updating `ALLOWED_HOSTS` in `settings.py` with the deployed Heroku URL and adding the templates path to a `TEMPLATES_DIR` variable in `settings.py`.
- This [stackoverflow article](https://stackoverflow.com/questions/68810221/login-required-decorator-gives-object-has-no-attribute-user-error) was referenced to understand how to use the 'login-required' decorator with a class based view.
- The approach to deleting a user account (actually making the account inactive) in response to a button was adapted from [this stackoverflow article](https://stackoverflow.com/questions/38047408/how-to-allow-user-to-delete-account-in-django-allauth).
- The Bootstrap 5 documentation was extensively referenced for guidance on implementing navbars and modal dialogs.
- The approach to using a crispy form Div helper class to layout form elements next to each other was based on [this stackoverflow article](https://stackoverflow.com/questions/23021746/get-two-fields-inline-in-django-crispy-forms-but-not-others-horizontal).
- The approach to using the crispy forms HTML help class to display an image from the database model in a form was based on (https://stackoverflow.com/questions/21076248/imagefield-preview-in-crispy-forms-layout).
- The approach to using a custom template tag to pass data to the base HTML template was adapated from (https://stackoverflow.com/questions/21062560/django-variable-in-base-html) and then refined with reference to the official Django documentation.
- This [stack overflow question](https://stackoverflow.com/questions/53672002/how-to-call-conditional-statements-on-template-tags-with-no-arguments-django) was referenced for details on how to convert a custom template tag to a variable in Django template.
- The technique for displaying values of a many to many field in the admin panel was adapted from [stack overflow question](https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django).
- This [stack overflow question](https://stackoverflow.com/questions/21666963/django-forms-multiplechoicefield-only-selects-one-value) was referenced to discover how to access a list of values returned by a multiple choice Django form element.
- The technique of using an `initial` argument when initialising a form to set a form input's initial value is from (https://stackoverflow.com/questions/604266/django-set-default-form-values).
- Using the `_in` lookup parameter to find out if the value of a field exists within a list was adapated from (https://stackoverflow.com/questions/70703168/check-if-each-value-within-list-is-present-in-the-given-django-model-table-in-a).
- The syntax for searching on a property of a foreign key object is adapated from (https://stackoverflow.com/questions/35012942/related-field-got-invalid-lookup-icontains).
- The technique for overriding the save method of a Django model class in order to compute the value of a field based on the values of other fields is adapted from(https://stackoverflow.com/questions/22157437/model-field-based-on-other-fields).
- The technique for identifying the currently active link in the navbar and conditionally applying classes is from (https://stackoverflow.com/questions/46617375/how-do-i-show-an-active-link-in-a-django-navigation-bar-dropdown-list).
- Using the JavaScript `setTimeout()` function to automatically dismiss Django messages was adapted from the Code Institute Django Blog walkthrough.
- This [Stack Overflow](https://stackoverflow.com/questions/35777410/multi-modals-bootstrap-in-for-loop-django) question was referenced to fix the issue with modals opening for the incorrect user when sending a message from the Find Collaborators page.
- This [Stack Overflow](https://stackoverflow.com/questions/19024218/bootstrap-3-collapse-change-chevron-icon-on-click) question was referenced for a solution to changing the icon displayed depending on the state of a Bootstrap collapse item.
- This [Stack Overflow](https://stackoverflow.com/questions/36940384/how-do-i-setup-a-unit-test-user-for-django-app-the-unit-test-cant-login) article was referenced to understand how to create a test user for Django unit tests.
- The technique to conditionally add a local database for unit tests within the `settings.py` file is from [this Stack Overflow artice](https://stackoverflow.com/questions/4650509/different-db-for-testing-in-django).
- The technique to ensure the latest state of the user is loaded from the database within a unit test is from [Stack Overflow](https://stackoverflow.com/questions/64741329/why-is-my-test-function-not-activating-the-user).
- This [Stack Overflow](https://stackoverflow.com/questions/910169/resize-fields-in-django-admin) article was referenced to understand how to resize fields in the Django admin panel forms.

In addition to the specific articles and materials referenced above, the official Django and Bootstrap documentation was extensively referenced throughout the project.

### Content

- Font Awesome icons
    - [Burger menu icon](https://fontawesome.com/icons/bars?s=solid&f=classic)
    - [Collaborator icon](https://fontawesome.com/icons/user?s=solid&f=classic)
    - [Information icon](https://fontawesome.com/icons/circle-info?s=solid&f=classic)
    - [User pen icon](https://fontawesome.com/icons/user-pen?s=solid&f=classic)
    - [Envelope icon](https://fontawesome.com/icons/envelope)
    - [Down chevron icon](https://fontawesome.com/icons/chevron-down?s=solid&f=classic)
    - [Up chevron icon](https://fontawesome.com/icons/chevron-up?s=solid&f=classic)
- Google fonts
    - [Monoton](https://fonts.google.com/specimen/Monoton?query=Monoton)
    - [Rubik Mono One](https://fonts.google.com/specimen/Rubik+Mono+One?query=rubik+mono)
    - [Rubik](https://fonts.google.com/specimen/Rubik?query=rubik)
- Placeholder profile image by WandererCreative and downloaded from [Pixabay](https://pixabay.com/images/id-973460/)
- Vinyl record image used in the logo by Paul Brennan and downloade from [Pixabay](https://pixabay.com/photos/phonograph-record-vinyl-audio-sound-3148686/)
- Vinyl record image used for the favicon by Clker-Free-Vector-Images from [Pixabay](https://pixabay.com/vectors/record-album-retro-vintage-vinyl-312730/)
- Hero image of red vinyl record by Stas Knop and downloaded from [Pexels](https://www.pexels.com/photo/red-vinyl-record-3552948/)
- Profile images for test user accounts:
    - ElizaB's image is from [Freepik](https://www.freepik.es/vector-premium/dibujo-dibujos-animados-cantante_20243817.htm)
    - Luna's image is from [Pixabay](https://pixabay.com/photos/cat-tree-climb-kitten-domestic-cat-2902599/)
    - Trumpet_Mike's image is from [Pixabay](https://pixabay.com/photos/music-instrument-trumpet-metal-624421/)
    - Elvis' image is from [Pixabay](https://pixabay.com/photos/elvis-elvis-presley-musician-1269775/)
    - holy_grail_42's image is from [Pixabay](https://pixabay.com/photos/forest-girl-trees-fog-lantern-3833973/)
    - Lauren's image is from [Pixabay](https://pixabay.com/photos/announcer-audio-black-cassette-316586/)
    - Aki's image is from [Pixabay](https://pixabay.com/vectors/tree-art-trunk-artwork-cartoon-576823/)
    - Emma's image is from [Pixabay](https://pixabay.com/photos/guitar-musical-instrument-make-music-1585657/)
    - Frasse's image is from [Pixabay](https://pixabay.com/photos/sweden-beach-milky-way-stars-6834164/)
    - JoeB's image is from [Pixabay](https://pixabay.com/photos/zombie-makeup-halloween-horror-2262987/)
    - JoeC's image is from [Pixabay](https://pixabay.com/photos/ball-pit-toys-kids-fun-play-ball-2923853/)
    - Johnson's image is from [Pixabay](https://pixabay.com/photos/daisy-flower-heart-love-blossom-6304767/)