# Location of this file should be in the same folder as the bnta repo
# To run ---> py -u notebookToPdf.py
# I ran it from git bash and had to install a couple of packages

# If a file is unsuccessful, I suggest opening it, from its .html saved in its folder, in your browser and printing to pdf from there.
# Then change the name to be consistent with the rest and add it to your pdf folder. This means the program will not attempt to convert it in future. eg 1_1_Collaboration_index.pdf

#TO DO:
#Look into Continuous Integration with CircleCl so it automatically runs from git 

######### Import Modules #########

import os
import shutil

######### Configure #########

bnta_repo_name = 'content' #Replace with your repo name
save_to = 'pdfs_content' #Make folder where you would like it to save

redo_conversion = False #In case you want to redo all the conversions for some reason

######### CODE #########

def return_parts_path(full_path):
    parts = []
    path = full_path
    while os.path.split(path)[0] != "": # Checks there is more path to split
        root,part = os.path.split(path)
        path=root
        parts.append(part)
    parts.reverse()
    return parts

def check_for_day(parts):
    day_no = None
    for part in parts:
        if part.startswith('Day'):
            day_no = int(part[4:])
    return day_no

def change_name(parts,day_no):
    if day_no:
        week_no = (day_no-1)//5 + 1
        week_day = (day_no-1) % 5 + 1
        prefix = str(week_no) + '_' + str(week_day) + '_'
        return prefix + parts[-2] + '_' + parts[-1]
    else:
        return parts[-1]

def entire_fn():
    save_location = '.\\' + save_to
    CWD = os.getcwd()
    if redo_conversion:
        shutil.rmtree(save_location)
        os.mkdir(save_location)
    for root, dirs, files in os.walk(os.path.join('.',bnta_repo_name)):
        for file in files:
            if file.endswith(".ipynb"):
                parts = return_parts_path(os.path.join(root,file))
                pdf_name = parts[-1][0:-6] + '.pdf'

                orig_pdf_parts = parts.copy()
                orig_pdf_parts[-1] = pdf_name
                path_orig_pdf = os.path.join(*orig_pdf_parts)

                day_no = check_for_day(parts)
                pdf_name = change_name(orig_pdf_parts,day_no)
                move_to = os.path.join(save_location, pdf_name)

                if day_no:
                    if len(parts) == 4:
                        print('From {}: {} {}' .format(parts[1],parts[2],parts[3]),end=':           ')
                    elif len(parts) == 3:
                        print('From {}: {}' .format(parts[1],parts[2]),end=':           ')
                    else:
                        print('File structure is not as expected!!!!!!')
                else:
                    print('From content:', parts[1],end=':          ')

                if os.path.exists(move_to):
                    print('Already completed.')
                else:
                    TEMPDIR = os.path.join(*parts[0:-1])
                    os.chdir(TEMPDIR)
                    os.system('jupyter nbconvert --to pdf {} /f >nul 2>&1' .format(parts[-1]))
                    os.chdir(CWD)

                    try:
                        os.rename(path_orig_pdf,move_to)
                    except:
                        print('-------- Unsucessful. ---------')
                    else:
                        print('Successfully converted!')
            

entire_fn()
