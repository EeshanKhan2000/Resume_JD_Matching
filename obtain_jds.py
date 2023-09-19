# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 22:25:16 2023

@author: eeshan
"""
'''
This is a simple script for cleaning JDs, obtaining different sections and 
storing them in s csv in a more accessible way.
'''

import pickle
import pandas as pd 
import json
import re

save_indices_flag = False

def clean_text(text):
    cleaned_text = re.sub('[^a-zA-Z]', ' ', text)
    cleaned_text = re.sub(r'[^\w\s]|_', ' ', cleaned_text)
    cleaned_text = re.sub(r'\d+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    cleaned_text=re.sub('http\S+\s', " ", cleaned_text)
    cleaned_text = re.sub(r'[^\x00-\x7f]',r' ', cleaned_text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text

    
base_folder = "."
jd_file_path = base_folder + "/training_data.csv"

df_all = pd.read_csv(jd_file_path)

print(df_all.columns)


# The indices here are for Job Descriptions which have been manually selected for this task. 
selected_jobs_list = [i for i in range(3,16)]
selected_jobs_list.extend([i for i in range(29,37)])

df = df_all.iloc[selected_jobs_list]

if save_indices_flag:
    index_mapping_path = base_folder + "/indices.pickle"
    
    indices_list = list(df.index)
    print(indices_list)
    
    with open(index_mapping_path, 'wb') as f:
        pickle.dump(indices_list, f)

df = df.reset_index()
df = df.drop("index", axis=1)

# seperate jd and m_r, but m_r concatenated. 
sections = {"Job Description": [], "Title": [], "Core Responsibilities": [], "Educational Requirements": [], "Experience Level": [],
            "Required Skills": []}


for i in range(len(df)):
    jd = clean_text(df["job_description"][i])
    mr = json.loads(df["model_response"][i])
    title = df["position_title"][i].strip().lower()
    
    if jd != "n/a" and jd != '':
        sections["Job Description"].append(jd)
    else:
        sections["Job Description"].append(None)
    
    sections["Title"].append(title)
        
    for sec in sections.keys():
        if sec in mr.keys() and (mr[sec] != "N/A" and mr[sec] != "n/a" and mr[sec] != "n a" and mr[sec] != ''):
            sections[sec].append(clean_text(mr[sec]))
        else:
            if sec != "Job Description" and sec != "Title":
                sections[sec].append(None)

df_jd = pd.DataFrame(sections)
df_jd.to_csv(base_folder + "/job_descriptions_selected_cleaned.csv")



