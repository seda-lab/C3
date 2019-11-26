# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
Created on November 12, 2019
@author: Anais Ollagnier

Identify Skills in CV (supports PDF and DOCx formats)
Pyresparser: https://github.com/OmkarPathak/pyresparser

Usage: 
        cv parsing : python3 skillsFromResume.py cv_folder/ Result/
        job recommendation : python3 skillsFromResume.py -r cv_folder/ Result/
'''

import glob
import sys
import os
import json
import random
from tempfile import mkdtemp
import pandas as pd 
from joblib import dump, load

# Main packages
import spacy
spacy.load('en_core_web_sm')
import nltk

from utils import *
from pyresparser import ResumeParser
from fuzzywuzzy import process
import numpy as np
from gensim.models import FastText
from tqdm import tqdm


def skill_extraction(rootDir, directory, dirResult, result) :
    """
    Run skill extractor module from pyresparser software
    
    Parameters
    ----------
    rootDir : string
        path to the root directory
    directory : string
        directory where resumes are stored
    dirResult : string 
        directory where output files are generated
    result : string
        result file where the model is saved (csv format)
    """
    #f= open(dirResult+result,"w")
    dict_skills = {}

    #for file in list(glob.glob(directory+'/*')):
    for file in list(glob.glob(directory+'/OmkarResume.pdf')):
        basename = os.path.basename(file)
        data = ResumeParser(file, skills_file='training_set/skill_set.csv').get_extracted_data()
        #data = ResumeParser(file).get_extracted_data()
        print(data)
        dict_skills[basename] = data['skills']
    df = pd.DataFrame(list(dict_skills.items()),columns=['file', 'skills'])
    write_file(df, dirResult+result)
    return data['skills']

def skill_normalization(skill_list, normalized_skills):
    """
    Run skill normalization to reduce vocabulary gap between two types of data

    Parameters
    ----------
    skill_list : list
        list of strings to normalize
    normalized_skills : list
        list of normalized skills to apply
    """

    skill_list = [i.lower() for i in skill_list]

    for idx, skill in enumerate(skill_list):
        highest = process.extractOne(skill, normalized_skills)
        if highest[1] == 100:
            if skill != 'c++':
                skill_list[idx] = highest[0]
    return sorted(skill_list)

def skills_from_file(csv_file):

    """
    Generate a list of skills from a csv file (one skill per column).

    Parameters
    ----------
    csv_file : string
        path to the file containing skills
    """

    skill_list = pd.read_csv(csv_file)
    skill_list = set([i.lower() for i in skill_list.columns.values.tolist()])
    
    return skill_list

def similar_products(v, n = 6):
    # https://www.analyticsvidhya.com/blog/2019/07/how-to-build-recommendation-system-word2vec-python/
    # extract most similar skills for the input vector
    ms = model.similar_by_vector(v, topn= n+1)[1:]
    return ms

def write_file(dataFrame, csv):
    dataFrame.to_csv(csv, sep='\t', encoding='utf-8')

if __name__ == '__main__':

    main = os.path.realpath(__file__).split('/')
    rootDir = '/'.join(main[:len(main)-1])

    pretrained_model = 'word2vec.model'  #saved model name
    dirModel = os.path.join(rootDir, 'model/')
    if not os.path.exists(dirModel): os.makedirs(dirModel)

    skill_file = 'training_set/skill_set.csv' #predefined list of skills for the normalization processing
    job_file = 'job_adverts/job2skills.json' # job ads to learn most frequent skill paths
    
    dirResult = os.path.join(rootDir, 'Result')
    if not os.path.exists(dirResult): os.makedirs(dirResult)
    dirResult = mkdtemp(dir = dirResult) + '/'

    parser = defaultOptions()
    options, args = parser.parse_args(sys.argv[1:])
    dirData = os.path.join(rootDir, str(args[0]))
   
    cv_skills = skill_extraction(rootDir, dirData, dirResult, 'skills_csv.csv')
    #cv_skills = ['angular', 'azure', 'c', 'css', 'data_structures', 'excel', 'git', 'html', 'javascript', 'laravel', 'linux', 'machine_learning', 'mongodb', 'nlp', 'php', 'python', 'scrum', 'unix']
    if options.recommendation:

        normalized_skills = skills_from_file(skill_file)

        if options.model:
            cv_skills = skill_normalization(cv_skills, normalized_skills)
            model = FastText.load(dirModel+pretrained_model)
        
        else:
            
            with open(job_file) as json_file:
                loaded_json = json.load(json_file)
                print('Number of jobs found ', len(loaded_json))
                #test_set = loaded_json[:50]
                test_set = loaded_json
                
            d = {str(skills[0]) : skill_normalization(skills[1], normalized_skills) for skills in test_set if len(skills[1]) != 0} 
            rows = []
            
            for key, values in d.items():
                for v in values:
                    rows.append([key, v]) 
                    
            df = pd.DataFrame(rows)
            print(df.info())
            
            job_ads = df[0].unique().tolist()
            print('Number of unique job ads :', len(df[0].unique().tolist()))
            print('Number of unique skills :', len(df[1].unique().tolist()))
            
            # shuffle customer ID's
            random.shuffle(job_ads)
            
            # extract 90% of customer ID's
            customers_train = [job_ads[i] for i in range(round(0.9*len(job_ads)))]
            
            # split data into train and validation set
            train_df = df[df[0].isin(customers_train)]
            validation_df = df[~df[0].isin(customers_train)]
            
            
            # list to capture purchase history of the customers
            purchases_train = []
            
            # populate the list with the product codes
            for i in tqdm(customers_train):
                temp = train_df[train_df[0] == i][1].tolist()
                purchases_train.append(temp)

            # list to capture purchase history of the customers
            purchases_val = []
            
            # populate the list with the product codes
            for i in tqdm(validation_df[0].unique()):
                temp = validation_df[validation_df[0] == i][1].tolist()
                purchases_val.append(temp)

            # train word2vec model
            model = FastText(window = 10, sg = 1, hs = 0,
                 negative = 10, # for negative sampling
                 alpha=0.03, min_alpha=0.0007,
                 seed = 14)
            
            model.build_vocab(purchases_train, progress_per=200)
            model.train(purchases_train, total_examples = model.corpus_count, 
                epochs=10, report_delay=1)
            model.init_sims(replace=True)

            model.save(os.path.join(dirModel, pretrained_model))
        
        final_rec = []
        for skill in cv_skills:
            try:
                recommended_skills = similar_products(model[skill])
                final_list = [skill[0] for skill in recommended_skills if skill[0] not in cv_skills and skill[0] not in final_rec and skill[1] > 0.90]
                if len(final_list) != 0 : final_rec.append(' '.join(final_list))
            except KeyError:
                pass
        
        print('recommended skill: ', ' '.join(final_rec))
