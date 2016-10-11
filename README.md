# Download my notes

Instead of using Evernote "web-clipper" or Dropbox on my mobile, I email
information to myself at a variation of my Gmail address.

For example, if my email address were ```someone@gmail.com```, I send my notes
to a Gmail alias such as ```some.one@gmail.com``` (_note_ addition of stop).

Goal: Every time this script is run, it will download these emails as HTML or
plain text, and create a file locally on my computer. Then, it will delete the
message from my inbox.

## Configuration

The script is configured using the **config.txt** file:

* **username**: your Gmail address or login id: ```user@gmail.com```
* **password**: associated password
* **folder**: which folder (aka label) to search ```[Gmail]/All Mail```
* **search**: how to find the notes, eg: ```To notes@place.com```
* **directory**: relative path to save the notes locally

## Usage

The app is setup to be called from the commandline as:

    python run.py config.txt

This default script is setup as such:

```python
from download_my_notes import MyNotes

notes = MyNotes() # Initialize the notes mailbox
notes.login(username, password) # Login to user's Gmail account
notes.search(folder, search) # Find emails in a folder by search query
notes.save(directory) # Output the email plaintext payload into files
```
