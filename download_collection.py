# http://www.neje.club/ says
# neje.club is the server used by the neje team for software documentation support.
# All documents are edited by the neje team and copyrighted by neje. Please use it properly.


import os
import sys

name = "collection_links.txt"

f = open(name)

outdir = "Collection/"

try:
    os.mkdir(outdir)
except FileExistsError:
    pass

l = 0

for i in f.readlines():
    # print (i.split('"'))
    if not str.isspace(i):
        link = i.split('"')[1]
        print(link, "  ->  ", end="")
        n = link.split("/")
        # print(n)
        new_name = n[4] + "_" + n[5]
        print(new_name)
        cmd = "curl " + link + " > " + outdir + new_name
        print(cmd)
        os.system(cmd)
        l += 1
        # if l== 10:
        #    sys.exit()
