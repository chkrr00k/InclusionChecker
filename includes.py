import os
import re
import sys
import getopt

HELP="""HELP
This program show all inclusion or modules/packages in files in a folder.
/!\ No recursion in folder is made (yet) and output is not grepable /!\ 

-l, --language <name>       choose the language name.
                            Defaults to python.
-p, --path <path>           the path of the folder.
                            Defaults to pwd.
-h, --help                  shows help.
--license                   shows the license.
"""

LICENSE_MESSAGE="""
    #############################################################
    #                                                           #
    #   This program is relased in the GNU GPL v3.0 license     #
    #   you can modify/use this program as you wish. Please     #
    #   link the original distribution of this software. If     #
    #   you plan to redistribute your modified/copied copy      #
    #   you need to relased the in GNU GPL v3.0 licence too     #
    #   according to the overmentioned licence.                 #
    #                                                           #
    #   "PROUDLY" MADE BY chkrr00k (i'm not THAT proud tbh)     #
    #                                                           #
    #############################################################
    #                                                           #
    #                                                           #
    #                            YEE                            #
    #                                                           #
    #                                                           #
    #############################################################
"""

def pythonImport(f, file):
    if file.endswith(".py"):
        print(file)
        imports = 0
        for line in f:
            if line.find("import") > -1:
                m = re.search(r"(from (\S+) )?import (\S+)", line.strip())
                if m:
                    if m.group(2) is None:
                        print("\t├─", m.group(3))
                    else:
                        print("\t├─", m.group(2) + "." + m.group(3))
                    imports += 1
        print("\t└──[Counted " + str(imports) + " import]")
    else:
        print("Skipping non python file", file)

def cInclude(f, file):
    if file.endswith(".c") or file.endswith(".h") or file.endswith(".cc") or file.endswith(".ccp"):
        print(file)
        imports = 0
        for line in f:
            if line.find("include") > -1:
                m = re.search(r"#include [<\"](\S+)[>\"]", line.strip())
                if m:
                    print("\t├─", m.group(1))
                    imports += 1
        print("\t└──[Counted " + str(imports) + " import]")
    else:
        print("Skipping non c file", file)

def javaImport(f, file):
    if file.endswith(".java"):
        print(file)
        imports = 0
        for line in f:
            if line.find("import") > -1:
                m = re.search(r"import (\S+)", line.strip())
                if m:
                    print("\t├─", m.group(1))
                    imports += 1
        print("\t└──[Counted " + str(imports) + " import]")
    else:
        print("Skipping non java file", file)

def phpImport(f, file):
    if file.endswith(".php"):
        print(file)
        imports = 0
        requires = 0
        for line in f:
            if line.find("require") > -1:
                m = re.search(r"require(_once)? (\S+)", line.strip())
                if m:
                    print("\t├─(r)─", m.group(2))
                    requires += 1
            elif line.find("include") > -1:
                m = re.search(r"include(_once)? (\S+)", line.strip())
                if m:
                    print("\t├─(i)─", m.group(2))
                    imports += 1
        print("\t├──[Counted " + str(requires) + " require]")
        print("\t└──[Counted " + str(imports) + " import]")
    else:
        print("Skipping non php file", file)        

def error(msg):
    print("ERROR")
    print(msg)
    sys.exit(1)
    
def main():
    languages = {"python" : pythonImport,
                 "c" : cInclude,
                 "java" : javaImport,
                 "php" : phpImport}
    path = os.getcwd()
    current = "python"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:l:y", ["help", "path=", "language=", "license"])
    except:
        error("Invalid arguments")
    for o, a in opts:
        if o in ("-h", "--help"):
            print(HELP)
            sys.exit(0)
        elif o in ("-l", "--language"):
            if a in languages:
                current = a
            else:
                error("Invalid arguments: language not valid")
        elif o in ("-p", "--path"):
            path = a
        elif o in ("--license"):
            print(LICENSE_MESSAGE)
            sys.exit(0)
    try:
        for file in os.listdir(path):
            if os.path.isdir(path + "\\" + file):
                print("Skipping dir", file)
            else:
                with open(path + "\\" + file) as f:
                    languages[current](f, file)
    except:
        error("Invalid folder: " + path)
            

if __name__ == "__main__":
    main()
