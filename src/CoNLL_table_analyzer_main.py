import sys
import GUI_util
import IO_libraries_util

if IO_libraries_util.install_all_packages(GUI_util.window, "CoNLL table_analyzer", ['os', 'tkinter','pandas']) == False:
    sys.exit(0)

import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import pandas as pd

import GUI_IO_util
import CoNLL_util
import CoNLL_table_search_util
import statistics_csv_util
import charts_util
import IO_files_util
import IO_csv_util
import IO_user_interface_util
import Stanford_CoreNLP_tags_util
import CoNLL_k_sentences_util
import reminders_util

# from data_manager_main import extract_from_csv

# more imports (e.g., import CoNLL_clause_analysis_util) are called below under separate if statements


# RUN section ______________________________________________________________________________________________________________________________________________________

# the values of the GUI widgets MUST be entered in the command otherwise they will not be updated
def run(inputFilename, outputDir, openOutputFiles, createCharts, chartPackage,
        searchedCoNLLField, searchField_kw, postag, deprel, co_postag, co_deprel,
        k_sentences_var,
        clausal_analysis_var,
        noun_analysis_var,
        verb_analysis_var,
        function_words_analysis_var):

    global recordID_position, documentId_position, data, all_CoNLL_records
    recordID_position = 9 # NEW CoNLL_U
    documentId_position = 11 # NEW CoNLL_U

    noResults = "No results found matching your search criteria for your input CoNLL file. Please, try different search criteria.\n\nTypical reasons for this warning are:\n   1.  You are searching for a token/word not found in the FORM or LEMMA fields (e.g., 'child' in FORM when in fact FORM contains 'children', or 'children' in LEMMA when in fact LEMMA contains 'child'; the same would be true for the verbs 'running' in LEMMA instead of 'run');\n   2. you are searching for a token that is a noun (e.g., 'children'), but you select the POS value 'VB', i.e., verb, for the POSTAG of searched token."
    filesToOpen = []  # Store all files that are to be opened once finished
    outputFiles = []

    if searchField_kw == 'e.g.: father':
        if not compute_sentence_var.get() and not extract_var.get():
            if clausal_analysis_var==False and noun_analysis_var==False and verb_analysis_var==False and function_words_analysis_var==False and k_sentences_var==False:
                mb.showwarning(title='No option selected',
                           message="No option has been selected. The 'Searched token' field must be different from 'e.g.: father' or you must select at least one of analyses on the right-hand side.\n\nPlease, select an option and try again.")
                return  # breaks loop

    withHeader = True
    data, header = IO_csv_util.get_csv_data(inputFilename, withHeader)
    if len(data) == 0:
        return
    all_CoNLL_records = CoNLL_util.CoNLL_record_division(data)
    if all_CoNLL_records == None:
        return
    if len(all_CoNLL_records) == 0:
        return

    right_hand_side = False

    if compute_sentence_var.get():
        tempOutputFile = CoNLL_util.compute_sentence_table(inputFilename, outputDir)
        filesToOpen.append(tempOutputFile)

    if extract_var.get():
        df = pd.read_csv(inputFilename, encoding='utf-8', error_bad_lines=False)
        data_files = [df]
        # print(csv_file_field_list)
        # outputFiles: list = IO_csv_util.extract_from_csv(path=[inputFilename], output_path=outputDir, data_files=data_files,
        #                                          csv_file_field_list=csv_file_field_list)
        outputFiles: list = IO_csv_util.extract_from_csv(inputFilename,outputDir, data_files,csv_file_field_list)
        if outputFiles != None:
            filesToOpen.append(outputFiles)

    if k_sentences_var:
        outputFiles = CoNLL_k_sentences_util.k_sent(inputFilename,outputDir)
        if outputFiles != None:
            filesToOpen.append(outputFiles)

    if clausal_analysis_var or noun_analysis_var or verb_analysis_var or function_words_analysis_var:
        startTime=IO_user_interface_util.timed_alert(GUI_util.window,2000,'Analysis start', 'Started running CoNLL table analyses at',
                                                     True, '', True, '', False)

    if clausal_analysis_var:
        import CoNLL_clause_analysis_util
        outputFiles = CoNLL_clause_analysis_util.clause_stats(inputFilename, '', outputDir,
                                                              data,
                                                              all_CoNLL_records,
                                                              openOutputFiles, createCharts,chartPackage)
        if outputFiles != None:
            filesToOpen.extend(outputFiles)

        right_hand_side = True

    if noun_analysis_var:
        import CoNLL_noun_analysis_util
        outputFiles = CoNLL_noun_analysis_util.noun_stats(inputFilename, outputDir, data, all_CoNLL_records,
                                                          openOutputFiles, createCharts, chartPackage)
        if outputFiles != None:
            filesToOpen.extend(outputFiles)

        right_hand_side = True

    if verb_analysis_var == True:
        import CoNLL_verb_analysis_util

        outputFiles = CoNLL_verb_analysis_util.verb_stats(config_filename, inputFilename, outputDir, data, all_CoNLL_records,
                                                          openOutputFiles, createCharts, chartPackage)

        if outputFiles != None:
            filesToOpen.extend(outputFiles)

        right_hand_side = True

    if function_words_analysis_var == True:
        import CoNLL_function_words_analysis_util

        outputFiles = CoNLL_function_words_analysis_util.function_words_stats(inputFilename, outputDir, data,
                                                                              all_CoNLL_records, openOutputFiles,
                                                                              createCharts, chartPackage)
        if outputFiles != None:
            filesToOpen.extend(outputFiles)

        right_hand_side = True

    if right_hand_side == True:
        if clausal_analysis_var or noun_analysis_var or verb_analysis_var or function_words_analysis_var:
            IO_user_interface_util.timed_alert(GUI_util.window,2000,'Analysis end',
                                               'Finished running CoNLL table analyses at',
                                               True, '', True, startTime, False)
        if openOutputFiles == True:
            IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir)
        filesToOpen = []  # Store all files that are to be opened once finished
        outputFiles = []
        return

# left-hand side SEARCH
    if searchField_kw != 'e.g.: father':
        # # create a subdirectory of the output directory
        # outputDir = IO_files_util.make_output_subdirectory(inputFilename, '', outputDir, label='CoNLL_search',
        #                                                    silent=True)

        if ' ' in searchField_kw:
            mb.showwarning(title='Search error',
                           message="The CoNLL table search can only contain one token/word since the table has one record for each token/word.\n\nPlease, enter a different word and try again.\n\nIf you need to search your corpus for collocations, i.e., multi-word expressions, you need to use the 'N-grams/Co-occurrence searches' or the 'Words/collocations searches' in the ALL searches GUI.")
            return
        if searchedCoNLLField.lower() not in ['lemma', 'form']:
            searchedCoNLLField = 'FORM'
        if postag != '*':
            postag = str(postag).split(' - ')[0]
            postag = postag.strip()
        else:
            postag = '*'
        if deprel != '*':
            deprel = str(deprel).split(' - ')[0]
            deprel = deprel.strip()
        else:
            deprel = '*'
        if co_postag != '*':
            co_postag = str(co_postag).split(' - ')[0]
            co_postag = co_postag.strip()
        else:
            co_postag = '*'
        if co_deprel != '*':
            co_deprel = str(co_deprel).split(' - ')[0]
            co_deprel = co_deprel.strip()
        else:
            co_deprel = '*'

        if (not os.path.isfile(inputFilename.strip())) and \
                ('CoNLL' not in inputFilename) and \
                (not inputFilename.strip()[-4:] == '.csv'):
            mb.showwarning(title='INPUT File Path Error',
                           message='Please, check INPUT FILE PATH and try again. The file must be a CoNLL table (extension .conll with Stanford CoreNLP no clausal tags, extension .csv with Stanford CoreNLP with clausal tags)')
            return
        if 'e.g.: father' in searchField_kw:
            msg = "Please, check the \'Searched token\' field and try again.\n\nThe value entered must be different from the default value (e.g.: father)."
            mb.showwarning(title='Searched Token Input Error', message=msg)
            return  # breaks loop
        if len(searchField_kw) == 0:
            msg = "Please, check the \'Searched token\' field and try again.\n\nThe value entered must be different from blank."
            mb.showwarning(title='Searched Token Input Error', message=msg)
            return  # breaks loop

        startTime=IO_user_interface_util.timed_alert(GUI_util.window,2000,'Analysis start', 'Started running CoNLL search at',
                                                     True, '', True, '', True)

        withHeader = True
        data, header = IO_csv_util.get_csv_data(inputFilename, withHeader)

        if len(data) <= 1000000:
            try:
                data = sorted(data, key=lambda x: int(x[recordID_position]))
            except:
                mb.showwarning(title="CoNLLL table ill formed",
                               message="The CoNLL table is ill formed. You may have tinkered with it. Please, rerun the Stanford CoreNLP parser since many scripts rely on the CoNLL table.")
                return

        # if len(data) == 0:
        #     return
        # all_CoNLL_records = CoNLL_util.sentence_division(data)
        # if len(all_CoNLL_records) == 0:
        #     return
        queried_list = CoNLL_table_search_util.search_CoNLL_table(all_CoNLL_records, searchField_kw, searchedCoNLLField,
                                                                  related_token_POSTAG=co_postag,
                                                                  related_token_DEPREL=co_deprel, _tok_postag_=postag,
                                                                  _tok_deprel_=deprel)

        if len(queried_list) != 0:
            if searchField_kw == '*':
                srcField_kw = 'astrsk'
            else:
                srcField_kw = searchField_kw
            output_file_name = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv', 'QC',
                                                                       srcField_kw, searchedCoNLLField)

            # convert list to dataframe and save
            df = pd.DataFrame(queried_list)
            # headers=['list_queried, related_token_DEPREL, Sentence_ID, related_token_POSTAG']
            IO_csv_util.df_to_csv(GUI_util.window, df, output_file_name, headers=None, index=False,
                                  language_encoding='utf-8')

            filesToOpen.append(output_file_name)

            """
            The 15 indexed items are created in the function query_the_table:
                item[0] form/lemma, item[1] postag, item[2] deprel, item[3] is_head, item[4] Document_ID, 
                item[5] Sentence_ID, item[6] Document, item[7] whole_sent, 
                item[8] keyword[1]/SEARCHED TOKEN, 
                item[9] keyword[3]/SEARCHED TOKEN POSTAG, 
                item[10] keyword[6]/'SEARCHED TOKEN DEPREL'))
            """
            # if createCharts == True:
            #
            #     columns_to_be_plotted_xAxis=[], columns_to_be_plotted_yAxis=[[0,1]]
            #     count_var=1
            #
            #     chart_outputFilename = charts_util.run_all(columns_to_be_plotted, output_file_name, outputDir,
            #                             outputFileLabel='QueryCoNLL_POS (' + searchField_kw + ')',
            #                             chartPackage=chartPackage,
            #                             chart_type_list=['bar'],
            #                             chart_title="Frequency of Searched Token POS Tags",
            #                             column_xAxis_label_var='Searched token POS tag',
            #                             hover_info_column_list=[],
            #                             count_var=count_var,
            #                             complete_sid=False)  # TODO to be changed
            #
            #     if chart_outputFilename != None:
            #         filesToOpen.append(chart_outputFilename)
            #
                # output_file_name_xlsx = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.xlsx', 'QC',
                #                                                                 'kw_deprel', 'stats_pie_chart')
                # column_stats = statistics_csv_util.compute_statistics_CoreNLP_CoNLL_tag(queried_list, 10,
                #                                                              "Searched token Deprel values (" + searchField_kw + ")",
                #                                                              "DEPREL")
                # errorFound = IO_csv_util.list_to_csv(GUI_util.window, column_stats, output_file_name_xlsx)
                # if errorFound == True:
                #     return
                #
                # chart_outputFilename = charts_util.run_all(columns_to_be_plotted, output_file_name, outputDir,
                #                         outputFileLabel='QueryCoNLL_DepRel (' + searchField_kw + ')',
                #                         chartPackage=chartPackage,
                #                         chart_type_list=['bar'],
                #                         chart_title="Frequency of Searched Token DepRel Tags",
                #                         column_xAxis_label_var='Searched token DepRel tag',
                #                         hover_info_column_list=[],
                #                         count_var=count_var)
                # filesToOpen.append(chart_outputFilename)
                #
                # output_file_name_xlsx = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.xlsx', 'QC',
                #                                                                 'co_kw_postag', 'stats_pie_chart')
                # column_stats = statistics_csv_util.compute_statistics_CoreNLP_CoNLL_tag(queried_list, 1,
                #                                                              "Co-token Postag values (" + searchField_kw + ")",
                #                                                              "POSTAG")
                # errorFound = IO_csv_util.list_to_csv(GUI_util.window, column_stats, output_file_name)
                # if errorFound == True:
                #     return
                # chart_outputFilename = charts_util.run_all(columns_to_be_plotted, output_file_name, outputDir,
                #                         outputFileLabel='QueryCoNLL_CoOcc_POS (' + searchField_kw + ')',
                #                         chartPackage=chartPackage,
                #                         chart_type_list=['bar'],
                #                         chart_title="Frequency of Searched Token Co-occurring POS Tags",
                #                         column_xAxis_label_var='Searched token CoOcc_POS tag',
                #                         hover_info_column_list=[],
                #                         count_var=count_var)
                # filesToOpen.append(chart_outputFilename)
                #
                # output_file_name_xlsx = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.xlsx', 'QC',
                #                                                                 'co_kw_deprel', 'stats_pie_chart')
                # column_stats = statistics_csv_util.compute_statistics_CoreNLP_CoNLL_tag(queried_list, 2,
                #                                                              "Co-token Deprel values (" + searchField_kw + ")",
                #                                                              "DEPREL")
                # errorFound = IO_csv_util.list_to_csv(GUI_util.window, column_stats, output_file_name_xlsx)
                # if errorFound:
                #     return
                #
                # chart_outputFilename = charts_util.run_all(columns_to_be_plotted, output_file_name, outputDir,
                #                         outputFileLabel='QueryCoNLL_CoOcc_DEP (' + searchField_kw + ')',
                #                         chartPackage=chartPackage,
                #                         chart_type_list=['bar'],
                #                         chart_title="Frequency of Searched Token Co-Occurring DepRel Tags",
                #                         column_xAxis_label_var='Searched token CoOcc_DEP tag',
                #                         hover_info_column_list=[],
                #                         count_var=count_var)
                # filesToOpen.append(chart_outputFilename)
            IO_user_interface_util.timed_alert(GUI_util.window,2000,'Analysis end',
                                               'Finished running CoNLL search at', True, '', True, startTime)

            # if openOutputFiles:
            #     IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen)

            # # Gephi network graphs _________________________________________________
            # TODO
            # the CoNLL table search can export a word and related words in a variety of relations to the word (by POS DEPREL etc.)
            # ideally, these sets of related words can be visualized in a network graph in Gephi
            # But... Gephi has been hard coded for SVO, since it has only been used for that so far, but any 2 or 3-terms can be visualized as a network
            # Furthermore, if we cant to create dynamic models that vary ov ertime, wehere we use the sentence index as a proxy for time, we need to pass that variable as well (the saentence index)
            # create_gexf would need to read in the proper column names, rather than S V OA
            # outputFileBase = os.path.basename(output_file_name)[0:-4] # without .csv or .txt
            # gexf_file = Gephi_util.create_gexf(outputFileBase, outputDir, output_file_name)
            # filesToOpen.append(gexf_file)

        else:
            mb.showwarning(title='Empty query results', message=noResults)

    if openOutputFiles:
        IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir)

run_script_command = lambda: run(GUI_util.inputFilename.get(),
                                 GUI_util.output_dir_path.get(),
                                 GUI_util.open_csv_output_checkbox.get(),
                                 GUI_util.create_chart_output_checkbox.get(),
                                 GUI_util.charts_dropdown_field.get(),
                                 searchedCoNLLField.get(),
                                 searchField_kw.get(),
                                 postag_var.get(),
                                 deprel_var.get(),
                                 co_postag_var.get(),
                                 co_deprel_var.get(),
                                 k_sentences_var.get(),
                                 clausal_analysis_var.get(),
                                 noun_analysis_var.get(),
                                 verb_analysis_var.get(),
                                 function_words_analysis_var.get())

GUI_util.run_button.configure(command=run_script_command)

# GUI section ______________________________________________________________________________________________________________________________________________________

# the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)
#   just change the next statement to True or False IO_setup_display_brief=True
IO_setup_display_brief=True
GUI_size, y_multiplier_integer, increment = GUI_IO_util.GUI_settings(IO_setup_display_brief,
                                                 GUI_width=GUI_IO_util.get_GUI_width(3),
                                                 GUI_height_brief=630, # height at brief display
                                                 GUI_height_full=670, # height at full display
                                                 y_multiplier_integer=GUI_util.y_multiplier_integer,
                                                 y_multiplier_integer_add=1, # to be added for full display
                                                 increment=1)  # to be added for full display

GUI_label = 'Graphical User Interface (GUI) for CoNLL Table Analyzer'
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
config_input_output_numeric_options=[1,0,0,1]

GUI_util.set_window(GUI_size, GUI_label, config_filename, config_input_output_numeric_options)

window = GUI_util.window
# config_input_output_numeric_options = GUI_util.config_input_output_numeric_options
# config_filename = GUI_util.config_filename
inputFilename = GUI_util.inputFilename

GUI_util.GUI_top(config_input_output_numeric_options, config_filename,IO_setup_display_brief)

searchField_kw = tk.StringVar()
searchedCoNLLField = tk.StringVar()
postag_var = tk.StringVar()
deprel_var = tk.StringVar()
co_postag_var = tk.StringVar()
co_postag_var = tk.StringVar()
co_deprel_var = tk.StringVar()
SVO_var = tk.IntVar()
k_sentences_var = tk.IntVar()
csv_file_field_list = []

clausal_analysis_var = tk.IntVar()

noun_analysis_var = tk.IntVar()
verb_analysis_var = tk.IntVar()
function_words_analysis_var = tk.IntVar()

compute_sentence_var = tk.IntVar()

extract_var = tk.IntVar()
selected_fields_var = tk.StringVar()
select_csv_field_extract_var = tk.StringVar()


all_analyses_var = tk.IntVar()

buildString = ''
menu_values = []
error = False

postag_menu = '*', 'JJ* - Any adjective', 'NN* - Any noun', 'VB* - Any verb', *sorted([k + " - " + v for k, v in Stanford_CoreNLP_tags_util.dict_POSTAG.items()])
deprel_menu = '*', *sorted([k + " - " + v for k, v in Stanford_CoreNLP_tags_util.dict_DEPREL.items()])

def clear(e):
    searchField_kw.set('e.g.: father')
    postag_var.set('*')
    deprel_var.set('*')
    co_postag_var.set('*')
    co_postag_var.set('*')
    co_deprel_var.set('*')
    activate_options()
    activate_csv_fields_selection(extract_var.get(), False, False)
    reset_all_values()
    GUI_util.clear("Escape")


window.bind("<Escape>", clear)


# custom sorter to place non alpha strings later while custom sorting
def custom_sort(s):
    if s:
        if s[0].isalpha():
            return 0
        else:
            return 10
    else:
        return 10


searchToken_lb = tk.Label(window, text='Searched token')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(),
                                                    y_multiplier_integer, searchToken_lb,True)

searchField_kw.set('e.g.: father')

# used to place noun/verb checkboxes starting at the top level
y_multiplier_integer_top = y_multiplier_integer

entry_searchField_kw = tk.Entry(window, textvariable=searchField_kw)
# place widget with hover-over info
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + GUI_IO_util.combobox_position,
    y_multiplier_integer,
    entry_searchField_kw,
    False, False, False, False, 90, GUI_IO_util.get_labels_x_coordinate() + GUI_IO_util.combobox_position,
    "Enter the CASE SENSITIVE word that you would like to search (* for any word). All searches are done WITHIN EACH SENTENCE for the EXACT word.")

# Search type var (FORM/LEMMA)
searchedCoNLLField.set('FORM')
searchedCoNLLdescription_csv_field_menu_lb = tk.Label(window, text='CoNLL search field')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               searchedCoNLLdescription_csv_field_menu_lb,True)

searchedCoNLLdescription_csv_field_menu_lb = tk.OptionMenu(window, searchedCoNLLField, 'FORM', 'LEMMA')
searchedCoNLLdescription_csv_field_menu_lb.configure(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + GUI_IO_util.combobox_position, y_multiplier_integer,
                                               searchedCoNLLdescription_csv_field_menu_lb)

# POSTAG variable
postag_var.set('*')
POS_lb = tk.Label(window, text='POSTAG of searched token')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               POS_lb, True)

postag_menu_lb = ttk.Combobox(window, width = GUI_IO_util.combobox_width, textvariable = postag_var)
postag_menu_lb['values'] = postag_menu
postag_menu_lb.configure(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + GUI_IO_util.combobox_position, y_multiplier_integer,
                                               postag_menu_lb)

# DEPREL variable

deprel_var.set('*')
DEPREL_lb = tk.Label(window, text='DEPREL of searched token')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               DEPREL_lb, True)

deprel_menu_lb = ttk.Combobox(window, width = GUI_IO_util.combobox_width, textvariable = deprel_var)
deprel_menu_lb['values'] = deprel_menu
deprel_menu_lb.configure(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+GUI_IO_util.combobox_position, y_multiplier_integer,
                                               deprel_menu_lb)

# Co-Occurring POSTAG menu

co_postag_var.set('*')

POSTAG_CoOc_lb = tk.Label(window, text='POSTAG of co-occurring tokens')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               POSTAG_CoOc_lb, True)

co_postag_menu_lb = ttk.Combobox(window, width = GUI_IO_util.combobox_width, textvariable = co_postag_var)
co_postag_menu_lb['values'] = postag_menu
co_postag_menu_lb.configure(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+GUI_IO_util.combobox_position, y_multiplier_integer,
                                               co_postag_menu_lb)

co_deprel_menu = '*','acl - clausal modifier of noun (adjectival clause)', 'acl:relcl - relative clause modifier', 'acomp - adjectival complement', 'advcl - adverbial clause modifier', 'advmod - adverbial modifier', 'agent - agent', 'amod - adjectival modifier', 'appos - appositional modifier', 'arg - argument', 'aux - auxiliary', 'auxpass - passive auxiliary', 'case - case marking', 'cc - coordinating conjunction', 'ccomp - clausal complement with internal subject', 'cc:preconj - preconjunct','compound - compound','compound:prt - phrasal verb particle','conj - conjunct','cop - copula conjunction','csubj - clausal subject','csubjpass - clausal passive subject','dep - unspecified dependency','det - determiner','det:predet - predeterminer','discourse - discourse element','dislocated - dislocated element','dobj - direct object','expl - expletive','foreign - foreign words','goeswith - goes with','iobj - indirect object','list - list','mark - marker','mod - modifier','mwe - multi-word expression','name - name','neg - negation modifier','nn - noun compound modifier','nmod - nominal modifier','nmod:npmod - noun phrase as adverbial modifier','nmod:poss - possessive nominal modifier','nmod:tmod - temporal modifier','nummod - numeric modifier','npadvmod - noun phrase adverbial modifier','nsubj - nominal subject','nsubjpass - passive nominal subject','num - numeric modifier','number - element of compound number','parataxis - parataxis','pcomp - prepositional complement','pobj - object of a preposition','poss - possession modifier', 'possessive - possessive modifier','preconj - preconjunct','predet - predeterminer','prep - prepositional modifier','prepc - prepositional clausal modifier','prt - phrasal verb particle','punct - punctuation','quantmod - quantifier phrase modifier','rcmod - relative clause modifier','ref - referent','remnant - remnant in ellipsis','reparandum - overridden disfluency','ROOT - root','sdep - semantic dependent','subj - subject','tmod - temporal modifier','vmod - reduced non-finite verbal modifier','vocative - vocative','xcomp - clausal complement with external subject','xsubj - controlling subject','# - #'

co_deprel_var.set('*')
DEPREL_CoOc_lb = tk.Label(window, text='DEPREL of co-occurring tokens')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               DEPREL_CoOc_lb, True)

co_deprel_menu_lb = ttk.Combobox(window, width = GUI_IO_util.combobox_width, textvariable = co_deprel_var)
co_deprel_menu_lb['values'] = deprel_menu
co_deprel_menu_lb.configure(state='disabled')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate()+GUI_IO_util.combobox_position, y_multiplier_integer,co_deprel_menu_lb)

def reset_all_values():
    global buildString
    buildString = ''
    csv_file_field_list.clear()
    selected_fields_var.set('')

    extract_checkbox.config(state='normal')

    comparator_menu.configure(state="disabled")
    where_entry.configure(state="disabled")
    and_or_menu.configure(state="disabled")

    selected_fields_var.set('')

    where_entry_var.set("")
    comparator_var.set("")
    and_or_var.set("")

    select_csv_field_extract_menu.config(state='disabled')

    extract_var.set(0)


def changed_filename(tracedInputFile):
    global error
    if os.path.isfile(tracedInputFile):
        if not CoNLL_util.check_CoNLL(tracedInputFile):
            error = True
            return
        else:
            error = False
    menu_values = []
    if tracedInputFile != '':
        nRecords, nColumns = IO_csv_util.GetNumberOf_Records_Columns_inCSVFile(tracedInputFile)
        if nColumns == 0 or nColumns is None:
            return False
        if IO_csv_util.csvFile_has_header(tracedInputFile) == False:
            menu_values = range(1, nColumns + 1)
        else:
            data, headers = IO_csv_util.get_csv_data(tracedInputFile, True)
            menu_values = headers
    else:
        menu_values.clear()
        return
    m = select_csv_field_extract_menu["menu"]
    m.delete(0, "end")

    for s in menu_values:
        m.add_command(label=s, command=lambda value=s: select_csv_field_extract_var.set(value))
    clear("<Escape>")

GUI_util.inputFilename.trace('w', lambda x, y, z: changed_filename(GUI_util.inputFilename.get()))


compute_sentence_var.set(0)
sentence_table_checkbox = tk.Checkbutton(window, text='Compute sentence table', variable=compute_sentence_var,
                                         onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               sentence_table_checkbox)

extract_var.set(0)
extract_checkbox = tk.Checkbutton(window, text='Extract from CoNLL', variable=extract_var, onvalue=1,
                                  offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               extract_checkbox, True)

select_csv_field_lb = tk.Label(window, text='Select field')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + GUI_IO_util.combobox_position, y_multiplier_integer,
                                               select_csv_field_lb, True)

if len(menu_values) > 0:
    select_csv_field_extract_menu = tk.OptionMenu(window, select_csv_field_extract_var, *menu_values)
else:
    select_csv_field_extract_menu = tk.OptionMenu(window, select_csv_field_extract_var, menu_values)
select_csv_field_extract_menu.configure(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + GUI_IO_util.combobox_position+80, y_multiplier_integer,
                                               select_csv_field_extract_menu, True)

comparator_var = tk.StringVar()
comparator_menu = tk.OptionMenu(window, comparator_var, 'not equals', 'equals', 'greater than',
                                    'greater than or equals', 'less than', 'less than or equals')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 410, y_multiplier_integer,
                                               comparator_menu, True)

where_lb = tk.Label(window, text='WHERE')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 535, y_multiplier_integer,
                                               where_lb, True)

where_entry_var = tk.StringVar()
where_entry = tk.Entry(window, width=25, textvariable=where_entry_var)
where_entry.configure(state="disabled")
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 610, y_multiplier_integer,
                                               where_entry, True)

and_or_lb = tk.Label(window, text='and/or')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 790, y_multiplier_integer,
                                               and_or_lb, True)

and_or_var = tk.StringVar()
and_or_menu = tk.OptionMenu(window, and_or_var, 'and', 'or')
and_or_menu.configure(state="disabled")
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 840, y_multiplier_integer,
                                               and_or_menu, True)


def clear_csv_selections():
    select_csv_field_extract_var.set('')
    comparator_var.set('')
    and_or_var.set('')
    where_entry_var.set('')


def build_extract_string(comingFrom_Plus, comingFrom_OK):
    add_field_to_list(select_csv_field_extract_var.get(), comingFrom_OK)
    activate_csv_fields_selection(extract_var.get(), comingFrom_Plus, comingFrom_OK)
    clear_csv_selections()


add_extract_options_var = tk.IntVar()
add_extract_options = tk.Button(window, text='+', width=2, height=1, state='disabled',
                                command=lambda: build_extract_string(True, False))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 905, y_multiplier_integer,
                                               add_extract_options, True)

OK_extract_button = tk.Button(window, text='OK', width=3, height=1, state='disabled',
                              command=lambda: build_extract_string(False, True))
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 955, y_multiplier_integer,
                                               OK_extract_button, True)


def add_field_to_list(menu_choice, visualizeBuildString=True):
    global buildString
    # skip empty values and csv fields already selected
    if select_csv_field_extract_var.get() == '':
        return

    new_build_string = '"",' + menu_choice  # the first one is input file name, which is not used.

    if comparator_var.get() != '' and where_entry_var.get() == '':
        mb.showwarning(title='Warning',
                       message='You have selected the comparator value ' + comparator_var.get() + '\n\nYou MUST enter a WHERE value or press ESC to cancel.')
        return
    # always enter the value even if empty to ensure a similarly formatted string
    if comparator_var.get() != '':
        new_build_string = new_build_string + "," + comparator_var.get()
    else:
        new_build_string = new_build_string + "," + "''"
    if where_entry_var.get() != '':
        new_build_string = new_build_string + "," + where_entry_var.get()
    else:
        new_build_string = new_build_string + "," + "''"
    if and_or_var.get() != '':
        new_build_string = new_build_string + "," + and_or_var.get()
    else:
        new_build_string = new_build_string + "," + "''"
    csv_file_field_list.append(new_build_string)
    buildString = buildString + new_build_string


def show_values():
    mb.showwarning(title='Information', message=buildString)


show_button = tk.Button(window, width=7, text='Show', state='normal', command=lambda: show_values())
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 1005, y_multiplier_integer,
                                               show_button, True)

reset_all_button = tk.Button(window, width=6, text='Reset', state='normal', command=lambda: reset_all_values())
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 1075, y_multiplier_integer,
                                               reset_all_button)


def extractSelection(*args):
    # if extract_var.get():
    #     mb.showwarning(title='Warning',
    #                    message='The routine to extract fields an field values from the CoNLL table is under '
    #                            'construction.')
    activate_csv_fields_selection(extract_var.get(), False, False)


extract_var.trace('w', extractSelection)

SVO_var.set(0)
SVO_checkbox = tk.Checkbutton(window, text="Automatic extraction of Subject-Verb-Object from CoNLL table",
                              variable=SVO_var, onvalue=1, offvalue=0)
SVO_checkbox.configure(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               SVO_checkbox)

k_sentences_var.set(0)
k_sentences_checkbox = tk.Checkbutton(window, text="K sentences analyzer (repetition finder)",
                              variable=k_sentences_var, onvalue=1, offvalue=0)
# k_sentences_checkbox.configure(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,
                                               k_sentences_checkbox)

# Here rowspan=3 is necessary to make the separator span all 3 rows (the header, player 1 and player2).
# The sticky='ns' is there to stretch the separator from the top to the bottom of the window.
# Separators are only 1 pixel long per default, so without the sticky it would hardly be visible.
# tk.ttk.Separator(window, orient=tk.VERTICAL).grid(column=1, row=0, rowspan=3, sticky='ns')
# When you specify rowspan, it means that the widget will span its row and any rows below it
# ttk.Separator(window, orient=tk.VERTICAL).grid(column=1, row=0, rowspan=3, sticky='ns')
# without tk. VERTICAL is not defined; see GUI_IO_util slider_widget function
# ttk.Separator(window, orient=tk.VERTICAL).grid(row=0, column=1, rowspan=3)

# used to place noun/verb checkboxes starting at the bottom level
y_multiplier_integer_bottom = y_multiplier_integer

y_multiplier_integer = y_multiplier_integer_top

clausal_analysis_var.set(0)
clausal_analysis_checkbox = tk.Checkbutton(window, text='CLAUSE analyses', variable=clausal_analysis_var, onvalue=1,
                                           offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 610, y_multiplier_integer,
                                               clausal_analysis_checkbox)

noun_analysis_var.set(0)
noun_analysis_checkbox = tk.Checkbutton(window, text='NOUN analyses', variable=noun_analysis_var, onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 610, y_multiplier_integer,
                                               noun_analysis_checkbox)

verb_analysis_var.set(0)
verb_analysis_checkbox = tk.Checkbutton(window, text='VERB analyses', variable=verb_analysis_var, onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 610, y_multiplier_integer,
                                               verb_analysis_checkbox)

function_words_analysis_var.set(0)
function_words_analysis_checkbox = tk.Checkbutton(window, text='FUNCTION WORDS analyses',
                                                  variable=function_words_analysis_var, onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 610, y_multiplier_integer,
                                               function_words_analysis_checkbox)

all_analyses_var.set(0)
all_analyses_checkbox = tk.Checkbutton(window,
                                       text="ALL analyses: Clauses, nouns, verbs, function words ('junk/stop' words)",
                                       variable=all_analyses_var, onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.get_labels_x_coordinate() + 610, y_multiplier_integer,
                                               all_analyses_checkbox)

# -------------------------------------------------------------------------------------------------------

y_multiplier_integer = y_multiplier_integer_bottom


#
def activate_options(*args):
    global error
    # if there is an error everything is disabled
    if error:
        entry_searchField_kw.configure(state='disabled')
        searchedCoNLLdescription_csv_field_menu_lb.configure(state='disabled')
        postag_menu_lb.configure(state='disabled')
        deprel_menu_lb.configure(state='disabled')
        co_postag_menu_lb.configure(state='disabled')
        co_deprel_menu_lb.configure(state='disabled')
        all_analyses_checkbox.configure(state='disabled')
        clausal_analysis_checkbox.configure(state='disabled')
        noun_analysis_checkbox.configure(state='disabled')
        verb_analysis_checkbox.configure(state='disabled')
        function_words_analysis_checkbox.configure(state='disabled')

        sentence_table_checkbox.configure(state='disabled')
        extract_checkbox.configure(state='disabled')
        k_sentences_checkbox.configure(state='disabled')

        return

    entry_searchField_kw.configure(state='normal')

    all_analyses_checkbox.configure(state='normal')
    clausal_analysis_checkbox.configure(state='normal')
    noun_analysis_checkbox.configure(state='normal')
    verb_analysis_checkbox.configure(state='normal')
    function_words_analysis_checkbox.configure(state='normal')

    sentence_table_checkbox.configure(state='normal')
    extract_checkbox.configure(state='normal')
    k_sentences_checkbox.configure(state='normal')

    if searchField_kw.get() != 'e.g.: father':

        all_analyses_var.set(0)
        clausal_analysis_var.set(0)

        noun_analysis_var.set(0)
        verb_analysis_var.set(0)
        function_words_analysis_var.set(0)

        searchedCoNLLdescription_csv_field_menu_lb.configure(state='normal')
        postag_menu_lb.configure(state='normal')
        deprel_menu_lb.configure(state='normal')
        co_postag_menu_lb.configure(state='normal')
        co_deprel_menu_lb.configure(state='normal')

        all_analyses_checkbox.configure(state='disabled')
        clausal_analysis_checkbox.configure(state='disabled')
        noun_analysis_checkbox.configure(state='disabled')
        verb_analysis_checkbox.configure(state='disabled')
        function_words_analysis_checkbox.configure(state='disabled')
    else:
        searchedCoNLLdescription_csv_field_menu_lb.configure(state='disabled')
        postag_menu_lb.configure(state='disabled')
        deprel_menu_lb.configure(state='disabled')
        co_postag_menu_lb.configure(state='disabled')
        co_deprel_menu_lb.configure(state='disabled')

        all_analyses_checkbox.configure(state='normal')
        clausal_analysis_checkbox.configure(state='normal')
        noun_analysis_checkbox.configure(state='normal')
        verb_analysis_checkbox.configure(state='normal')
        function_words_analysis_checkbox.configure(state='normal')

        if all_analyses_var.get():
            reminders_util.checkReminder(config_filename,
                                         reminders_util.title_options_CoreNLP_nn_parser,
                                         reminders_util.message_CoreNLP_nn_parser,
                                         True)
            entry_searchField_kw.configure(state='disabled')

            clausal_analysis_var.set(1)
            noun_analysis_var.set(1)
            verb_analysis_var.set(1)
            function_words_analysis_var.set(1)

            searchedCoNLLdescription_csv_field_menu_lb.configure(state='disabled')
            postag_menu_lb.configure(state='disabled')
            deprel_menu_lb.configure(state='disabled')
            co_postag_menu_lb.configure(state='disabled')
            co_deprel_menu_lb.configure(state='disabled')

            clausal_analysis_checkbox.configure(state='normal')
            noun_analysis_checkbox.configure(state='normal')
            verb_analysis_checkbox.configure(state='normal')
            function_words_analysis_checkbox.configure(state='normal')
        else:
            entry_searchField_kw.configure(state='normal')
            clausal_analysis_var.set(0)
            noun_analysis_var.set(0)
            verb_analysis_var.set(0)
            function_words_analysis_var.set(0)


searchField_kw.trace('w', activate_options)
all_analyses_var.trace('w', activate_options)
#
#
activate_options()


#
def activate_CoNLL_options(*args):
    if clausal_analysis_var.get() == True or \
            noun_analysis_var.get() == True or \
            verb_analysis_var.get() == True or \
            function_words_analysis_var.get() == True:

        entry_searchField_kw.configure(state='disabled')
        searchedCoNLLdescription_csv_field_menu_lb.configure(state='disabled')
        postag_menu_lb.configure(state='disabled')
        deprel_menu_lb.configure(state='disabled')
        co_postag_menu_lb.configure(state='disabled')
        co_deprel_menu_lb.configure(state='disabled')
    else:
        entry_searchField_kw.configure(state='normal')
        searchedCoNLLdescription_csv_field_menu_lb.configure(state='normal')
        postag_menu_lb.configure(state='normal')
        deprel_menu_lb.configure(state='normal')
        co_postag_menu_lb.configure(state='normal')
        co_deprel_menu_lb.configure(state='normal')

    if clausal_analysis_var.get() == True:
        reminders_util.checkReminder(config_filename,
                                     reminders_util.title_options_CoreNLP_nn_parser,
                                     reminders_util.message_CoreNLP_nn_parser,
                                     True)

clausal_analysis_var.trace('w', activate_CoNLL_options)
noun_analysis_var.trace('w', activate_CoNLL_options)
verb_analysis_var.trace('w', activate_CoNLL_options)
function_words_analysis_var.trace('w', activate_CoNLL_options)


def activate_csv_fields_selection(checkButton, comingFrom_Plus, comingFrom_OK):
    if extract_var.get():
        select_csv_field_extract_menu.configure(state='normal')

    if not checkButton:
        extract_checkbox.config(state='normal')
        select_csv_field_extract_var.set('')
        select_csv_field_extract_menu.config(state='disabled')

        comparator_menu.configure(state="disabled")
        where_entry.configure(state="disabled")
        and_or_menu.configure(state="disabled")
        OK_extract_button.config(state='disabled')

        where_entry_var.set("")
        comparator_var.set("")
        and_or_var.set("")
    if checkButton:
        reset_all_button.config(state='normal')
        add_extract_options.config(state='normal')
        if select_csv_field_extract_var.get() != '':
            if comingFrom_Plus:
                select_csv_field_extract_menu.configure(state='normal')
            else:
                select_csv_field_extract_menu.configure(state='disabled')

            if where_entry_var.get() != '':
                and_or_menu.configure(state='normal')
            else:
                and_or_menu.configure(state='disabled')

            if comingFrom_OK:
                comparator_menu.configure(state="disabled")
                where_entry.configure(state="disabled")
                and_or_menu.configure(state='disabled')
                add_extract_options.config(state='disabled')
                OK_extract_button.config(state='disabled')
            else:
                add_extract_options.config(state='normal')
                OK_extract_button.config(state='normal')
                comparator_menu.configure(state="normal")
                where_entry.configure(state="normal")
        else:
            select_csv_field_extract_menu.configure(state='normal')
            extract_checkbox.config(state='normal')
            comparator_menu.configure(state="normal")
            where_entry.configure(state="normal")
            and_or_menu.configure(state="normal")
            OK_extract_button.config(state='normal')


select_csv_field_extract_var.trace('w', lambda x, y, z: extract_var.get())

activate_csv_fields_selection(extract_var.get(), False, False)

videos_lookup = {'No videos available':''}
videos_options='No videos available'

TIPS_lookup = {'CoNLL Table': "TIPS_NLP_Stanford CoreNLP CoNLL table.pdf",
               'POSTAG (Part of Speech Tags)': "TIPS_NLP_POSTAG (Part of Speech Tags) Stanford CoreNLP.pdf",
               'DEPREL (Stanford Dependency Relations)': "TIPS_NLP_DEPREL (Dependency Relations) Stanford CoreNLP.pdf",
               'English Language Benchmarks': 'TIPS_NLP_English Language Benchmarks.pdf',
               'Style Analysis': 'TIPS_NLP_Style Analysis.pdf', 'Clause Analysis': 'TIPS_NLP_Clause Analysis.pdf',
               'Noun Analysis': 'TIPS_NLP_Noun Analysis.pdf', 'Verb Analysis': 'TIPS_NLP_Verb Analysis.pdf',
               'Function Words Analysis': 'TIPS_NLP_Function Words Analysis.pdf',
               'Nominalization': 'TIPS_NLP_Nominalization.pdf', 'NLP Searches': "TIPS_NLP_NLP Searches.pdf",
               'Excel Charts': 'TIPS_NLP_Excel Charts.pdf',
               'Excel Enabling Macros': 'TIPS_NLP_Excel Enabling macros.pdf',
               'Excel smoothing data series': 'TIPS_NLP_Excel smoothing data series.pdf',
                'Statistical measures':'TIPS_NLP_Statistical measures.pdf',
               'Network Graphs (via Gephi)': 'TIPS_NLP_Gephi network graphs.pdf'}
TIPS_options = 'CoNLL Table', 'POSTAG (Part of Speech Tags)', 'DEPREL (Stanford Dependency Relations)', 'English Language Benchmarks', 'Style Analysis', 'Clause Analysis', 'Noun Analysis', 'Verb Analysis', 'Function Words Analysis', 'Nominalization', 'NLP Searches', 'Excel Charts', 'Excel Enabling Macros', 'Excel smoothing data series', 'Statistical measures', 'Network Graphs (via Gephi)'

# add all the lines lines to the end to every special GUI
# change the last item (message displayed) of each line of the function y_multiplier_integer = help_buttons
# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util.
right_msg = "\n\nON THE RIGHT-HAND SIDE, please, tick any of the checkboxes to obtain frequency distributions of specific linguistic objects."


def help_buttons(window, help_button_x_coordinate, y_multiplier_integer):
    resetAll = "\n\nPress the RESET ALL button to clear all values, including csv files and fields, and start fresh."
    plusButton = "\n\nPress the + buttons, when available, to add either a new field from the same csv file (the + button at the end of this line) or a new csv file (the + button next to File at the top of this GUI). Multiple csv files can be used with any of the operations."
    OKButton = "\n\nPress the OK button, when available, to accept the selections made, then press the RUN button to process the query."
    if not IO_setup_display_brief:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help", GUI_IO_util.msg_CoNLL)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                      GUI_IO_util.msg_outputDirectory)
    else:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                      GUI_IO_util.msg_IO_setup)

    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "ON THE LEFT-HAND SIDE, please, enter the CASE SENSITIVE token (i.e., word) to be searched (enter * for any word). ENTER * TO SEARCH FOR ANY TOKEN/WORD. The EXACT word will be searched (e.g., if you enter 'American', any instances of 'America' will not be found).\n\nTHE SELECT OUTPUT BUTTON IS DISABLED UNTIL A SEARCHED TOKEN HAS BEEN ENTERED.\n\nDO NOT USE QUOTES WHEN ENTERING A SEARCH TOKEN. n\nThe program will search all the tokens related to this token in the CoNLL table. For example, if the the token wife is entered, the program will search in each dependency tree (i.e., each sentence) all the tokens whose head is the token wife, and the head of the token wife." + right_msg + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "ON THE LEFT-HAND SIDE, please, select the CoNLL field to be used for the search (FORM or LEMMA).\n\nFor example, if brother is entered as the searched token, and FORM is entered as search field, the program will first search all occurrences of the FORM brother. Note that in this case brothers will NOT be considered. Otherwise, if LEMMA is entered as search field, the program will search all occurences of the LEMMA brother. In this case, tokens with form brother and brothers will all be considered." + right_msg + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "ON THE LEFT-HAND SIDE, please, select POSTAG value for searched token (e.g., NN for noun; RETURN for ANY POSTAG value)." + right_msg + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "ON THE LEFT-HAND SIDE, please, select DEPREL value for searched token (e.g., nsubjpass for passive nouns that are subjects; RETURN for ANY DEPREL value)." + right_msg + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "ON THE LEFT-HAND SIDE, please, select POSTAG value for token co-occurring in the same sentence (e.g., NN for noun; RETURN for ANY POSTAG value)." + right_msg + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "ON THE LEFT-HAND SIDE, please, select DEPREL value for token co-occurring in the same sentence (e.g., DEPREL nsubjpass for passive nouns that are subjects; RETURN for ANY DEPREL value)." + right_msg + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "Please, tick the checkbox if you wish to compute a sentence table with various sentence statistics.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "The EXTRACT option allows you to select specific fields, even by specific values, from one or more csv files and save the output as a new file.\n\nStart by ticking the Extract checkbox, then selecting the csv field from the current csv file. To filter the field by specific values, select the comparator character to be used (e.g., =), enter the desired value in the \'WHERE\' widget (case sensitive!), and select and/or if you want to add another filter.\n\nOptions become available in succession.\n\nPress the + button to register your choices (these will be displayed in command line in the form: filename and path, field, comparator, WHERE value, and/or selection; empty values will be recorded as ''. ). PRESSING THE + BUTTON TWICE WITH NO NEW CHOICES WILL CLEAR THE CURRENT CHOICES. PRESS + AGAIN TO RE-INSERT THE CHOICES. WATCH THIS IN COMMAND LINE.\n\nIF YOU DO NOT WISH TO FILTER FIELDS, PRESS THE + BUTTON AFTER SELECTING THE FIELD." + plusButton + OKButton + GUI_IO_util.msg_Esc + resetAll)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "ON THE LEFT-HAND SIDE, please, tick the checkbox if you wish to extract SVOs from the CoNLL table.\n\nON THE RIGHT-HAND SIDE, tick the 'All analyses: clauses, nouns, verbs, function words (\'junk/stop\' words)' to select and deselect all options, allowing you to select specific options." + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  "Please, tick the checkbox if you wish to run the repetition finder to locate word expressions repeated across selected K sentences." + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  GUI_IO_util.msg_openOutputFiles)
    return y_multiplier_integer -1
y_multiplier_integer = y_multiplier_integer = help_buttons(window, GUI_IO_util.get_help_button_x_coordinate(), increment)

# change the value of the readMe_message
readMe_message = "This Python 3 script will allow you to analyze in depth the contents of the CoNLL table (CoNLL U format), the table produced by Stanford CoreNLP parser. You can do two things in this GUI, depending upon whether you use the tools on the left-hand side (a search tool) or the tools on the right-hand side (statistical frequency tools).\n\nON THE LEFT-HAND SIDE, you can search all the tokens (i.e., words) related to a user-supplied keyword, found in either FORM or LEMMA of a user-supplied CoNLL table.\n\nYou can filter results by specific POSTAG and DEPREL values for both searched and co-occurring tokens (e.g., POSTAG ‘NN for nouns, DEPREL nsubjpass for passive nouns that are subjects.)\n\nIn INPUT the script expects a CoNLL table generated by the python script StanfordCoreNLP.py. \n\nIn OUTPUT the script creates a tab-separated csv file with a user-supplied filename and path.\n\nThe script also displays the same infomation in the command line.\n\nON THE RIGHT-HAND SIDE, the tools provide frequency distributions of various types of linguistic objects: clauses, nouns, verbs, and function words." + GUI_IO_util.msg_multipleDocsCoNLL
readMe_command = lambda: GUI_IO_util.display_help_button_info("NLP Suite Help", readMe_message)
scriptName=os.path.basename(__file__)

GUI_util.GUI_bottom(config_filename, config_input_output_numeric_options, y_multiplier_integer, readMe_command, videos_lookup, videos_options, TIPS_lookup, TIPS_options, IO_setup_display_brief,scriptName,True)

if GUI_util.input_main_dir_path.get()!='':
    GUI_util.run_button.configure(state='disabled')
    mb.showwarning(title='Input file',
                   message="The CoNLL Table Analyzer scripts require in input a csv CoNLL table created by the Stanford CoreNLP parser (not the spaCy and Stanza parsers).\n\nAll options and RUN button are disabled until the expected CoNLL file is seleted in input.\n\nPlease, select in input a CoNLL file created by the Stanford CoreNLP parser.")
    error = True
    activate_options()
else:
    GUI_util.run_button.configure(state='normal')
    if inputFilename.get()!='':
        if not CoNLL_util.check_CoNLL(inputFilename.get()):
            error = True
            activate_options()

GUI_util.window.mainloop()
