#The Python 3 routine was written by Jian Chen, 12.12.2018
# modified by Jian Chen (January 2019)
# modified by Jack Hester (February 2019)
# modified by Roberto Franzosi (February 2019-August 2020), November 2021

import sys
import GUI_util
import IO_libraries_util

if IO_libraries_util.install_all_packages(GUI_util.window,"CoNLL_clause_analysis.py",['os','csv','tkinter','ntpath','collections','subprocess'])==False:
    sys.exit(0)

import os
from collections import Counter
import tkinter.messagebox as mb
import pandas as pd

import IO_files_util
import IO_csv_util
import IO_user_interface_util
import CoNLL_util
import charts_Excel_util
import statistics_csv_util
import Stanford_CoreNLP_tags_util

dict_POSTAG, dict_DEPREL = Stanford_CoreNLP_tags_util.dict_POSTAG, Stanford_CoreNLP_tags_util.dict_DEPREL

clause_position = 8 # NEW CoNLL_U
recordID_position = 9 # NEW CoNLL_U
sentenceID_position = 10 # NEW CoNLL_U
documentID_position = 11 # NEW CoNLL_U

# Following are used if running all analyses to prevent redundancy
# filesToOpen = []  # Store all files that are to be opened once finished
input_file_name = ''
output_dir = ''

# def compute_stats(CoNLL_table):
#     global clausal_list, clausal_counter
#     clausal_list = [i[clause_position] for i in CoNLL_table]
#     clausal_counter = Counter(clausal_list)
#     return clausal_list, clausal_counter

# def clause_compute_frequencies(data, data_divided_sents):
#     clause_tags = []

#     clause_stats = [['Clause Tags', 'Frequencies'],
#                          ['Clause-level (S - Sentence)', clausal_counter['S']],
#                          ['Clause-level (SBAR - Clause introduced by a (possibly empty) subordinating conjunction)', clausal_counter['SBAR']],
#                          ['Clause-level (SBARQ - Direct question introduced by a wh-word or a wh-phrase)', clausal_counter['SBARQ']],
#                          ['Clause-level (SINV - Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal)', clausal_counter['SINV']],
#                          ['Phrase-level (NP - Noun Phrase)', clausal_counter['NP']],
#                          ['Phrase-level (VP - Verb Phrase)', clausal_counter['VP']],
#                          ['Phrase-level (ADJP - Adjective Phrase)', clausal_counter['ADJP']],
#                          ['Phrase-level (ADVP - Adverb Phrase)', clausal_counter['ADVP']],
#                          ['Phrase-level (PP - Prepositional Phrase)', clausal_counter['PP']]]

#     return clause_stats

# written by Tony Chen Gu Mar 2022
# add an extra column describing verb tense
def clause_data_preparation(data):
    dat = []
    sbar_counter = 0
    s_counter = 0
    sbarq_counter = 0
    sinv_counter = 0
    np_counter = 0
    vp_counter = 0
    adjp_counter = 0
    advp_counter = 0
    pp_counter = 0
    clause_list = ['S','SBAR', 'SBARQ', 'SINV', 'NP', 'VP', 'ADJP', 'ADVP', 'PP']

    for i in data:
        if(i[8] in clause_list):
            tense = i[8]
            if(tense == 'SBAR'):
                tense_col = 'Clause introduced by a (possibly empty) subordinating conjunction'
                sbar_counter+=1
            elif(tense == 'SBARQ'):
                tense_col = 'Direct question introduced by a wh-word or a wh-phrase'
                sbarq_counter+=1
            elif(tense == 'SINV'):
                tense_col = 'Inverted declarative sentence'
                sinv_counter+=1
            elif(tense == 'NP'):
                tense_col = 'Noun Phrase'
                np_counter+=1
            elif(tense == 'VP'):
                tense_col = 'Verb Phrase'
                vp_counter+=1
            elif(tense == 'ADJP'):
                tense_col = 'Adjective Phrase'
                adjp_counter+=1
            elif(tense == 'ADVP'):
                tense_col = 'Adverb Phrase'
                advp_counter+=1
            elif(tense == 'PP'):
                tense_col = 'Prepositional Phrase'
                pp_counter+=1
            elif(tense == 'S'):
                tense_col = 'Sentence'
                s_counter+=1
            dat.append(i+[tense_col])
            
    clause_stats = [['Clause Tags', 'Frequencies'],
                         ['Clause-level (S - Sentence)', s_counter],
                         ['Clause-level (SBAR - Clause introduced by a (possibly empty) subordinating conjunction)', sbar_counter],
                         ['Clause-level (SBARQ - Direct question introduced by a wh-word or a wh-phrase)', sbarq_counter],
                         ['Clause-level (SINV - Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal)', sinv_counter],
                         ['Phrase-level (NP - Noun Phrase)', np_counter],
                         ['Phrase-level (VP - Verb Phrase)', vp_counter],
                         ['Phrase-level (ADJP - Adjective Phrase)', adjp_counter],
                         ['Phrase-level (ADVP - Adverb Phrase)', advp_counter],
                         ['Phrase-level (PP - Prepositional Phrase)', pp_counter]]
    dat = sorted(dat, key=lambda x: int(x[recordID_position]))
    return clause_stats, dat

def clause_stats(inputFilename,inputDir, outputDir,data, data_divided_sents,openOutputFiles,createExcelCharts):

    filesToOpen = []  # Store all files that are to be opened once finished

    startTime=IO_user_interface_util.timed_alert(GUI_util.window, 3000, 'Analysis start', 'Started running CLAUSE ANALYSES at',
                                                 True, '', True, '', True)

    #output file names
    #clausal_analysis_file_name contains all the CoNLL table records that have a clausal tag
    clausal_analysis_file_name=IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv', 'CA', 'Clause tags', 'list')
    filesToOpen.append(clausal_analysis_file_name)
    #clausal_analysis_stats_file_name will contain a data sheet with the frequency distribution of all available clausal tags and a chart sheet with the pie chart visualization of the data
  
    
    # if 0:
    #    stats_clauses(data)
    #else:
    if not os.path.isdir(outputDir):
        mb.showwarning(title='Output file path error', message='Please check OUTPUT DIRECTORY PATH and try again')
        return

    #clausal_list, clausal_counter = compute_stats(data)
    #clausal_stats = clause_compute_frequencies(data,data_divided_sents)

    clausal_stats, clausal_list = clause_data_preparation(data)

    clausal_analysis_stats_file_name=IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv', 'CA', 'Clause tags', 'stats')
    clause_file_name = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv', 'CA', 'Clause tags', 'list')
    errorFound=IO_csv_util.list_to_csv(GUI_util.window,clausal_stats,clausal_analysis_stats_file_name)
    if errorFound==True:
        return
    errorFound=IO_csv_util.list_to_csv(GUI_util.window,clausal_list,clause_file_name)
    if errorFound==True:
        return

    df = pd.read_csv(clause_file_name, header=None)
    df.to_csv(clause_file_name,
				header=["ID", "FORM", "Lemma", "POStag", "NER", "Head", "DepRel", "Deps", "Clause Tag", "Record ID", "Sentence ID", "Document ID", "Document",
						"Clause Tags"])
    

    if createExcelCharts==True:
        Excel_outputFilename= charts_Excel_util.create_excel_chart(GUI_util.window,
                                        data_to_be_plotted=[clausal_stats],
                                        inputFilename=clausal_analysis_stats_file_name,
                                        outputDir=outputDir,
                                        scriptType='CoNLL_Clause',
                                        chartTitle="Frequency Distribution of Clause Type",
                                        chart_type_list=["pie"],
                                        column_xAxis_label="Clause Tags",
                                        column_yAxis_label="Frequency")
        if Excel_outputFilename != "":
            filesToOpen.append(Excel_outputFilename)

        # return filesToOpen # to avoid code breaking in plot by sentence index

        # line plot by sentence index
        Excel_outputFilename = charts_Excel_util.compute_csv_column_frequencies(inputFilename=clause_file_name,
                                        outputDir=outputDir,
                                        select_col=['Clause Tags'],
                                        group_col=['Sentence ID'],
                                        chartTitle="Frequency Distribution of Clause")
        # Excel_outputFilename=charts_Excel_util.compute_csv_column_frequencies(GUI_util.window,
        #                                                                 clausal_analysis_file_name,
        #                                                                 '',
        #                                                                 outputDir,
        #                                                                 openOutputFiles,
        #                                                                 createExcelCharts,
        #                                                                 [[8,8]],
        #                                                                 ['CLAUSE TAGS'],
        #                                                                 ['FORM','Sentence'],
        #                                                                 ['Sentence ID','Document ID'],
        #                                                                 'CA','line')
        if len(Excel_outputFilename)>0:
            filesToOpen.extend(Excel_outputFilename)

        # output_df= charts_Excel_util.add_missing_IDs(clausal_analysis_file_name)
        # # overwrite original file having added any missing document ID and sentence ID
        # output_df.to_csv(clausal_analysis_file_name,index=False)
        # columns_to_be_plotted = [[1, 8]]
        # hover_label = ['CLAUSAL TAG-DESCRIPTION']
        # inputFilename = clausal_analysis_file_name
        # Excel_outputFilename = charts_Excel_util.run_all(columns_to_be_plotted,
        #                                             inputFilename, outputDir,
        #                                             outputFileLabel='CoNLL_Clause',
        #                                             chart_type_list=["line"],
        #                                             chart_title='Frequency of Clause Tags',
        #                                             column_xAxis_label_var='Sentence index',
        #                                             hover_info_column_list=hover_label,
        #                                             count_var=1)
        # if Excel_outputFilename!='':
        #     filesToOpen.append(Excel_outputFilename)

    IO_user_interface_util.timed_alert(GUI_util.window, 3000, 'Analysis end', 'Finished running CLAUSE ANALYSES at', True, '', True, startTime, True)
    return filesToOpen

