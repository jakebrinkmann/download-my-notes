""" Main script to run """
import sys
from download_my_notes import MyNotes

def main(username, password, folder, search, directory):
    notes = MyNotes()
    notes.login(username, password)
    notes.search(folder, search)
    notes.save(directory)

if __name__ == "__main__":
    usernm = sys.argv[1]
    passwd = sys.argv[2]
    foldr = sys.argv[3]
    srch = sys.argv[4]
    dest = sys.argv[5]
    main(usernm, passwd, foldr, srch, dest)
