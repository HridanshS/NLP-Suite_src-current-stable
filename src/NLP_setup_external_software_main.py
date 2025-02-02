import tkinter as tk
import os
import webbrowser
import time
import tkinter.messagebox as mb

import GUI_IO_util
import GUI_util
import IO_libraries_util
import config_util
import IO_files_util

# RUN section ______________________________________________________________________________________________________________________________________________________

# There are no commands in the NLP_setup_package_language_main GUI

# GUI section ______________________________________________________________________________________________________________________________________________________

IO_setup_display_brief=True
GUI_size, y_multiplier_integer, increment = GUI_IO_util.GUI_settings(IO_setup_display_brief,
                                                 GUI_width=GUI_IO_util.get_GUI_width(1),
                                                 GUI_height_brief=300, # height at brief display
                                                 GUI_height_full=340, # height at full display
                                                 y_multiplier_integer=GUI_util.y_multiplier_integer,
                                                 y_multiplier_integer_add=1, # to be added for full display
                                                 increment=1)  # to be added for full display

GUI_label = 'Graphical User Interface (GUI) for setting up external software used in the NLP Suite (e.g., Stanford CoreNLP, Gephi)'
config_filename = 'NLP_setup_external_software_config.csv'
head, scriptName = os.path.split(os.path.basename(__file__))

config_input_output_numeric_options=[0,0,0,0]

GUI_util.set_window(GUI_size, GUI_label, config_filename, config_input_output_numeric_options)
GUI_util.GUI_top(config_input_output_numeric_options,config_filename,IO_setup_display_brief)
window = GUI_util.window

software_download_var = tk.StringVar()
software_install_var = tk.StringVar()
y_multiplier_integer=0

missing_software_lb = tk.Label(window,text='Missing external software')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(),
                                               y_multiplier_integer, missing_software_lb, True)

y_multiplier_integer_SV=y_multiplier_integer

missing_software_var = tk.StringVar()

missing_software_display_area = tk.Entry(width=80, state='disabled', textvariable=missing_software_var)
y_multiplier_integer = GUI_IO_util.placeWidget(window, GUI_IO_util.website_url_placement,
                                               y_multiplier_integer, missing_software_display_area, True)

# software_dir, missing_external_software = IO_libraries_util.get_external_software_dir(scriptName, software_download_var.get(), True, True)
#
# if missing_external_software=='':
#     missing_software_var.set('All external software has been installed')
#     error = False
# else:
#     # must be displayed at the end after the whole GUI has been laid
#     error = True
#     missing_software_var.set(missing_external_software)

# missing_software_display_area = tk.Label(width=80, height=1, anchor='w', text=str(missing_external_software), state='disabled')
# y_multiplier_integer = GUI_IO_util.placeWidget(window, GUI_IO_util.get_open_file_directory_coordinate() + 100,
#                                                y_multiplier_integer_SV, missing_software_display_area, True)

def openConfigFile():
    IO_files_util.openFile(window, GUI_IO_util.configPath + os.sep + config_filename)
    time.sleep(10) # wait 10 seconds to give enough time to save any changes to the csv config file

openInputConfigFile_button = tk.Button(window, width=GUI_IO_util.open_file_directory_button_width, text='',
                                 command=lambda: openConfigFile())
# place widget with hover-over info
x_coordinate_hover_over=1150
y_multiplier_integer = GUI_IO_util.placeWidget(window,x_coordinate_hover_over, y_multiplier_integer,
                                               openInputConfigFile_button, False, False, True,False, 90, x_coordinate_hover_over-100, "Open csv config file")

software_download_lb = tk.Label(window,text='Software download & install')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(),
                                               y_multiplier_integer, software_download_lb, True)
software_download_var.set('')
software_download_menu = tk.OptionMenu(window, software_download_var, '*','Stanford CoreNLP', 'Gephi','Google Earth Pro','MALLET','SENNA','WordNet')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+200,
                                               y_multiplier_integer, software_download_menu,True)

software_website = tk.Label(height=1, anchor='w', text='Website url')
y_multiplier_integer = GUI_IO_util.placeWidget(window, GUI_IO_util.website_url_placement,
                                               y_multiplier_integer, software_website, True)

software_website_url_var=tk.StringVar()
software_website_display_area = tk.Entry(width=80, state='disabled', textvariable=software_website_url_var)
y_multiplier_integer = GUI_IO_util.placeWidget(window, GUI_IO_util.website_url_placement,
                                               y_multiplier_integer, software_website_display_area, True)

error = False
def activate_software_website(*args):
    software_website_url=''
    if 'CoreNLP' in software_download_var.get():
        software_website_url="https://stanfordnlp.github.io/CoreNLP/download.html"
    if 'Gephi' in software_download_var.get():
        software_website_url="https://gephi.org/users/download/"
    if 'MALLET' in software_download_var.get():
        software_website_url="http://mallet.cs.umass.edu/download.php"
    if 'SENNA' in software_download_var.get():
        software_website_url= "https://ronan.collobert.com/senna/download.html"
    if 'WordNet' in software_download_var.get():
        software_website_url="https://wordnet.princeton.edu/download/current-version"
    software_website_url_var.set(software_website_url)

    software_dir, missing_software = IO_libraries_util.get_external_software_dir(scriptName, software_download_var.get(), False,
                                                                                 False, True)
software_download_var.trace('w',activate_software_website)


def openWebsite(software_website_url):
    webbrowser.open_new_tab(software_website_url)

openWebsite_button = tk.Button(window, width=GUI_IO_util.open_file_directory_button_width, text='',
                                 command=lambda: openWebsite(software_website_url_var.get()))
# place widget with hover-over info
x_coordinate_hover_over=1150
y_multiplier_integer = GUI_IO_util.placeWidget(window,x_coordinate_hover_over, y_multiplier_integer,
                                               openWebsite_button, False, False, True,False, 90, x_coordinate_hover_over-100, "Open software website")

def save_external_software_config(parsers):
    # config_util.save_NLP_package_language_config(window, currently_selected_package_language, parsers_display_area['text'])
    config_util.save_external_software_config_config(window)

save_button = tk.Button(window, text='SAVE', width=10, height=2, command=lambda: save_external_software_config(parsers))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.close_button_x_coordinate,
                                               y_multiplier_integer, save_button)
videos_lookup = {'No videos available':''}
videos_options='No videos available'

TIPS_lookup = {'Setup INPUT-OUTPUT options':'TIPS_NLP_Setup INPUT-OUTPUT options.pdf'}
TIPS_options='Setup INPUT-OUTPUT options'

# add all the lines to the end to every special GUI
# change the last item (message displayed) of each line of the function y_multiplier_integer = help_buttons
# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util.
def help_buttons(window, help_button_x_coordinate, y_multiplier_integer):
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "The text widget displays the external software that has not been installed yet in the NLP Suite. All missing software will need to be downloaded/installed or some functionality will be lost for some of the scripts (e.g., you cannot do any textual analysis of any kind without spaCy, Stanford CoreNLP, or Stanza or produce any geographic maps without Google Earth Pro).\n\nClick on the button to the far right to open the config file for inspection."+GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "Please, using the dropdown menu, select the external software that you wish to download/install."+GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "Please, hit the SAVE button to save any changes made.")
    y_multiplier_integer = 4.5
    return y_multiplier_integer-1

y_multiplier_integer = help_buttons(window, GUI_IO_util.get_help_button_x_coordinate(), 0)

# change the value of the readMe_message
readMe_message = "This Python 3 script provides a front-end GUI (Graphical User Interface) for setting up the default NLP package (e.g., Stanford CoreNLP, Stanza) and language (e.g., English, Chinese) to be used for parsing and annotating your corpus in a specific language. Different packages support different sets of languages."
readMe_command = lambda: GUI_IO_util.display_help_button_info("NLP Suite Help", readMe_message)
GUI_util.GUI_bottom(config_filename, config_input_output_numeric_options, y_multiplier_integer, readMe_command, videos_lookup, videos_options, TIPS_lookup, TIPS_options, True, scriptName, False)

software_dir, missing_software = IO_libraries_util.get_external_software_dir(scriptName, software_download_var.get(), True,
                                                                             True, True)
missing_external_software=missing_software.replace('\n\n','')

if missing_external_software == '':
    missing_software_var.set('All external software has been installed')
    error = False
else:
    # must be displayed at the end after the whole GUI has been laid
    error = True
    missing_software_var.set(missing_external_software)

software_dir, missing_software = IO_libraries_util.get_external_software_dir(scriptName, software_download_var.get(), False,
                                                                             False, True)
if missing_software!="":
    mb.showwarning(title='Warning',
                   message='The following external software has not been installed in the NLP Suite:\n\n' + str(missing_external_software) + '\n\nSome of the algorithms that require the software will not run.\n\nPlease, using the dropdown menu Software download & install, select the software to download/install.')

GUI_util.window.mainloop()
