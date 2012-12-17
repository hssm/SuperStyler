#SuperStyler

SuperStyler is an add-on for [Anki](http://ankisrs.net/) which allows you to edit a note type's stylesheet from the desktop client while previewing the changes on multiple other devices at the same time.

[Here is a YouTube video](http://www.youtube.com/watch?v=9-nN6KMO3Cw) demonstrating the add-on.

---
## Purpose
This add-on was created in response to the frustration of creating suitable stylesheets for my mobile devices; making small changes, syncing the deck on both ends, and then realising the changes weren't what you needed, is nettlesome. After doing it a hundred times, this add-on mysteriously materialized for the good of compulsive stylesheetists everywhere. It also helps to create better cross-platform stylesheets for those who intend to widely distribute their decks.

Template editing is not (yet!) supported. CSS only.

---

## How to use
### Prepare
![Prepare](https://raw.github.com/ntsp/SuperStyler/master/docs/image/prepare.png "Prepare collection")  

### Start
![Main](https://raw.github.com/ntsp/SuperStyler/master/docs/image/mainscreen.png "Main screen")  

Click on a "Start" link to insert all the required data in your collection and open a server in the background.  
![Opened](https://raw.github.com/ntsp/SuperStyler/master/docs/image/open.png "SuperStyler server open")  

A dynamic deck is created to present cards of the new server-based SuperStyler card type.  
![Dyn](https://raw.github.com/ntsp/SuperStyler/master/docs/image/dyndeck.png "SuperStyler dynamic deck")  

This deck can be opened on any device to view changes as you make them. Of course, you need to synchronize your collection to make this deck available everywhere.

### Editor
![Editor](https://raw.github.com/ntsp/SuperStyler/master/docs/image/editor.png "SuperStyler editor")  

### Cleanup
Cleanup is important!

---

## Developer notes

### Known issues
### TODOs
### Running the add-on from this directory

maindialog.ui needs to be compiled with pyuic4, but the output (maindialog.py) is already included in the project, so there's no need to do that unless you modify the .ui file.
