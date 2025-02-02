# Created on Thu Nov 21 09:45:47 2019
# @author: jack hester
# rewritten by Roberto Franzosi April 2020

import sys
import GUI_util
import IO_libraries_util
if IO_libraries_util.install_all_packages(GUI_util.window,"knowledge_graphs_DBpedia_YAGO_main.py",['os','tkinter','subprocess'])==False:
    sys.exit(0)

import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from subprocess import call

import GUI_IO_util
import IO_files_util
import IO_csv_util
import reminders_util
import constants_util

# RUN section ______________________________________________________________________________________________________________________________________________________

def run(inputFilename,inputDir,outputDir, openOutputFiles, createCharts, chartPackage,
        knowledge_graphs_DBpedia_var,
        knowledge_graphs_YAGO_var,
        confidence_level,
        databases_var,
        sub_class_entry,
        DBpedia_YAGO_class_list,
        DBpedia_YAGO_color_list,
        bold_DBpedia_YAGO_var):

    # if not DBpedia_YAGO_color_map:
    #     mb.showwarning(title='Warning', message="You haven't selected any ontology classes, by default we will annotated everything we could.")

    # check file number, if too many file pop the warning.
    inputDocs = IO_files_util.getFileList(inputFilename, inputDir, fileType='.txt')
    fileNum = len(inputDocs)
    if fileNum > 10:
        res = mb.askokcancel("File Number Warning",
                             "Your input directory contains more than 10 files. The annotation will take a significantly longer time (especially for YAGO), and the output will contain " +
                             str(fileNum) + " html files.\n\n Do you want to proceed? ")
        # stop the process if user click cancel
        if not res:
            return

    if knowledge_graphs_DBpedia_var==True or knowledge_graphs_YAGO_var==True:
        import IO_internet_util
        if knowledge_graphs_DBpedia_var:
            IO_internet_util.check_internet_availability_warning('DBpedia')
        else:
            IO_internet_util.check_internet_availability_warning('YAGO')

    if knowledge_graphs_DBpedia_var==True or knowledge_graphs_YAGO_var==True:
        if inputFilename!='' and inputFilename[-4:]!='.txt':
            mb.showwarning(title='Warning', message='You have selected to annotate your corpus, but the input file is not of type .txt as required by the selected annotator.\n\nPlease, select a .txt file (or a directory) and try again.')
            return
        # if DBpedia_YAGO_class_list==[]:
        #     mb.showwarning(title='Warning', message='You have selected to annotate your corpus but it looks like you have not selected any Ontology class or entered an Ontology sub-class.\n\nRemember to press the + button to add your selections')
        #     return

    ontology_list = list(DBpedia_YAGO_color_map.keys())
    colorls = list(DBpedia_YAGO_color_map.values())

    def final_check():
        # if class contains values, the user forgot to press + (which would empty the two widgets)
        #   not to lose the values, these are automatically appended (could also ask the user to confirm)
        if ontology_class_var.get()!='' and ontology_class_var.get() not in str(ontology_list):
            ontology_list.append(ontology_class_var.get())
        # if sub-class contains values, the user forgot to press + (which would empty the two widgets)
        #   not to lose the values, these are automatically appended (could also ask the user to confirm)
        if sub_class_entry_var.get()!='' and sub_class_entry_var.get() not in str(ontology_list):
            ontology_list.append(sub_class_entry_var.get())
        # if class and sub-class contain values, the user forgot to press + (which would empty the two widgets)
        #   not to lose the values, these are automatically appended (could also ask the user to confirm)
        if ontology_class_var.get()!='' or sub_class_entry_var.get() != '':
            if color_palette_DBpedia_YAGO_var.get()!='' and color_palette_DBpedia_YAGO_var.get() not in str(colorls):
                colorls.append(color_palette_DBpedia_YAGO_var.get())
            else:
                colorls.append('blue')
        if not ontology_list: # if nothing selected, annotate everything
            ontology_list.append('Thing')
            colorls.append('blue')



    if knowledge_graphs_DBpedia_var==True:
        if not IO_internet_util.check_internet_availability_warning('knowledge_graphs_DBpedia_YAGO_main.py'):
            return
        if IO_libraries_util.check_inputPythonJavaProgramFile('knowledge_graphs_DBpedia_util.py')==False:
            return
        import knowledge_graphs_DBpedia_util
        # for a complete list of annotator types:
        #http://mappings.DBpedia.org/server/ontology/classes/
        final_check()
        filesToOpen = knowledge_graphs_DBpedia_util.DBpedia_annotate(inputFilename, inputDir,
                                                                     outputDir,0,
                                                                     ontology_list, colorls, confidence_level)

    elif knowledge_graphs_YAGO_var==True:
        if not IO_internet_util.check_internet_availability_warning('knowledge_graphs_DBpedia_YAGO_main.py'):
            return
        import knowledge_graphs_YAGO_util
        if IO_libraries_util.check_inputPythonJavaProgramFile('knowledge_graphs_YAGO_util.py')==False:
            return
        # for a complete list of annotator types:
        #http://mappings.DBpedia.org/server/ontology/classes/

        color1 = 'black'
        final_check()

        filesToOpen = knowledge_graphs_YAGO_util.YAGO_annotate(inputFilename, inputDir, outputDir,
                                                                ontology_list, color1, colorls)

    else:
        mb.showwarning(title='Warning', message='There are no options selected.\n\nPlease, select one of the available options and try again.')
        return

    if openOutputFiles==True:
        if filesToOpen==None:
            if knowledge_graphs_DBpedia_var:
                print("\nDBpedia exited with error")
            if knowledge_graphs_YAGO_var:
                print("\nYAGO exited with error")
            return
        nFile=len(filesToOpen)
        if nFile > 5:
            mb.showwarning(title='Warning', message='There are too many output files (' + str(nFile) + ') to be opened automatically.\n\nPlease, do not forget to check the html files in your selected output directory.')
            return
        else:
            IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir)

#the values of the GUI widgets MUST be entered in the command otherwise they will not be updated
#def run(inputFilename,input_main_dir_path,outputDir, dictionary_var, annotator_dictionary, DBpedia_var, annotator_extractor, openOutputFiles):
run_script_command=lambda: run(GUI_util.inputFilename.get(),
                GUI_util.input_main_dir_path.get(),
                GUI_util.output_dir_path.get(),
                GUI_util.open_csv_output_checkbox.get(),
                                                GUI_util.create_chart_output_checkbox.get(),
                                GUI_util.charts_dropdown_field.get(),

                knowledge_graphs_DBpedia_var.get(),
                knowledge_graphs_YAGO_var.get(),
                confidence_level_entry.get(),
                databases_var.get(),
                sub_class_entry_var.get(),
                DBpedia_YAGO_class_list,
                DBpedia_YAGO_color_list,
                bold_DBpedia_YAGO_var.get())

GUI_util.run_button.configure(command=run_script_command)

# GUI section ______________________________________________________________________________________________________________________________________________________

# the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)
#   just change the next statement to True or False IO_setup_display_brief=True
IO_setup_display_brief=True
GUI_size, y_multiplier_integer, increment = GUI_IO_util.GUI_settings(IO_setup_display_brief,
                                                 GUI_width=GUI_IO_util.get_GUI_width(3),
                                                 GUI_height_brief=320, # height at brief display
                                                 GUI_height_full=400, # height at full display
                                                 y_multiplier_integer=GUI_util.y_multiplier_integer,
                                                 y_multiplier_integer_add=2, # to be added for full display
                                                 increment=2) # to be added for full display

GUI_label='Graphical User Interface (GUI) for HTML Annotating Documents Using the Knowledge Graphs (KG) DBpedia & YAGO'
head, scriptName = os.path.split(os.path.basename(__file__))
config_filename = scriptName.replace('main.py', 'config.csv')

# The 4 values of config_option refer to:
#   input file
        # 1 for CoNLL file
        # 2 for TXT file
        # 3 for csv file
        # 4 for any type of file
        # 5 for txt or html
        # 6 for txt or csv
#   input dir
#   input secondary dir
#   output dir
config_input_output_numeric_options=[5,1,0,1]

GUI_util.set_window(GUI_size, GUI_label, config_filename, config_input_output_numeric_options)

window=GUI_util.window
config_input_output_numeric_options=GUI_util.config_input_output_numeric_options
config_filename=GUI_util.config_filename
inputFilename=GUI_util.inputFilename

GUI_util.GUI_top(config_input_output_numeric_options,config_filename,IO_setup_display_brief)

def clear(e):
    ontology_class_var.set('')
    sub_class_entry_var.set('')
    clear_DBpedia_YAGO_class_list()
    DBpedia_YAGO_color_list.clear()
    add_class_button.configure(state='disabled')
    show_class_color_button.configure(state='disabled')
    GUI_util.clear("Escape")
window.bind("<Escape>", clear)

DBpedia_YAGO_class_list=[]
DBpedia_YAGO_color_list=[]
DBpedia_YAGO_color_map = {}

knowledge_graphs_DBpedia_var=tk.IntVar() # to annotate a document using DBpedia
knowledge_graphs_YAGO_var=tk.IntVar() # to annotate a document using YAGO
confidence_level_var=tk.StringVar()
databases_var=tk.StringVar()
ontology_class_var = tk.StringVar()
sub_class_entry_var = tk.StringVar()
color_palette_DBpedia_YAGO_var= tk.StringVar() # the color selected for DBpedia/YAGO annotation
bold_DBpedia_YAGO_var= tk.IntVar() # display in bod the selected color selected for DBpedia/YAGO annotation

# http://mappings.dbpedia.org/server/ontology/classes/
# DBpedia_menu_options=(
#         'Thing',
#         'Activity',
#         'Agent',
#         'Algorithm'
#         'Altitude',
#         'AnatomicalStructure',
#         'Area',
#         'Award',
#         'Biomolecule',
#         'Blazon',
#         'Browser',
#         'ChartsPlacements',
#         'ChemicalSubstance',
#         'Cipher',
#         'Colour',
#         'Currency',
#         'Demographics',
#         'Depth',
#         'Device',
#         'Diploma',
#         'Disease',
#         'ElectionDiagram',
#         'ElectricalSubstation',
#         'EthnicGroup',
#         'Event',
#         'FileSystem',
#         'Flag',
#         'Food',
#         'GeneLocation',
#         'GrossDomesticProduct',
#         'GrossDomesticProductPerCapita',
#         'Holiday',
#         'Identifier',
#         'Language',
#         'List',
#         'MeanOfTransportation',
#         'Media',
#         'MedicalSpecialty',
#         'Medicine',
#         'Name',
#         'Person',
#         'Place',
#         'Population',
#         'Protocol',
#         'PublicService',
#         'Relationship',
#         'Species',
#         'SportCompetitionResult',
#         'SportsSeason',
#         'Spreadsheet',
#         'StarCluster',
#         'Statistic',
#         'Tank',
#         'TimePeriod',
#         'TopicalConcept',
#         'UnitOfWork',
#         'Unknown',
#         'Work')

# These are schema.org classes https://schema.org/docs/full.html
# YAGO_menu_options=(
#         'BioChemEntity', 	# bioschemas
#         'Gene',				# bioschemas
#         'MolecularEntity',	# bioschemas
#         'Taxon',			# bioschemas
#         'Brand',			# schema
#         'BroadcastChannel',	# schema
#         'CreativeWork',		# schema
#         'Emotion',			# yago
#         'MedicalEntity',	# schema
#         'Organization',		# schema
#         'Person',			# schema
#         'Place',			# schema
#         'Product')			# schema

# temporarily set DBpedia_YAGO_menu_options to avoid
#	is not defined error
# DBpedia_YAGO_menu_options=DBpedia_menu_options

def activate_DBpedia_YAGO_menu():
    global DBpedia_YAGO_menu_options
    if knowledge_graphs_DBpedia_var.get():
        DBpedia_YAGO_menu_options=DBpedia_ontology_class_menu
    if knowledge_graphs_YAGO_var.get():
        DBpedia_YAGO_menu_options=YAGO_ontology_class_menu

y_multiplier_integerSV= y_multiplier_integer

knowledge_graphs_DBpedia_var.set(0)
knowledge_graphs_DBpedia_checkbox = tk.Checkbutton(window, text='HTML annotate corpus using DBpedia knowledge graph)', variable=knowledge_graphs_DBpedia_var, onvalue=1, offvalue=0,command=lambda: activate_DBpedia_YAGO_menu())
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(),y_multiplier_integer,knowledge_graphs_DBpedia_checkbox,True)

# http://yago.r2.enst.fr/
# http://yago.r2.enst.fr/downloads/yago-4
knowledge_graphs_YAGO_var.set(0)
knowledge_graphs_YAGO_checkbox = tk.Checkbutton(window, text='HTML annotate corpus using YAGO knowledge graph',variable=knowledge_graphs_YAGO_var, onvalue=1, offvalue=0,command=lambda: activate_DBpedia_YAGO_menu())
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate()+200,y_multiplier_integer,knowledge_graphs_YAGO_checkbox,True)

confidence_level_lb = tk.Label(window, text='DBpedia confidence level')
# y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate()+270,y_multiplier_integer,confidence_level_lb,True)

confidence_level_entry = tk.Scale(window, from_=0.0, to=1.0, resolution = 0.1, orient=tk.HORIZONTAL)
# y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate()+420,y_multiplier_integer,confidence_level_entry)
confidence_level_entry.set(.5)

y_multiplier_integer=y_multiplier_integerSV+1

DB_menu_options=('*','Wikipedia', 'Wikidata')
databases_var.set('')
databases_menu_lb = tk.Label(window, text='Databases')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+20,y_multiplier_integer,databases_menu_lb,True)
databases_menu = tk.OptionMenu(window,databases_var,*DB_menu_options)
databases_menu.configure(state="disabled")
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+100,y_multiplier_integer,databases_menu,True)


#activated when pressing the RESET button

def clear_DBpedia_YAGO_class_list():
    ontology_class_var.set('')
    sub_class_entry_var.set('')
    DBpedia_YAGO_class_list.clear()
    DBpedia_YAGO_color_list.clear()
    DBpedia_YAGO_color_map.clear()
    color_palette_DBpedia_YAGO_var.set('')
    confidence_level_var.set('.5')
    reset_class_button.configure(state='disabled')
    activate_DBpedia_YAGO_Options(y_multiplier_integerSV,confidence_level_lb,confidence_level_entry)

def accept_DBpedia_YAGO_list():
    #press OK
    global DBpedia_YAGO_class_list
    if sub_class_entry_var.get()!='':
        color = color_palette_DBpedia_YAGO_var.get()
        if not color:
            color = 'blue'
        for token in sub_class_entry_var.get().split(' '):
            if token:
                DBpedia_YAGO_class_list.append(token)
                DBpedia_YAGO_color_map[token] = color
        # print(DBpedia_YAGO_color_map)

        DBpedia_YAGO_color_list.append(color)
        # DBpedia_YAGO_class_list=[str(x) for x in sub_class_entry_var.get().split(',') if x]
    elif ontology_class_var.get() != '':

        color = color_palette_DBpedia_YAGO_var.get()
        if not color:
            color = 'blue'
        DBpedia_YAGO_color_map[ontology_class_var.get()] = color
        DBpedia_YAGO_class_list.append(ontology_class_var.get())
        DBpedia_YAGO_color_list.append(color)
    else:
        mb.showwarning(title='Warning', message='You have pressed the OK button, but you must first select your class(es).\n\nPlease, select the class(es) and try again.')

def add_DBpedia_sub_class(*args):
    if sub_class_entry_var.get()!='':
        activate_DBpedia_YAGO_Options(y_multiplier_integerSV,confidence_level_lb,confidence_level_entry)
sub_class_entry_var.trace ('w',add_DBpedia_sub_class)

YAGO_ontology_class_menu = constants_util.YAGO_ontology_class_menu
DBpedia_ontology_class_menu = constants_util.DBpedia_ontology_class_menu

ontology_class_lb = tk.Label(window, text='Class')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+180,y_multiplier_integer,ontology_class_lb,True)
ontology_class_var.set('')
# to jump to an item in the list that starts with a specific letter (e.g., without) by pressing that letter (e.g., w)
# https://stackoverflow.com/questions/32747592/can-you-have-a-tkinter-drop-down-menu-that-can-jump-to-an-entry-by-typing
# autocomplete
# https://stackoverflow.com/questions/12298159/tkinter-how-to-create-a-combo-box-with-autocompletion
# for the code
#   https://mail.python.org/pipermail/tkinter-discuss/2012-January/003041.html

if sys.platform == 'win32':
    ontology_width = 30
elif sys.platform == 'darwin':
    ontology_width = 20

ontology_class = ttk.Combobox(window, width = ontology_width, textvariable = ontology_class_var)
ontology_class['values'] = DBpedia_ontology_class_menu
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+230, y_multiplier_integer,ontology_class,True)
ontology_class.configure(state='disabled')

sub_class_entry_lb = tk.Label(window, text='Sub-class')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+470,y_multiplier_integer,sub_class_entry_lb,True)

sub_class_entry = tk.Entry(window,width=35,textvariable=sub_class_entry_var)
sub_class_entry.configure(state="disabled")
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+550,y_multiplier_integer,sub_class_entry,True)

color_palette_DBpedia_YAGO_var.set('')
color_palette_DBpedia_YAGO_lb = tk.Label(window, text='Color')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+780,y_multiplier_integer,color_palette_DBpedia_YAGO_lb,True)
color_palette_DBpedia_YAGO_menu = tk.OptionMenu(window, color_palette_DBpedia_YAGO_var,'black','blue','green','pink','red','yellow')
color_palette_DBpedia_YAGO_menu.configure(state='disabled')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+830, y_multiplier_integer,color_palette_DBpedia_YAGO_menu,True)

bold_DBpedia_YAGO_var.set(1)
bold_DBpedia_YAGO_checkbox = tk.Checkbutton(window, text='Bold', state='disabled',variable=bold_DBpedia_YAGO_var, onvalue=1, offvalue=0)
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+900,y_multiplier_integer,bold_DBpedia_YAGO_checkbox,True)

def activate_class_var(*args):
    if ontology_class_var.get() or sub_class_entry_var.get():
        accept_DBpedia_YAGO_list()  # get current vale and stores into the dict
        ontology_class_var.set('')
        color_palette_DBpedia_YAGO_var.set('')
        sub_class_entry_var.set('')
        add_class_button.configure(state='normal')
        show_class_color_button.configure(state='normal')
    else:
        add_class_button.configure(state='disabled')
    ontology_class.configure(state='normal')

reset_class_button = tk.Button(window, text='Reset', width=5,height=1,state='disabled',command=lambda: clear_DBpedia_YAGO_class_list())
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+970,y_multiplier_integer,reset_class_button,True)

def show_class_color_list():
    # if len(DBpedia_YAGO_color_list)==0:
    #     if len(DBpedia_YAGO_class_list)==0:
    #         mb.showwarning(title='Warning', message='There are no currently selected combinations of ontology class and color.')
    #     else:
    #         mb.showwarning(title='Warning',
    #                        message='The currently selected ontology class list\n  ' + str(DBpedia_YAGO_class_list) + '\nhas no colors associated with it.')
    if not DBpedia_YAGO_color_map:
        mb.showwarning(title='Warning',
                       message='There are no currently selected combinations of ontology class and color.')
    else:
        class_color_string = ""
        for ont in DBpedia_YAGO_color_map.keys():
            class_color_string = class_color_string + ont + ":" + DBpedia_YAGO_color_map[ont] + "\n"
        # mb.showwarning(title='Warning', message='The currently selected combination of ontology classes and colors are:\n\n' + ','.join(DBpedia_YAGO_color_list) + '\n\nPlease, press the RESET button (or ESCape) to start fresh.')
        mb.showwarning(title='Warning', message='The currently selected combination of ontology classes and colors are:\n\n' + class_color_string + '\n\nPlease, press the RESET button (or ESCape) to start fresh.')

show_class_color_button = tk.Button(window, text='Show', width=5,height=1,state='disabled',command=lambda: show_class_color_list())
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+1035,y_multiplier_integer,show_class_color_button,True)

firstTime = False

add_class_button = tk.Button(window, text='+', width=2,height=1,state='disabled',command=lambda: activate_class_var())
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+1100,y_multiplier_integer,add_class_button)

# https://www.python.org/download/mac/tcltk/
# https://stackoverflow.com/questions/24207870/cant-reenable-menus-in-python-tkinter-on-mac
# In Mac, widgets are temporarily turned disabled but immediately return to normal. This is a bug in the Apple-supplied Tk 8.5. The Cocoa versions of Tk that Apple has been shipping since OS X 10.6 have had numerous problems many of which have been fixed in more recent versions of Tk 8.5. With the current ActiveTcl 8.5.15, your test appears to work correctly. Unfortunately, you can't easily change the version of Tcl/Tk that the Apple-supplied system Pythons use. One option is to install the current Python 2.7.7 from the python.org binary installer along with ActiveTcl 8.5.15. There is more information here:

# https://www.python.org/downloads/

def activate_DBpedia_YAGO_Options(y_multiplier_integerSV,confidence_level_lb,confidence_level_entry,*args):
    global firstTime
    if knowledge_graphs_DBpedia_var.get()==False and knowledge_graphs_YAGO_var.get()==False:
        DBpedia_YAGO_class_list.clear()
        DBpedia_YAGO_color_list.clear()
        ontology_class_var.set('') # DBpedia_YAGO_menu_options
        knowledge_graphs_DBpedia_checkbox.configure(state="normal")
        knowledge_graphs_YAGO_checkbox.configure(state="normal")
        y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate()+200, y_multiplier_integerSV,
                                                   knowledge_graphs_YAGO_checkbox)
    else:
        ontology_class.configure(state='normal')
    if knowledge_graphs_DBpedia_var.get()==True:
        ontology_class['values'] = DBpedia_ontology_class_menu
        y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate()+200, y_multiplier_integerSV,
                                                       knowledge_graphs_YAGO_checkbox, True)
        y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate() + 550,
                                                       y_multiplier_integerSV, confidence_level_lb,True)
        y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate() + 720,
                                                       y_multiplier_integerSV, confidence_level_entry)
        knowledge_graphs_YAGO_checkbox.configure(state="disabled")
    else:
        y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_entry_box_x_coordinate()+200, y_multiplier_integerSV,
                                                       knowledge_graphs_YAGO_checkbox)
        confidence_level_lb.place_forget()  # invisible
        confidence_level_entry.place_forget()  # invisible
    if knowledge_graphs_DBpedia_var.get()==True:
        knowledge_graphs_YAGO_checkbox.configure(state="disabled")
    if knowledge_graphs_YAGO_var.get()==True:
        ontology_class['values'] = YAGO_ontology_class_menu
        knowledge_graphs_DBpedia_checkbox.configure(state="disabled")
    if knowledge_graphs_DBpedia_var.get()==True or knowledge_graphs_YAGO_var.get()==True:
        # display the reminder only once in the same GUI or the trace will display it many times
        if firstTime==False:
            reminders_util.checkReminder(config_filename,
                                         reminders_util.title_options_DBpedia_YAGO,
                                         reminders_util.message_DBpedia_YAGO,
                                         True)
        firstTime=True
        # databases_menu.configure(state="normal")
        ontology_class.configure(state='normal')
        sub_class_entry.configure(state="normal")
    else:
        databases_menu.configure(state="disabled")
        ontology_class.configure(state='disabled')
        sub_class_entry.configure(state="disabled")
knowledge_graphs_DBpedia_var.trace('w',callback = lambda x,y,z: activate_DBpedia_YAGO_Options(y_multiplier_integerSV,confidence_level_lb,confidence_level_entry))
knowledge_graphs_YAGO_var.trace('w',callback = lambda x,y,z: activate_DBpedia_YAGO_Options(y_multiplier_integerSV,confidence_level_lb,confidence_level_entry))

def activate_class_options(*args):
    if ontology_class_var.get() in DBpedia_YAGO_class_list:
        mb.showwarning(title='Warning', message='The class "'+ ontology_class_var.get() + '" is already in your selection list: '+ str(DBpedia_YAGO_class_list) + '.\n\nPlease, select another class.')
        window.focus_force()
        return
    state = str(ontology_class['state'])
    if state != 'disabled':
        if ontology_class_var.get() != '':
            add_class_button.configure(state='normal')
            reset_class_button.configure(state='normal')
            show_class_color_button.configure(state='normal')
            DBpedia_YAGO_class_list.append(ontology_class_var.get())
            ontology_class.configure(state='disabled')
            # sub_class_entry.configure(state="disabled")
            color_palette_DBpedia_YAGO_menu.configure(state='normal')
            if color_palette_DBpedia_YAGO_var.get() != '':
                add_class_button.configure(state='normal')
            # color palette ONLY available when selecting a major ontology class from the dropdown menu
            # color_palette_DBpedia_YAGO_menu.configure(state='normal')
        else:
            color_palette_DBpedia_YAGO_menu.configure(state='disabled')
    else:
        reset_class_button.configure(state='normal')
        if sub_class_entry_var.get() != '':
            ontology_class.configure(state='disabled')
        else:
            ontology_class.configure(state='normal')
ontology_class_var.trace ('w',activate_class_options)

def activate_OK_buttton(*args):
    if ontology_class_var.get() != '' or sub_class_entry_var.get() != '':
        add_class_button.config(state="normal")
    if sub_class_entry_var.get() != '':
        ontology_class.configure(state='disabled')
        color_palette_DBpedia_YAGO_menu.configure(state='normal')
        reset_class_button.configure(state='normal')
    if not ontology_class_var.get() and not sub_class_entry_var.get():
        add_class_button.config(state="disabled")
sub_class_entry_var.trace('w',activate_OK_buttton)
ontology_class_var.trace('w', activate_OK_buttton)

def activate_class_color_combo(*args):
    if color_palette_DBpedia_YAGO_var.get()!='':
        state = str(color_palette_DBpedia_YAGO_menu['state'])
        # 'active' for mac; 'normal' for windows
        if state != 'disabled': # normal/active
            color_palette_DBpedia_YAGO_menu.configure(state='disabled')
            add_class_button.configure(state='normal')
            reset_class_button.configure(state='normal')
            show_class_color_button.configure(state='normal')
color_palette_DBpedia_YAGO_var.trace('w',activate_class_color_combo)

videos_lookup = {'No videos available':''}
videos_options='No videos available'

TIPS_lookup = {'csv files - Problems & solutions':'TIPS_NLP_csv files - Problems & solutions.pdf','Statistical measures':'TIPS_NLP_Statistical measures.pdf','Annotator':'TIPS_NLP_Annotator.pdf','Annotator DBpedia':'TIPS_NLP_Annotator DBpedia.pdf','DBpedia ontology classes':'TIPS_NLP_Annotator DBpedia ontology classes.pdf','YAGO (schema.org) ontology classes':'TIPS_NLP_Annotator YAGO (schema.org) ontology classes.pdf','YAGO (REDUCED schema.org) ontology classes':'TIPS_NLP_Annotator YAGO (schema reduced).pdf','The world of emotions and sentiments':'TIPS_NLP_The world of emotions and sentiments.pdf','W3C, OWL, RDF, SPARQL':'TIPS_NLP_W3C OWL RDF SPARQL.pdf','Annotator dictionary':'TIPS_NLP_Annotator dictionary.pdf','Annotator extractor':'TIPS_NLP_Annotator extractor.pdf','Gender annotator':'TIPS_NLP_Gender annotator.pdf'}
TIPS_options='csv files - Problems & solutions','Statistical measures','Annotator','Annotator DBpedia','DBpedia ontology classes','YAGO (schema.org) ontology classes','YAGO (REDUCED schema.org) ontology classes','The world of emotions and sentiments','W3C, OWL, RDF, SPARQL', 'Annotator dictionary','Annotator extractor','Gender annotator'
# add all the lines to the end to every special GUI
# change the last item (message displayed) of each line of the function y_multiplier_integer = help_buttons
# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util.
def help_buttons(window,help_button_x_coordinate,y_multiplier_integer):
    if not IO_setup_display_brief:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_txtFile)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_corpusData)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_outputDirectory)
    else:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                  GUI_IO_util.msg_IO_setup)

    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help", 'Please, tick the appropriate checkbox if you wish to run the Python 3 annotator_DBpedia script or annotator_YAGO script to annotate the input corpus by terms found in either DBpedia or YAGO.\n\nDBpedia will allow you to set confidence levels for your annotation (.5 is the recommended default value in a range between 0 and 1). THE HIGHER THE CONFIDENCE LEVEL THE LESS LIKELY YOU ARE TO FIND DBpedia ENTRIES; THE LOWER THE LEVEL AND THE MORE LIKELY YOU ARE TO FIND EXTRANEOUS ENTRIES.\n\nDBpedia and YAGO are enormous databases (DB for database) designed to extract structured content from the information created in Wikipedia, Wikidata and other knowledge bases. DBpedia and YAGO allow users to semantically query relationships and properties of Wikipedia data (including links to other related datasets) via a large ontology of search values (for a complete listing, see the TIPS files TIPS_NLP_DBpedia Ontology Classes.pdf or TIPS_NLP_YAGO (schema.org) Ontology Classes.pdf).\n\nFor more information, see https://wiki.DBpedia.org/ and https://yago-knowledge.org/.\n\nIn INPUT the scripts expect one or more txt files.\n\nIn OUTPUT the scripts generate as many annotated html files as selected in input.')
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help", 'Once you tick the DBpedia or YAGO checkbox, the options on this line will become available.\n\nUsing the class dropdown menu, select the DPpedia or YAGO ontology class you wish to use.\n Press the + button to add another selection.\n IF NO CLASS IS SELECTED, ALL CLASSES WILL BE PROCESSED, WITH \'THING\' AS THE DEFAULT CLASS.\n\nThe class dropdown menu only includes the main classes in the DBpedia or YAGO ontology. For specific sub-classes, please, get the values from the TIPS_NLP_DBpedia ontology classes.pdf or TIPS_NLP_YAGO (schema.org) Ontology Classes.pdf and enter them, comma-separated, in Ontology sub-class field. CLICK + AFTER ENTERING CLASS AND/OR SUB-CLASS VALUES.\n\nYAGO DOES NOT USE THE COMPLETE SCHEMA CLASSES AND SUB-CLASSES. PLEASE, REFER TO THE REDUCED LIST FOR ALL THE SCHEMA CLASSES USED.\n\nYou can test the resulting annotations directly on DBpedia Spotlight at https://www.dbpedia-spotlight.org/demo/\n\nYou can select a specific color for a specific ontology class (Press the \'Show\' widget to display the combination of seleted values).\n\nPress RESET (or ESCape) to delete all values entered and start fresh.\nPress SHOW to display all selected values (the SHOW button only becomes available afyter pressing the + button to confirm your choices).\n\nThe RESET, SHOW, and + widgets become available only after selecting an ontology class or sub-class.')
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",GUI_IO_util.msg_openOutputFiles)
    return y_multiplier_integer -1

y_multiplier_integer = help_buttons(window,GUI_IO_util.get_help_button_x_coordinate(),0)

# change the value of the readMe_message
readMe_message="The Python 3 scripts provide ways of annotating text files for matching terms found in the knowledge graphs DBpedia or YAGO.\n\nDBpedia and YAGO tags can be selected from the class dropdown menu containing the DBpedia and YAGO ontology. The menu only includes the main classes in the ontology. For specific sub-classes, please, get the values from the TIPS_NLP_DBpedia ontology classes.pdf or TIPS_NLP_YAGO (schema.org) ontology classes.pdf and enter them in the Ontology sub-class field."
readMe_command = lambda: GUI_IO_util.display_button_info("NLP Suite Help", readMe_message)
GUI_util.GUI_bottom(config_filename, config_input_output_numeric_options, y_multiplier_integer, readMe_command, videos_lookup, videos_options, TIPS_lookup, TIPS_options, IO_setup_display_brief, scriptName)

GUI_util.window.mainloop()

