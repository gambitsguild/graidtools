#!/usr/bin/python
import getopt, sys
from os import write
from typing import List

def write_macro(groups, export=True):
    with open("all_groups.txt","w") as macro:
        for index, data in enumerate(groups):
            line = "/rw " + "group %s" % str(index + 1) + " {skull} %s || {cross} %s || {square} %s || {moon} %s || {triangle} %s" % tuple(data)
            print(line)
            if export:
                macro.write(line + "\n")

def groups_from_url(url) -> List:
    # find first ; from there names begin in url
    chars = url[url.index(';')+1:].replace(';',',')
    all_names = chars.split(',')
    all_names = [name.strip() or "PUG" for name in all_names]

    # Make 2 groups of 5
    n_groups = 2
    per_grp = 5
    
    # Split up all_names into groups of 5
    groups = [all_names[i : i + per_grp] for i in range(0, len(all_names), per_grp)]
    # Pick the first N groups from the groups
    groups = groups[:n_groups]

    return groups

def test():
    test_url="https://tbc.wowhead.com/raid-composition#0xxxxxxxxxxxxxxxxxxxxxxxxx;A;B;C;D;E;F;G;H;I;J;A;B;C;D;E;F;G;H;I;J"
    expected = [["A","B","C","D","E"],["F","G","H","I","J"]]
    actual = groups_from_url(test_url)
    write_macro(actual, False)
    print("Test Passed") if expected == actual else print("Test failed")




# CLI USAGE: python mag_groups.py -u "https://some_tbc_wowhead_url_goes_here"
if __name__ == '__main__':

    arguments = sys.argv[1:]
    short_options = "hu:t"
    long_options = ["help", "url=","test"]


    if len(arguments) > 0:
        try:
            arguments, values = getopt.getopt(arguments, short_options, long_options)
        except getopt.error as err:
            # Output error, and return with an error code
            print (str(err))
            sys.exit(2)
    else:
        print('Not enough arguments set')
        

    for current_argument, current_value in arguments:
        if current_argument in ("-u", "--url"):
            print ("using url: %s" % current_value)
            write_macro(groups_from_url(current_value))
        elif current_argument in ("-h", "--help"):
            print ("use -u '<url>' or --url='<url>' to set a url e.g. --url='google.com'")
        elif current_argument in ("-t","--test"):
            print("running test")
            test()