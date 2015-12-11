# __author__ = 'rynzar'
#  for name in folderList:
#         folder = "saves/"+name
#         rs = bucket.list( prefix=folder )
#         count = 0
#         for key in rs:
#             count+=1
#         final_str += (name + " " * 15)[:15]    + "\t"+str(count)+"\n"
#
#     print(final_str)

import os






def get_folders(d):
    ignore_folders = ['doc', 'src', '.vagrant', 'frontend', 'requirements', 'site-setup', 'migrations', 'tests', 'templates', 'commands', '.git', '.idea', 'test', 'static', 'cache', 'management', 'templatetags', 'settings', 'mixins', 'base_nba_stats']

    paths = filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d))
    arr = []
    for p in paths:
        if p not in ignore_folders and "__" not in p:
            arr.append(p)
    return arr

def make_title(name):
    title = name
    title = title.capitalize()
    title += "\n"
    for i in range(len(name)):
        title += "="
    return title

def make_doc(name, prefix):
    fullpath = "./doc/"+name+".rst"
    if not os.path.exists(fullpath):
        file_data = make_title(name)+"\n description \n\nViews\n-----\n.. automodule:: "+prefix+name+".views\n    :members:\n\nModels\n------\n.. automodule:: "+prefix+name+".models\n    :members:\n\nExceptions\n----------\n.. automodule:: "+prefix+name+".exceptions\n    :members:\n    :undoc-members:\n\nTesting\n-------\n.. automodule:: "+prefix+name+".tests\n    :members:\n"
        text_file = open(fullpath, "w")
        text_file.write(file_data)

        text_file.close()
def walk_tree(dir, spacing, prefix):
    folders = get_folders(dir)
    if folders != None:
        for p in get_folders(dir):
            print(spacing + p)
            make_doc(p, prefix)
            walk_tree(dir+"/"+p, spacing, prefix+p+".")





#print(make_doc("test"))
walk_tree(".", "    ", "")

#
# missingFiles = 0
# for directory in directories:
#     print(directory)
#     for file in file_names:
#         fullpath = base_dir+directory+"/"+file+".cfr"
#         if not os.path.exists(fullpath):
#             #print("dir:"+directory+" file:"+file + " fullpath:"+fullpath)
#             print("     "+file)
#             missingFiles +=1