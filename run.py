""" Main script to run """
import sys

from download_my_notes import MyNotes
from load_defaults import load_config_file

def main(username, password, folder, search, directory):
    notes = MyNotes()
    notes.login(username, password)
    notes.search(folder, search)
    notes.save(directory)

if __name__ == "__main__":
    config = sys.argv[1]
    defaults = load_config_file(config, 'Default', {})
    main(defaults['username'], defaults['password'], defaults['folder'],
         defaults['search'], defaults['directory'])
