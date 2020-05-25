import sys
from PyQt5.QtWidgets import QApplication, QWidget,QTableWidget,QTableWidgetItem
import mutagen
from mutagen.mp3 import MP3 #metadata manipulation
from mutagen.id3 import *
import musicbrainzngs
import eyed3
import librosa
import scipy.stats
import json
import objectpath

def getMetadata(artist, release):
    """ Data from public database Music brainz

        Parameters
        ----------
        artist : str
            Name of artists to search in database

        release : str
            Name of song=release from artist for searching

        Returns
        -------
        dict : information for table, with data about song
    """

    # variable for result of appending data
    finalList = {}

    #set name for search
    musicbrainzngs.set_useragent(
        "python-musicbrainzngs-example",
        "0.1",
        "https://github.com/alastair/python-musicbrainzngs/",
    )

    #wjson = json.loads(ss)
    #jsonnn_tree = objectpath.Tree(wjson)

    # getting data from web
    result = musicbrainzngs.search_releases(artist=artist, tracks=release,limit=1)

    # get to json format
    sorted_string = json.dumps(result, indent=4, sort_keys=True)

    #save  fro parsing
    wjson = json.loads(sorted_string)
    jsonnn_tree = objectpath.Tree(wjson['release-list'])

    #iterate for data in strings
    IDval = 0
    for (idx, release) in enumerate(result['release-list']):#goes once
        if 'date' in release:#check for existence
            finalList.update({"date":release['date']})
        if 'country' in release:
            finalList.update({"country":release['country']})
        if 'title' in release:
            finalList.update({"title":release['title']})
        if 'packaging' in release:
            finalList.update({"packaging":release['packaging']})
        if 'barcode' in release:
            finalList.update({"barcode":release['barcode']})
        if 'status' in release:
            finalList.update({"status":release['status']})
        if 'id' in release:
            finalList.update({"Release ID":release['id']})
            IDval = release['id']
        for (jdx, items) in enumerate(release):#iterovanie vo vsetkych
            repre = release[items]
            if 'text-representation' == items:
                if 'language' in (repre):
                    finalList.update({"language":repre['language']})
                if 'script' in (repre):
                    finalList.update({"script":repre['script']})
            if 'artist-credit' == items:
                #print(repre)
                #a = json.dumps(release[items], indent=4, sort_keys=True)
                #print(a)
                try:
                    tree = objectpath.Tree(release[items])
                    ent = tree.execute("$.artist[0]")
                    for x in (ent):
                        keyID = "Artist " + str(x)
                        finalList.update({keyID:ent[x]})
                except Exception:
                    pass

    return finalList
