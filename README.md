#SuperStyler

SuperStyler is an add-on for [Anki](http://ankisrs.net/) which allows you to edit a stylesheets from the desktop client while previewing the changes on multiple other devices at the same time.

[Here is a YouTube video](http://www.youtube.com/watch?v=9-nN6KMO3Cw) demonstrating the add-on.

---
## Purpose
This add-on was created in response to the frustration of creating suitable stylesheets for my mobile devices; making small changes, syncing the deck on both ends, and then realising the changes weren't what you needed, is nettlesome. After doing it a hundred times, this add-on mysteriously materialized for the good of compulsive stylesheetists everywhere. It also helps to create better cross-platform stylesheets for those who intend to widely distribute their decks.

Template editing is not (yet!) supported. CSS only. Tested on AnkiDroid, AnkiWeb with FireFox, and the desktop client on Linux and Windows.

---

## How to use
### Prepare
Your collection needs to be prepared before using this plugin. This is mainly done to avoid having to do a full sync every time you use the plugin. Preparing the collection will create a card type inside each of your note types and trigger a full sync. If you create a new note type, the prepare screen will prompt you to prepare again (because the new note type doesn't have the special card type yet).
![Prepare](https://raw.github.com/ntsp/SuperStyler/master/docs/image/prepare.png "Prepare collection")  

### Start
The main screen lists your notes and all of their card types. You are shown notes instead of decks since the notes are the objects that contain the stylesheets. Editing a note's stylesheet affects all cards.
![Main](https://raw.github.com/ntsp/SuperStyler/master/docs/image/mainscreen.png "Main screen")  

To begin begin editing, decide which card type to use as your base template and click the "Start" link next to it. The card's template will be copied over to the SuperStyler card (so your original is untouched). 
![Opened](https://raw.github.com/ntsp/SuperStyler/master/docs/image/open.png "SuperStyler server open")  

This will also create a new dynamic deck which contains the new SuperStyler cards. This is the deck you must open to preview stylesheet changes when editing. The note type you are editing is appended to the name of the dynamic deck.
![Dyn](https://raw.github.com/ntsp/SuperStyler/master/docs/image/dyndeck.png "SuperStyler dynamic deck")  

This deck can be opened on any device to view changes as you make them. Of course, you need to synchronize your collection to make this deck available everywhere. Don't forget to sync!

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
