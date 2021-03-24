#!/usr/bin/python

import math
import datetime
import os
import argparse
import stat
from pwd import getpwuid
from grp import getgrgid

def parseArgs():
    ##Initializing my parser for flags/arguments
    parser = argparse.ArgumentParser(description='Lists files and directories')

    ##Defining my flags/arguments
    parser.add_argument('directory', type=str, nargs='?', default='.') # nargs="?" allows zero or one arguments
    parser.add_argument('--all', '-a', action='store_true', help='Include dotfiles in listing')
    parser.add_argument('--long', '-l', action='store_true', help='Icludes the details of each file and directory')
    return parser.parse_args()

def aFlagOff(dirs):
    return [dir for dir in dirs if dir[0] != '.']

def lFlag(dirs, curdir):
    dirs.sort(key=str.lower)
    longDirs = []
    
    for obj in dirs:
        objinfo = os.stat(os.path.join(args.directory, obj))

        ##Filetype
        objtype = ''
        symlinkPath = ''
        if stat.S_ISDIR(objinfo.st_mode):
            objtype = 'l'
        elif stat.S_ISDIR(objinfo.st_mode):
            objtype = 'd'
        else:
            objtype = '-'

        ##File Permissions
        permBits = bin(objinfo.st_mode)[-9:] # we're grabbing the last 9 characters where the permission bits are stored
        permChars = ['r', 'w', 'x'] # read, write and execute characters that'll correspond to our permission bits
        permissions = ''
        for i, perm, in enumerate(permBits):
            if perm == '0': # zeroes are our dashes in the last 9 characters of permission bits
                permissions += '-'
            else:
                permissions += permChars[i % 3]

        ##Inode
        inode = str(objinfo.st_nlink) # nlink is nodelink

        ##User ID
        user = getpwuid(objinfo.st_uid).pw_name

        ##Group Name
        group = getgrgid(objinfo.st_gid).gr_name
        
        ##Sizes
        objBytes = objinfo.st_size
        bsize = str(objBytes) + 'b'

        ##Creation Date
        dateCreated = getDateCreated(objinfo.st_mtime)

        ##Append all priorly collected info together
        longDirs.append(objtype + permissions + ' ' + inode + '\t' + user + '\t' + group + '\t' + bsize + '\t' + dateCreated + '\t' + obj + '\t' + symlinkPath)

    return longDirs

def getDateCreated(time):
    time = datetime.datetime.fromtimestamp(time)
    if time < datetime.datetime.now() - datetime.timedelta(days = 365):
        return time.strftime('%b %d  %Y')
    return time.strftime('%b %d %H:%M')

def ls(args):
    dirs = os.listdir(args.directory) # the list of directories and files in a given directory

    if args.all:
        dirs += [os.curdir, os.pardir]
    else:
        ##Here we are readding everything in the list that doesn't start with '.'
        dirs = aFlagOff(dirs)
   
    if args.long:
        dirs = lFlag(dirs, args.directory)

    dirs.sort(key=str.lower) # the quickest way to sort the list, regardless of the casing

    for obj in dirs:
        print(obj)

if __name__ == '__main__':
    try:
        args = parseArgs()
        ls(args)
    except OSError as err:
        print(err)


