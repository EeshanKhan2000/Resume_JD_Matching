# Introduction

 This repository contains code for a task to match and rank resumes from the following Kaggle Resumes datsset: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset for selected job-descriptions from the Hugging Face Job Descriptions Dataset (https://huggingface.co/datasets/jacob-hugging-face/job-descriptions/viewer/default/train?row=0) 
 Specifically, the following files are present: 

 1. parser_basic.py: Uses PyPDF2 to parse resumes from the selected categories. Further, text cleaning and extraction of different sections in each resume is performed here. This can be further updated to use advanced methods, such as identifying seperators for different sections, since there is a distribution of synonyms used in place of "skills", "education", "experience" in some resumes. Other than that, summary generation for extracting each section of the resume, so as to compress data and remove noise could also be considered. 

 2. obtain_jds.py: Simply selects specified JDs from the provided data of Job Descriptions, cleans text and stores it in a more accessible format.

 3. Resume_Feature_Matching.ipynb: Uses HuggingFace DistilBert Tokenizer and model for generating embeddings from the text. 
 4. Resume_Ranking.ipynb: Uses cosine similarity to generate a resume ranking for selected 20 JDs. 
 5. top_5_cvs_selected_jds.csv: indices of JDs matched to full paths of the top 5 matching resumes. 
 6. Resume_archive: has the subset of data which is used, from the original dataset. 

# Problems Faced and Solutions

 1. Numbers in JD and Resume: Numbers need to be translated into the context they present. For example, cumulative the years worked in all roles need to be translated to total experience in years. This featrue can be added using Regex. Along with that, using Named Entity Recognition, the years can be further categorized into types of roles. 

 2. Usage of synonyms for section deliniation: When words such as "Expertise" are used in place of "Skills" as section headers. 

 3. Lack of Title in some Resumes, and some titles appearing after name: For this, again, NER has to be used while parsing itself. 

 4. Weightage given to different sections while matching for overall ranking: There is no method to determine this, other than fine-tuning the model, with different sections being processed parallely for some layers. 

# Further possible work

1. Fine-tuning the model on the dataset.
2. For creating a ranking of all JDs, rather than KNN, ANN (Approximate Nearest Neighbor) search can be used. Extracted Embeddings from CVs can be used to create a Hierarchial Navigable Small World Graph for logarithmic look-up (~O(nlogn)). This feature is available in many vector-databases, such as in Langchain, Pinecone etc. 
