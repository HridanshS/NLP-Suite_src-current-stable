#written by Roberto Franzosi November 2019

import sys
import GUI_util
import IO_libraries_util

if IO_libraries_util.install_all_packages(GUI_util.window,"Wordclouds",['os','tkinter','webbrowser'])==False:
    sys.exit(0)

import os
import webbrowser
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from subprocess import call

import GUI_IO_util
import IO_csv_util
import Gephi_util
import IO_files_util

# csv_file_field_list contains the column header of node1, edge, node2 (e.g., SVO)

def runGephi(inputFilename, outputDir, csv_file_field_list, dynamic_network_field_var):
    fileBase = os.path.basename(inputFilename)[0:-4]
    return Gephi_util.create_gexf(GUI_util.window, fileBase, outputDir, inputFilename,
                                  csv_file_field_list[0], csv_file_field_list[1],
                                  csv_file_field_list[2], dynamic_network_field_var)

def run(inputFilename, inputDir, outputDir, openOutputFiles, csv_file_field_list, dynamic_network_field_var):
    if Gephi_var==False:
        mb.showwarning("Warning",
                       "No options have been selected.\n\nPlease, select an option to run and try again.")
        # Gephi_var.set(0)
        return
    else:
        # check if input file is csv
        if os.path.basename(inputFilename)[-4:] != ".csv":
            mb.showwarning("Warning",
                           "The input file must be a csv file.")
            return
        filesToOpen = []
        gexf_file = runGephi(inputFilename, outputDir, csv_file_field_list, dynamic_network_field_var)
        filesToOpen.append(gexf_file)
        if openOutputFiles and len(filesToOpen) > 0:
            IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir)


#the values of the GUI widgets MUST be entered in the command otherwise they will not be updated
run_script_command=lambda: run(GUI_util.inputFilename.get(),
                            GUI_util.input_main_dir_path.get(),
                            GUI_util.output_dir_path.get(),
                            GUI_util.open_csv_output_checkbox.get(),
                            csv_file_field_list,
                            dynamic_network_field_var.get())

GUI_util.run_button.configure(command=run_script_command)

# GUI section ______________________________________________________________________________________________________________________________________________________

# the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)
#   just change the next statement to True or False IO_setup_display_brief=True
IO_setup_display_brief=True
GUI_size, y_multiplier_integer, increment = GUI_IO_util.GUI_settings(IO_setup_display_brief,
                             GUI_width=GUI_IO_util.get_GUI_width(3),
                             GUI_height_brief=520, # height at brief display
                             GUI_height_full=600, # height at full display
                             y_multiplier_integer=GUI_util.y_multiplier_integer,
                             y_multiplier_integer_add=2, # to be added for full display
                             increment=2)  # to be added for full display

GUI_label='Graphical User Interface (GUI) for Visualization Tools'
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
config_input_output_numeric_options=[3,1,0,1]

GUI_util.set_window(GUI_size, GUI_label, config_filename, config_input_output_numeric_options)
window=GUI_util.window
config_input_output_numeric_options=GUI_util.config_input_output_numeric_options
config_filename=GUI_util.config_filename
inputFilename=GUI_util.inputFilename
input_main_dir_path=GUI_util.input_main_dir_path

GUI_util.GUI_top(config_input_output_numeric_options,config_filename,IO_setup_display_brief)

def clear(e):
    GUI_util.clear("Escape")
window.bind("<Escape>", clear)


Gephi_var = tk.IntVar()
selected_csv_file_fields_var = tk.StringVar()

csv_file_field_list = []
menu_values = []

dynamic_network_field_var = tk.IntVar()

Excel_button = tk.Button(window, text='Open Excel GUI', width=GUI_IO_util.select_file_directory_button_width, height=1,
                               command=lambda: call("python charts_Excel_main.py", shell=True))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               Excel_button)

GIS_button = tk.Button(window, text='Open GIS GUI', width=GUI_IO_util.select_file_directory_button_width, height=1,
                               command=lambda: call("python GIS_main.py", shell=True))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               GIS_button)

HTML_button = tk.Button(window, text='Open HTML annotator GUI', width=GUI_IO_util.select_file_directory_button_width, height=1,
                               command=lambda: call("python html_annotator_main.py", shell=True))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               HTML_button)

wordcloud_button = tk.Button(window, text='Open wordcloud GUI', width=GUI_IO_util.select_file_directory_button_width, height=1,
                               command=lambda: call("python wordclouds_main.py", shell=True))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               wordcloud_button)
Gephi_var.set(0)
Gephi_checkbox = tk.Checkbutton(window, text='Visualize relations in a Gephi network graph', variable=Gephi_var,
                                    onvalue=1)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               Gephi_checkbox)

if GUI_util.inputFilename.get() != '':
    nRecords, nColumns = IO_csv_util.GetNumberOf_Records_Columns_inCSVFile(GUI_util.inputFilename.get())
    if IO_csv_util.csvFile_has_header(GUI_util.inputFilename.get()) == False:
        menu_values = range(1, nColumns + 1)
    else:
        data, headers = IO_csv_util.get_csv_data(GUI_util.inputFilename.get(), True)
        menu_values = headers
else:
    nColumns = 0
    menu_values = " "
if nColumns == -1:
    pass

def changed_filename(tracedInputFile):
    menu_values = []
    if tracedInputFile != '':
        nRecords, nColumns = IO_csv_util.GetNumberOf_Records_Columns_inCSVFile(tracedInputFile)
        if nColumns == 0 or nColumns == None:
            return False
        if IO_csv_util.csvFile_has_header(tracedInputFile) == False:
            menu_values = range(1, nColumns + 1)
        else:
            data, headers = IO_csv_util.get_csv_data(tracedInputFile, True)
            menu_values = headers
    else:
        menu_values.clear()
        return
    m1 = select_csv_field_menu["menu"]
    m2 = dynamic_network_field_menu["menu"]
    m1.delete(0, "end")
    m2.delete(0, "end")

    for s in menu_values:
        m1.add_command(label=s, command=lambda value=s: csv_field_var.set(value))
        m2.add_command(label=s, command=lambda value=s: dynamic_network_field_var.set(value))
    clear("<Escape>")

select_csv_field_lb = tk.Label(window, text='Select csv file field')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_indented_coordinate(), y_multiplier_integer,
                                               select_csv_field_lb, True)

csv_field_var = tk.StringVar()
select_csv_field_menu = tk.OptionMenu(window, csv_field_var, *menu_values)
select_csv_field_menu.configure(state='disabled', width=12)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_indented_coordinate()+150, y_multiplier_integer,
                                               select_csv_field_menu, True)

GUI_util.inputFilename.trace('w', lambda x, y, z: changed_filename(GUI_util.inputFilename.get()))

changed_filename(GUI_util.inputFilename.get())

OK_button = tk.Button(window, text='OK', width=3, height=1, state='disabled',
                            command=lambda: display_selected_csv_fields(True,False))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 800, y_multiplier_integer,
                                               OK_button,True)

add_button_var = tk.IntVar()
add_button = tk.Button(window, text='+', width=2, height=1, state='disabled',
                              # command=lambda: add_field_to_list(selected_csv_file_fields_var.get()))
                                command = lambda: activate_csv_fields_selection(True,False))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 850, y_multiplier_integer,
                                               add_button, True)

reset_button = tk.Button(window, text='Reset', width=5,height=1,state='disabled',command=lambda: reset())
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 900,y_multiplier_integer,reset_button, True)

select_csv_field_dynamic_network_lb = tk.Label(window, text='Select csv file field for dynamic network graph')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_indented_coordinate()+300, y_multiplier_integer,
                                               select_csv_field_dynamic_network_lb, True)

dynamic_network_field_var = tk.StringVar()
dynamic_network_field_menu = tk.OptionMenu(window, dynamic_network_field_var, *menu_values)
dynamic_network_field_menu.configure(state='disabled', width=12)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_indented_coordinate()+600, y_multiplier_integer,
                                               dynamic_network_field_menu)

csv_file_fields=tk.Entry(window, width=150,textvariable=selected_csv_file_fields_var)
csv_file_fields.config(state='disabled')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_indented_coordinate(), y_multiplier_integer,csv_file_fields)

def activate_csv_fields_selection(comingFrom_Plus, comingFrom_OK):
    # check if input file is csv
    if Gephi_var.get()==True:
        if os.path.basename(inputFilename.get())[-4:] != ".csv":
            mb.showwarning("Warning",
                           "The Gephi algorithm expects in input a csv file.\n\nPlease, select a csv file and try again.")
            return
    reset_button.config(state='normal')
    if dynamic_network_field_var.get() != '':
        OK_button.config(state='normal')
    if csv_field_var.get() != '':
        select_csv_field_menu.config(state='disabled')
        # add_button.config(state='normal')
        OK_button.config(state='normal')
        add_button.config(state='disabled')
        if comingFrom_Plus == True:
            OK_button.config(state='disabled')
            if len(csv_file_field_list) == 3:
                select_csv_field_menu.configure(state='disabled')
                dynamic_network_field_menu.config(state='normal')
            else:
                select_csv_field_menu.configure(state='normal')
                dynamic_network_field_menu.config(state='disabled')
        if comingFrom_OK == True or len(csv_file_field_list) == 4:
            select_csv_field_menu.configure(state='disabled')
            add_button.config(state='normal') # RF
            OK_button.config(state='disabled')
            select_csv_field_menu.configure(state='disabled')
        if dynamic_network_field_var.get() != '':
            OK_button.config(state='normal')
    else:
        select_csv_field_menu.config(state='normal')
        reset_button.config(state='disabled')

    # clear content of current variables when selecting a different main option
    # csv_file_field_list.clear()

Gephi_var.trace('w', callback = lambda x,y,z: activate_csv_fields_selection(False,False))
csv_field_var.trace('w', callback = lambda x,y,z: activate_csv_fields_selection(False,False))
dynamic_network_field_var.trace('w', callback = lambda x,y,z: activate_csv_fields_selection(False,False))

def display_selected_csv_fields(comingFrom_OK,comingFrom_Plus):
    if csv_field_var.get() != '' and not csv_field_var.get() in csv_file_field_list:
        csv_file_field_list.append(csv_field_var.get())
    if dynamic_network_field_var.get() != '' and not dynamic_network_field_var.get() in csv_file_field_list:
        csv_file_field_list.append(dynamic_network_field_var.get())
    selected_csv_file_fields_var.set(str(csv_file_field_list))
    activate_csv_fields_selection(comingFrom_Plus, comingFrom_OK)

def reset():
    csv_file_field_list.clear()
    csv_field_var.set('')
    dynamic_network_field_var.set('')
    selected_csv_file_fields_var.set('')

videos_lookup = {'No videos available':''}
videos_options='No videos available'

TIPS_lookup = {"Lemmas & stopwords":"TIPS_NLP_NLP Basic Language.pdf",
               "Word clouds":"TIPS_NLP_Wordclouds Visualizing word clouds.pdf",
               "Wordle":"TIPS_NLP_Wordclouds Wordle.pdf",
               "Tagxedo":"TIPS_NLP_Wordclouds Tagxedo.pdf",
               "Tagcrowd":"TIPS_NLP_Wordclouds Tagcrowd.pdf",
               'Excel charts': 'TIPS_NLP_Excel Charts.pdf',
               'Excel smoothing data series': 'TIPS_NLP_Excel smoothing data series.pdf',
                'Network Graphs (via Gephi)': 'TIPS_NLP_Gephi network graphs.pdf',
               'csv files - Problems & solutions': 'TIPS_NLP_csv files - Problems & solutions.pdf',
               'Statistical measures': 'TIPS_NLP_Statistical measures.pdf'}

TIPS_options='Lemmas & stopwords', 'Word clouds', 'Tagcrowd', 'Tagxedo', 'Wordle', 'Excel smoothing data series', 'Network Graphs (via Gephi)', 'csv files - Problems & solutions', 'Statistical measures'

# add all the lines to the end to every special GUI
# change the last item (message displayed) of each line of the function y_multiplier_integer = help_buttons
# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util.
def help_buttons(window,help_button_x_coordinate,y_multiplier_integer):
    resetAll = "\n\nPress the RESET button to clear all selected values, and start fresh."
    plusButton = "\n\nPress the + buttons, when available, to add a new field."
    OKButton = "\n\nPress the OK button, when available, to accept the selections made, then press the RUN button to process the query."
    if not IO_setup_display_brief:
        y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",GUI_IO_util.msg_CoNLL)
        y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",GUI_IO_util.msg_corpusData)
        y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",GUI_IO_util.msg_outputDirectory)
    else:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_IO_setup)

    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help","Please, click on the button to open the Excel GUI.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help","Please, click on the button to open the GIS GUI.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help","Please, click on the button to open the HTML annotator GUI.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help","Please, click on the button to open the wordcloud GUI.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help","Please, tick the checkbox if you wish to visualize a network graph in Gephi.\n\nOptions become available in succession.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help","\n\nOptions become available in succession.\n\nThe first field selected is the first node; the second field selected is the edge; the third field selected is the second node.\n\nOnce all three fields have been selected, the widget 'Field to be used for dynamic network graphs' will become available. When available, select a field to be used for dynamic networks (e.g., the Sentence ID) or ignore the option if the network should not be dynamic." + plusButton + OKButton + resetAll)
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help","\n\nThe widget is always disabled; it is for display only. When pressing OK, the selected csv fields will be displayed." + plusButton + OKButton + resetAll)
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",GUI_IO_util.msg_openOutputFiles)
    return y_multiplier_integer -1
y_multiplier_integer = help_buttons(window,GUI_IO_util.get_help_button_x_coordinate(),0)

# change the value of the readMe_message
readMe_message="The Python 3 script and online services display the content of text files as word cloud.\n\nA word cloud, also known as text cloud or tag cloud, is a collection of words depicted visually in different sizes (and colors). The bigger and bolder the word appears, the more often it’s mentioned within a given text and the more important it is.\n\nDifferent, freeware, word cloud applications are available: 'TagCrowd', 'Tagul', 'Tagxedo', 'Wordclouds', and 'Wordle'. These applications require internet connection.\n\nThe script also provides Python word clouds (via Andreas Mueller's Python package WordCloud https://amueller.github.io/word_cloud/) for which no internet connection is required."
readMe_command = lambda: GUI_IO_util.display_help_button_info("NLP Suite Help", readMe_message)
GUI_util.GUI_bottom(config_filename, config_input_output_numeric_options, y_multiplier_integer, readMe_command, videos_lookup, videos_options, TIPS_lookup, TIPS_options, IO_setup_display_brief, scriptName)

GUI_util.window.mainloop()
