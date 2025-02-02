"""
TWO STEPS ARE INVOLVED
STEP ONE: IMPORT YOUR CORPUS
    COMMAND: bin\\mallet import-dir --input folder\\files --output tutorial.mallet --keep-sequence --remove-stopwords

    Here, we tell MALLET to import all the TXT files of your corpus and to create a single Mallet-formatted file in output
    Parameter: --keep-sequence keep the original texts in the order in which they were listed;
    Parameter: --remove-stopwords strip out the stop words (words such as and, the, but, and if that occur in such frequencies that they obstruct analysis) using the default English stop-words dictionary.
    INPUT: all TXT files of your corpus
    OUTPUT: (tutorial.mallet) a single Mallet-formatted file containing all TXT input files

STEP TWO
    COMMAND: bin\\mallet train-topics  --input tutorial.mallet --num-topics 20 --output-state topic-state.gz --output-topic-keys tutorial_keys.txt --output-doc-topics tutorial_compostion.txt
    Here, we tell MALLET to create a topic model (train-topics) and everything with a double hyphen afterwards sets different parameters

    This Command trains MALLET to find 20 topics
       INPUT: the output file from STEP ONE (your tutorial.mallet file)
       OUTPUT (.gz): a .gz compressed file containing every word in your corpus of materials and the topic it belongs to (.gz; see www.gzip.org on how to unzip this)
       OUTPUT (KEYS): a CSV or TXT document (tutorial_keys.txt) showing you what the top key words are for each topic
       OUTPUT (COMPOSITION): a CSV or TXT  file (tutorial_composition.txt) indicating the breakdown, by percentage, of each topic within each original text file you imported.
           To see the full range of possible parameters that you may want to tweak, type bin\\mallet train-topics ?help at the prompt

All OUTPUT file names can be changed and Mallet will still run successfully
 OUTPUT file names extensions for step two can be TXT or CSV
"""
import sys
import GUI_util
import IO_libraries_util

if not IO_libraries_util.install_all_packages(GUI_util.window, "Mallet Topic modeling",
                                              ['os', 'tkinter.messagebox', 'subprocess']):
    sys.exit(0)

import os
import tkinter as tk
import tkinter.messagebox as mb
import subprocess
from subprocess import call
from sys import platform

import GUI_IO_util
import IO_files_util
import topic_modeling_mallet_util
import reminders_util


# RUN section __________________________________________________________________________________________________________

def run(inputDir, outputDir, openOutputFiles, createCharts, chartPackage, OptimizeInterval, numTopics):
    if numTopics == 20:
        reminders_util.checkReminder(config_filename, reminders_util.title_options_topic_modelling_number_of_topics,
                                     reminders_util.message_topic_modelling_number_of_topics, True)

    # create a subdirectory of the output directory
    outputDir = IO_files_util.make_output_subdirectory(inputFilename, inputDir, outputDir, label='TM-MALLET',
                                                       silent=False)
    if outputDir == '':
        return

    filesToOpen = topic_modeling_mallet_util.run(inputDir, outputDir, openOutputFiles, createCharts, chartPackage,
                                                 OptimizeInterval, numTopics)

    if openOutputFiles:
        IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir)


# the values of the GUI widgets MUST be entered in the command otherwise they will not be updated
def run_script_command(): return run(GUI_util.input_main_dir_path.get(),
                                     GUI_util.output_dir_path.get(),
                                     GUI_util.open_csv_output_checkbox.get(),
                                     GUI_util.create_chart_output_checkbox.get(),
                                     GUI_util.charts_dropdown_field.get(),
                                     optimize_intervals_var.get(),
                                     num_topics_var.get())


GUI_util.run_button.configure(command=run_script_command)

# GUI section __________________________________________________________________________________________________________

# the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)
#   just change the next statement to True or False IO_setup_display_brief=True
IO_setup_display_brief = True
GUI_size, y_multiplier_integer, increment = GUI_IO_util.GUI_settings(IO_setup_display_brief,
                                                                     GUI_width=GUI_IO_util.get_GUI_width(3),
                                                                     GUI_height_brief=320,  # height at brief display
                                                                     GUI_height_full=360,  # height at full display
                                                                     y_multiplier_integer=GUI_util.y_multiplier_integer,
                                                                     y_multiplier_integer_add=1,
                                                                     # to be added for full display
                                                                     increment=1)  # to be added for full display

GUI_label = 'Graphical User Interface (GUI) for Topic Modeling with Mallet'
head, scriptName = os.path.split(os.path.basename(__file__))
config_filename = scriptName.replace('main.py', 'config.csv')

# The 4 values of config_option refer to:
#   input file
#       1 for CoNLL file
#       2 for TXT file
#       3 for csv file
#       4 for any type of file
#       5 for txt or html
#       6 for txt or csv
#   input dir
#   input secondary dir
#   output dir
config_input_output_numeric_options = [0, 1, 0, 1]

GUI_util.set_window(GUI_size, GUI_label, config_filename, config_input_output_numeric_options)

window = GUI_util.window
config_input_output_numeric_options = GUI_util.config_input_output_numeric_options
config_filename = GUI_util.config_filename
inputFilename = GUI_util.inputFilename

GUI_util.GUI_top(config_input_output_numeric_options, config_filename, IO_setup_display_brief)

optimize_intervals_var = tk.IntVar()
num_topics_var = tk.IntVar()

num_topics_lb = tk.Label(window, text='Number of topics ')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               num_topics_lb, True)

num_topics_var.set(20)
num_topics_entry = tk.Entry(window, width=5, textvariable=num_topics_var)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_indented_coordinate() + 100,
                                               y_multiplier_integer, num_topics_entry)

optimize_intervals_var.set(1)
optimize_intervals_checkbox = tk.Checkbutton(window, text='Optimize topic intervals', variable=optimize_intervals_var,
                                             onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               optimize_intervals_checkbox)

videos_lookup = {'No videos available': ''}
videos_options = 'No videos available'

TIPS_lookup = {"Mallet installation":"TIPS_NLP_Topic modeling Mallet installation.pdf",
               'Excel - Enabling Macros': 'TIPS_NLP_Excel Enabling macros.pdf',
               'csv files - Problems & solutions':'TIPS_NLP_csv files - Problems & solutions.pdf',
               'Statistical measures': 'TIPS_NLP_Statistical measures.pdf',
               "Topic modeling in Mallet":"TIPS_NLP_Topic modeling Mallet.pdf",
               "Topic modeling in Gensim":"TIPS_NLP_Topic modeling Gensim.pdf",
               'Topic modeling and corpus size':'TIPS_NLP_Topic modeling and corpus size.pdf'}
#               "JAVA installation": "TIPS_NLP_Java download install run.pdf"}
TIPS_options='Topic modeling in Mallet','Mallet installation','Excel - Enabling Macros','csv files - Problems & solutions', 'Statistical measures', 'Topic modeling in Gensim','Topic modeling and corpus size'

# add all the lines to the end to every special GUI
# change the last item (message displayed) of each line of the function y_multiplier_integer = help_buttons
# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util.
def help_buttons(window, help_button_x_coordinate, y_multiplier_integer):
    if not IO_setup_display_brief:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_corpusData)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_outputDirectory)
    else:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_IO_setup)

    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer,
                                  "NLP Suite Help",
                                  "Please, tick the checkbox if you do NOT wish to optimize intervals.\n\n"
                                  "Optimization, however, seems to lead to better reults "
                                  "(https://programminghistorian.org/lessons/topic-modeling-and-mallet).")
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer,
                                  "NLP Suite Help",
                                  "Please, enter the number of topics to be used (recommended default = 20).\n\n"
                                  "Varying the number of topics may provide better results.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer,
                                  "NLP Suite Help", GUI_IO_util.msg_openOutputFiles)

    return y_multiplier_integer -1
y_multiplier_integer = help_buttons(window, GUI_IO_util.get_help_button_x_coordinate(), 0)

# change the value of the readMe_message
readMe_message = "This Python 3 script analyzes a set of documents for topic modeling with Mallet" \
                 "(https://mimno.github.io/Mallet/topics).\n\n" \
                 "MALLET CODE WILL BREAK IF INPUT AND/OR OUTPUT PATHS CONTAIN SPACES (I.E., BLANKS).\n\n" \
                 "In INPUT the script expects a set of text files stored in a directory.\n\n" \
                 "In OUTPUT, the script creates a set of four files:\n" \
                 "  MalletFormatted_TXTFiles.mallet\n" \
                 "  NLP-Mallet_Output_Keys.tsv\n  NLP-Mallet_Output_Composition\n" \
                 "  NLP-Mallet_Output_Compressed.gz.\n\n" \
                 "The 2 files of interest are:\n" \
                 "NLP-Mallet_Output_Keys.tsv\nNLP-Mallet_Output_Composition.\n\n" \
                 "The KEYS file has as many lines as specified topics and three columns:\n" \
                 "  TOPIC #,\n" \
                 "  WEIGHT OF TOPIC that measures the weight of the topic across all the documents,\n" \
                 "  KEY WORDS IN TOPIC that lists a set of typical words belonging to the topic.\n\n" \
                 "The COMPOSITION file has as many lines as documents analyzed (one document per line) and several " \
                 "columns:\n" \
                 "  column 1 (Document ID),\n" \
                 "  column 2 (Document with path),\n" \
                 "  as many successive pairs of columns as the number of topics, with column pairs as follow:\n" \
                 "    TOPIC is a number corresponding to the number in column 1 in the Keys file;\n" \
                 "PROPORTION measures the % of words in the document attributed to that topic (pairs sorted in " \
                 "descending PROPORTION order). "


readMe_command = lambda: GUI_IO_util.display_help_button_info("NLP Suite Help", readMe_message)

GUI_util.GUI_bottom(config_filename, config_input_output_numeric_options, y_multiplier_integer, readMe_command,
                    videos_lookup, videos_options, TIPS_lookup, TIPS_options, IO_setup_display_brief, scriptName)

reminders_util.checkReminder(
        config_filename,
        reminders_util.title_options_English_language_MALLET,
        reminders_util.message_English_language_MALLET,
        True)

GUI_util.window.mainloop()
