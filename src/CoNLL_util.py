import sys
import GUI_util
# import IO_libraries_util
#
# if IO_libraries_util.install_all_packages(GUI_util.window, "CoNLL_util",
# 								['os', 'io','tkinter','pandas','time']) == False:
# 	sys.exit(0)

import os
import tkinter.messagebox as mb
import time
import io
import pandas as pd


import IO_user_interface_util
import Stanford_CoreNLP_tags_util
import IO_csv_util

global sentenceID_position, documentID_position, document_position

clause_position = 8 # NEW CoNLL_U
sentenceID_position = 10  # NEW CoNLL_U
documentID_position = 11  # NEW CoNLL_U
document_position = 12 # NEW CoNLL_U

def find_full_postag(__form__, __postag__):
    if __postag__ in Stanford_CoreNLP_tags_util.dict_POSTAG:
        return Stanford_CoreNLP_tags_util.dict_POSTAG[__postag__]
    else:
        #return __form__
        return "Not found in CoNLL POSTAG list"

def find_full_deprel(__form__, __deprel__):
    if __deprel__ in Stanford_CoreNLP_tags_util.dict_DEPREL:
        return Stanford_CoreNLP_tags_util.dict_DEPREL[__deprel__]
    else:
        #return __form__
        return "Not found in CoNLL DEPREL list"


def find_full_clausalTag(__form__, __clausalTag__):
    if __clausalTag__ in Stanford_CoreNLP_tags_util.dict_CLAUSALTAG:
        return Stanford_CoreNLP_tags_util.dict_CLAUSALTAG[__clausalTag__]
    else:
        #return __form__
        return "Not found in CoNLL CLausal_Tag list"

#check the number of columns in a csv file to ensure that a conll table is used in input
#conll tables will have either 13 or 14 columns (14 if a date field is included)
# returns False if filename is NOT CoNLL
def check_CoNLL(filename,skipWarning=False):
    wrongFile=False
    headers=IO_csv_util.get_csvfile_headers(filename)
    numColumns=len(headers)
    #check the headers; 13 or 14 if date is available
    if ('ID' and 'Form' and 'Lemma' not in headers):
        wrongFile = True
    else:
        if (numColumns!=13 and numColumns!=14):
            wrongFile=True
    if wrongFile==True and skipWarning==False:
        mb.showwarning(title='Input file error', message='The script expects in input a CoNLL table with the headers ID, Form, and Lemma and either 14 or 13 columns (with/without date field).\n\nThe selected file does not have these expected characteristics (number of columns = ' + str(numColumns) + ').\n\nPlease, select a CoNLL file and try again.')
    if wrongFile==True:
        return False
    else:
        return True

def sentence_division(list_csv_rows):

    try:
        list_sentences = []
        Sentence_ID_prev = 1  # Sentence_ID of previous row
        Document_ID_prev = '1.0'  # Document_ID of previous row
        current_sentence = []

        for _index_, item in enumerate(list_csv_rows):
            Sentence_ID = int(item[sentenceID_position])
            Document_ID = item[documentID_position]
            # This includes the last sentence
            if _index_ + 1 == len(list_csv_rows):
                list_sentences.append(current_sentence)
                current_sentence.append(item)
                return list_sentences
            if Sentence_ID == Sentence_ID_prev and Document_ID == Document_ID_prev:
                current_sentence.append(item)
                continue
            else:
                Sentence_ID_prev = Sentence_ID
                Document_ID_prev = Document_ID
                list_sentences.append(current_sentence)
                current_sentence = []
                current_sentence.append(item)
        if len(list_sentences) == 0:
            currentScript = os.path.basename(__file__)
            mb.showinfo("Fatal error",
                        "The sentence_division function in " + currentScript + " failed.\n\nPlease, check your data and/or the python scripts.\n\nIf the problem persists, please inform the script developers of the problem.\n\nProgram will exit.")
        return list_sentences
    except:
        print(
            "FATAL ERROR: INPUT MUST BE A CoNLL TABLE, generated by the Stanford_CoreNLP.py routine (parser option). Please, select a CoNLL table and try again.")
        mb.showinfo("Fatal error",
                    "INPUT MUST BE A CoNLL TABLE, generated by the Stanford_CoreNLP.py routine (parser option).\n\nPlease, select a CoNLL table and try again.")

# searching for a specific sentence sent_id in a specific document Document_ID
def Sentence_searcher(list_all_sents, Document_ID, sent_id):
    for sent in list_all_sents:
        if len(sent) > 0:
            if sent[0][documentID_position] == Document_ID and int(sent[0][sentenceID_position]) == int(sent_id):
                sent_str = " ".join([i[1] for i in sent])
                break
    return sent_str

# used by all CoNLL_*_analysis_util scripts

# label is the header displayed (e.g., verb voice, modality)
# in input the function takes _voice_sorted_ created by the various CoNLL analyses functions
# in input it contains the CoNLL table entries with the addition of the label (modallity, tense...) followed by the full sentence
# in output, the label is placed FIRST
def sort_output_list(label, _voice_sorted_):
    output_list = [
        [label, 'TOKEN_INDEX', 'FORM', 'LEMMA', 'POSTAG', 'POSTAG-DESCRIPTION', 'DEPREL', 'DEPREL-DESCRIPTION',
         'CLAUSAL TAG', 'CLAUSAL TAG-DESCRIPTION', 'Sentence ID', 'Sentence', 'Document ID', 'Document']]
    #the earlier new CoNLL routine always had the extra header date, whether there or not;
    #   so need to test not to break the code

    # recordID_position = 8
    # documentID_position = 10

    # NEW
    # recordID_position = 9
    # sentence_ID position = 10

    # the i[#] refer too the position in the CoNLL table
    # 12/13 is the label: modality, tense, ... (Displayed as the first column of the output csv file)

    # NEW
    # 13/14 is the label: modality, tense, ... (Displayed as the first column of the output csv file)

    # 0 is INDEX
    # 1 form
    # 2 lemma
    # 3 postag
    # 6 deprel

    # 7 clause
    # 9 Sentence_ID
    # 10 Document_ID/documentID_position
    # 11 document name

    # NEW
    # 8 clause
    # 10 Sentence_ID
    # 11 Document_ID/documentID_position
    # 12 document name

    # 12/13 label: modality, tense, ...
    # 13/14 full sentence

    # NEW
    # 13/14 label: modality, tense, ...
    # 14/15 full sentence

    try:
        _list_sorted_ = [
            [i[14], i[0], i[1], i[2], i[3], find_full_postag(i[1],i[3]), i[6], find_full_deprel(i[1],i[6]), i[clause_position],
                find_full_clausalTag(i[1],i[clause_position]), i[sentenceID_position], i[documentID_position], i[documentID_position], i[15]]
        for i in _voice_sorted_]
    except:
        try:
            _list_sorted_ = [
                [i[13], i[0], i[1], i[2], i[3], find_full_postag(i[1],i[3]), i[6], find_full_deprel(i[1],i[6]), i[clause_position],
                 find_full_clausalTag(i[1],i[clause_position]), i[sentenceID_position], i[documentID_position], i[documentID_position], i[14]] for i in _voice_sorted_]
        except:
            mb.showwarning(title="CoNLLL table ill formed",
                           message="The CoNLL table is ill formed. You may have tinkered with it. Please, rerun the Stanford CoreNLP parser since many scripts rely on the CoNLL table.")
            return
    output_list += _list_sorted_
    return output_list

# Cynthia Dong & Roberto Franzosi 11/28/2019
# compute a whole sentence from an input CoNLL table for a specific sentenceID and documentID
# called by the geocoder
def compute_sentence(CoNLL_table, recordID, sentenceID, documentID):
    """
    :type documentID: object
    """
    # Open ConLL
    df = pd.read_csv(io.open(CoNLL_table, 'rb'), sep=',', index_col=False, encoding='utf-8',error_bad_lines=False)
    df = df[df["Sentence ID"] == sentenceID]
    df = df[df["Document ID"] == documentID]
    rows = []  # Store data
    sent_str = ""  # Build string
    index = recordID
    for recordID in range(df.shape[0]):  # For every row in the ConLL table starting from RecordID
        row = df.iloc[recordID, :]
        # print ("sentenceID: ", sentenceID, " documentID: ", documentID, " recordID: ",recordID)
        # print("index: ",index)
        if sentenceID == row[sentenceID_position] and documentID == row[documentID_position]:  # Build the sentence if we are on the same document and sentence
            if row[6] == "punct":
                sent_str = sent_str + str(row[1])
            else:
                sent_str = sent_str + " " + str(row[1])
        else:
            if row[sentenceID_position] > sentenceID or row[documentID_position] > documentID:
                break
        index = index + 1
    return index, sent_str

# the function computes a sentence table from a conll table
# TODO must check for old and new CoNLL
def compute_sentence_table(CoNLL_table, output_path):
    RunningCoreNLPFromCommandLine = False
    startTime = time.localtime()
    # print ("")
    # print("Started computing the Sentence table at " + str(startTime[3]) + ':' + str(startTime[4]))  #Time when merge started, for future reference
    # print ("")
    if RunningCoreNLPFromCommandLine != True:
        IO_user_interface_util.timed_alert(GUI_util.window, 4000, 'Analysis start', 'Started computing the Sentence table at', True)
    # tk.messagebox.showinfo("Stanford CoreNLP has finished", "Started computing the Sentence table at " + str(startTime[3]) + ':' + str(startTime[4]))
    # df = pd.read_csv(io.open(os.path.join(output_path,CoNLL_table), 'rb'), sep='\t', header=None, index_col=False) # Open ConLL
    df = pd.read_csv(io.open(os.path.join(output_path, CoNLL_table), 'rb'), sep=',', index_col=False, encoding='utf-8',error_bad_lines=False)  # Open ConLL
    rows = []  # Store data
    sent_str = ""  # Build string
    # Keep track of variables
    sent_index = df.iloc[0][sentenceID_position]
    doc_id = df.iloc[0][documentID_position]
    current_file = df.iloc[0][document_position]

    for index, row in df.iterrows():  # For every row in the ConLL
        if sent_index == row[sentenceID_position] and doc_id == row[documentID_position]:  # Build the sentence if we are on the same document and sentence
            if row[6] == "punct":
                sent_str = sent_str + str(row[1])
            else:
                sent_str = sent_str + " " + str(row[1])
        else:  # End the sentence, add it to the array and move onto the next one
            arr = [len(sent_str.split(" ")),
                   len(list(sent_str)), sent_index, sent_str, doc_id, current_file]  # Save the data
            rows.append(arr)
            sent_index = row[sentenceID_position]
            sent_str = row[1]
            current_file = row[document_position]
            doc_id = row[documentID_position]

    # Construct and save the table
    col_names = ['Sentence length (Number of words/tokens)',
                 'Sentence length (Number of characters)', 'Sentence ID', 'Sentence', 'Document ID', 'Document']
    df2 = pd.DataFrame(columns=col_names, data=rows)

    output_fileName = os.path.join(output_path, CoNLL_table[:-4] + "_sentence" + ".csv")
    df2.to_csv(output_fileName, encoding='utf-8',
               index=False)  # os.path.join(output_path,output_fileName), sep='\t', encoding='utf-8')
    if RunningCoreNLPFromCommandLine != True:
        IO_user_interface_util.timed_alert(GUI_util.window, 4000, 'Analysis end', 'Finished computing the Sentence table at', True)
    # tk.messagebox.showinfo("Stanford CoreNLP has finished", "Finished computing the Sentence table at " + str(endTime[3]) + ':' + str(endTime[4])  + ". \n\nSentence table exported as: " + output_fileName) #os.path.join(output_path,output_fileName))
    endTime = time.localtime()
    print ("\nSentence table output written to: " + output_fileName)  # os.path.join(output_path,output_fileName))     #Time when compute sentence table finished, for future reference
    return output_fileName

# the function extracts DISTINCT nouns and verbs from the CoNLL table in both form and lemma
# inputFilename contains path
def get_nouns_verbs_CoNLL(inputFilename,output_dir):

    conll_table = pd.read_csv(inputFilename, encoding='utf-8',error_bad_lines=False)

    verb_form_set = set()
    verb_lemma_set = set()
    noun_form_set = set()
    noun_lemma_set = set()

    for index, row in conll_table.iterrows():
        # Check if cell value has length greq. than 2 since we're looking for VB* and NN*
        if len(conll_table['POStag'][index]) >= 2:
            # Check if begins with VB
            if "VB" in conll_table['POStag'][index][0:2]:
                # Starts with VB, add to verb set
                verb_form_set.add(conll_table['Form'][index])
                verb_lemma_set.add(conll_table['Lemma'][index])
            # Check if begins with NN
            elif 'NN' in conll_table['POStag'][index][0:2]:
                noun_form_set.add(conll_table['Form'][index])
                noun_lemma_set.add(conll_table['Lemma'][index])

    verbs_form_df = pd.DataFrame(verb_form_set, columns = ['Verbs'])
    verbs_lemma_df = pd.DataFrame(verb_lemma_set, columns = ['Verbs'])
    nouns_form_df = pd.DataFrame(noun_form_set, columns = ['Nouns'])
    nouns_lemma_df = pd.DataFrame(noun_lemma_set, columns = ['Nouns'])

    nouns_form_csv=os.path.join(output_dir,os.path.basename(inputFilename[:-4])+"_nouns_form.csv")
    nouns_lemma_csv=os.path.join(output_dir,os.path.basename(inputFilename[:-4])+"_nouns_lemma.csv")
    verbs_form_csv=os.path.join(output_dir,os.path.basename(inputFilename[:-4])+"_verbs_form.csv")
    verbs_lemma_csv=os.path.join(output_dir,os.path.basename(inputFilename[:-4])+"_verbs_lemma.csv")

    nouns_form_df.to_csv(nouns_form_csv, encoding='utf-8', index=False)
    nouns_lemma_df.to_csv(nouns_lemma_csv, encoding='utf-8', index=False)
    verbs_form_df.to_csv(verbs_form_csv, encoding='utf-8', index=False)
    verbs_lemma_df.to_csv(verbs_lemma_csv, encoding='utf-8', index=False)

    return nouns_form_csv, nouns_lemma_csv, verbs_form_csv, verbs_lemma_csv
