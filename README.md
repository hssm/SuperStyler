#SuperStyler

SuperStyler is an add-on for [Anki](http://ankisrs.net/) which allows you to edit stylesheets from the desktop client while previewing the changes on multiple other devices at the same time.

[Here is a YouTube video](http://www.youtube.com/watch?v=9-nN6KMO3Cw) demonstrating the add-on.

---
## Purpose
This add-on was created in response to the frustration of creating suitable stylesheets for my mobile devices; making small changes, syncing the deck on both ends, and then realising the changes weren't what you needed, is nettlesome. After doing it a hundred times, this add-on mysteriously materialized for the good of compulsive stylesheetists everywhere. It also helps to create better cross-platform stylesheets for those who intend to widely distribute their decks.

Template editing is not (yet!) supported. CSS only. Tested on AnkiDroid, AnkiWeb with FireFox, and the desktop client on Linux and Windows.

---

## How to use
### Prepare
Your collection needs to be prepared before using SuperStyler. This is done to avoid having to do a full sync every time you use SuperStyler. SuperStyler needs to create its own card types to ensure it doesn't mess up your real data, but Anki needs to do a full sync any time you add a new card type. It would be very inconvenient to have to full-sync every time you needed to use SuperStyler. Thus, preparing your collection will create empty card types in all of your note types, so you only do a full sync once. These card types will have empty templates, so no new cards are generated. **Do not edit those templates yourself in the card editor** (see [Cleanup](#cleanup)). If you create a new note type, the prepare screen will prompt you to prepare again (because the new note type doesn't have the special card type yet).

![Prepare](https://raw.github.com/ntsp/SuperStyler/master/docs/image/prepare.png "Prepare collection")  

### Main screen
The main screen lists your notes and all of their card types. You are shown notes instead of decks since the notes are the objects that contain the stylesheets. Editing a note's stylesheet affects all cards.

![Main](https://raw.github.com/ntsp/SuperStyler/master/docs/image/mainscreen.png "Main screen")  

To begin editing, decide which card type to use as your base template and click the "Start" link next to it. The card's template will be copied over to the SuperStyler card (so your original is untouched) and a server is opened in the background. 
![Opened](https://raw.github.com/ntsp/SuperStyler/master/docs/image/open.png "SuperStyler server open")  

**Note:** the main window shows you a warning that you must follow. SuperStyler creates brand new cards to freely modify for itself. These cards are in your collection and look identical to the base template you copied, so it's hard to tell them apart. If not removed, these cards may appear in your normal reviews as new cards. You *must* make use of the "[clear]" link shown on the SuperStyler main screen to remove any junk related to SuperStyler before reviewing normally again.

Click on the "[Open]" link to open the editor. This editor is linked to the server in the background.

![Editor](https://raw.github.com/ntsp/SuperStyler/master/docs/image/editor.png "SuperStyler editor")  

At this point, there will also be a new dynamic deck which contains the new SuperStyler cards that grab the styleshet from the abovementioned server. 

![Dyn](https://raw.github.com/ntsp/SuperStyler/master/docs/image/dyndeck.png "SuperStyler dynamic deck")  

This is the deck you must open to preview stylesheet changes when editing. The name of the dynamic deck will contain the note type's name at the end. This deck can be opened on any device to view changes as you make them. Of course, you need to synchronize your collection to make this deck available elsewhere. The server will remain open as long as Anki stays open, or until you click the "[clear]" link beside the note.

Once satisfied with your changes, **click the *save* button to save changes (TODO: save automatically like the original card editor)**.

### Cleanup
Cleanup is important!

---

## Developer notes

### Known issues
### TODOs
### Running the add-on from this directory

maindialog.ui needs to be compiled with pyuic4, but the output (maindialog.py) is already included in the project, so there's no need to do that unless you modify the .ui file.
