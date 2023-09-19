# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 19:35:26 2023

@author: eeshan
"""
from PyPDF2 import PdfReader
import pandas as pd
import os
import re

# =============================================================================
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
# =============================================================================


base_folder = "."
base_cv_folder = base_folder + "/data/data"
resume_folder = base_folder + "/Resume"

cv_types = os.listdir(base_cv_folder)

selected_types = [15,20] # Engineering and Information-Technology

sectionize_flag = False  # If True, entire cv text will not be as-is stored, but will be broken into sections as defined below

if sectionize_flag:
    sections = {"cv_category": [],"cv_number": [], "title": [], "experience": [], "education": [], "skills": []}
else:
    sections = {"cv_category": [],"cv_number": [], "title": [],"cleaned_text": []}

find_section_words = set(["experience", "education", "skills"]) # words to look for to deliniate sections. This can be made better using semantic extraction.

df = pd.DataFrame() # To store extracted CVs

for selected_type in selected_types:
    # Get paths for selected CVs. 
    cv_type = cv_types[selected_type]
    selected_type_folder = base_cv_folder + "/{}".format(cv_type)
    cv_names = os.listdir(selected_type_folder)
    
    for cv_name in cv_names:
        cv_path = selected_type_folder + "/{}".format(cv_name)
        
        # Read CV PDF
        reader = PdfReader(cv_path)
        number_of_pages = len(reader.pages)
        words = []
        title = ""
        
        sections["cv_category"].append(cv_type)
        sections["cv_number"].append(cv_name.split('.')[0])
        
        for page_num in range(number_of_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            cleaned_text = re.sub('[^a-zA-Z]', ' ', text)
            cleaned_text = re.sub(r'[^\w\s]|_', ' ', cleaned_text)
            cleaned_text = re.sub(r'\d+', ' ', cleaned_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            cleaned_text=re.sub('http\S+\s', " ", cleaned_text)
            cleaned_text = re.sub(r'[^\x00-\x7f]',r' ', cleaned_text)
            cleaned_text = cleaned_text.lower()
            
# =============================================================================
#             # Tokenize
#             word_tokens = word_tokenize(cleaned_text)
#     
#             # Remove stopwords
#             stop_words = set(stopwords.words('english'))
#             filtered_words = [word_token for word_token in word_tokens if word_token not in stop_words]
#             
#             # Apply stemming
#             stemmer = PorterStemmer()
#             stemmed_words = [stemmer.stem(word_filter) for word_filter in filtered_words]
#             
#             # Remove extra words
#             extra_words = ['compani', 'name', 'citi', 'state', 'work', 'manag']
#             extra_words_removed = [word for word in stemmed_words if word not in extra_words]
#             
#             cleaned_text = ' '.join(extra_words_removed)
# =============================================================================

            # Obtain CV title. This is present and easily extracted from most CVs. 
            if page_num == 0:
                i = 0
                while i < len(text) and text[i] != '\n':
                    title += text[i]
                    i += 1
                if title != '':
                    sections["title"].append(title.lower())
                else:
                    sections["title"].append(None)

            words_page = cleaned_text.split()
            
            words.extend(words_page)
        
        
        if sectionize_flag:
            '''
            Here the words are put into their relevant sections. Each split is identified by the index of the header
            associated with the section, as well as the occurance of key-word defined for that section in 
            find_section_words above. 
            '''
            section_splits = []
            found_words = set() # In order to disallow repetitions of words to form sections of their own. 
    
            for index, word in enumerate(words):
                if word in find_section_words and word not in found_words:
                    section_splits.append([index, word])
                    found_words.add(word)
    
            
            for i in range(len(section_splits)):
                split = section_splits[i]
                
                if i != len(section_splits)-1:
                    next_index = section_splits[i+1][0]
                else:
                    next_index = len(words)
                    
                word = split[1]
                split_part = ' '.join(words[split[0] + 1 : next_index]).strip()

                
                if split_part != ' ' and split_part != '':
                    sections[word].append(split_part)
                else:
                    sections[word].append(None)
            
            # To account for sections not present in some CVs, or the ones which could not be deliniated. 
            for word in list(find_section_words - found_words):
                sections[word].append(None) 
           
            
        else:
            whole_text = ' '.join(words)
            sections["cleaned_text"].append(whole_text)

        
df = pd.DataFrame(sections)
df.to_csv(resume_folder + "/Resumes_Extracted_Sectionized_{}.csv".format(sectionize_flag))

