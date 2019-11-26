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

from pyresparser import ResumeParser
from fuzzywuzzy import process
import numpy as np
from gensim.models import FastText
from tqdm import tqdm

class Skillator(object):
    def __init__(self, filename):
        main = os.path.realpath(__file__).split('/')
        self.rootDir = '/'.join(main[:len(main)-2])
        self.dirModel = os.path.join(self.rootDir, 'model/')
        if not os.path.exists(self.dirModel): os.makedirs(self.dirModel)

        self.skill_file = 'training_set/skill_set.csv' #predefined list of skills for the normalization processing
        self.job_file = 'job_adverts/job2skills.json' # job ads to learn most frequent skill paths

        self.dirResult = os.path.join(self.rootDir, 'Result')
        if not os.path.exists(self.dirResult): os.makedirs(self.dirResult)
        self.dirResult = mkdtemp(dir = self.dirResult) + '/'

        self.cv = filename

    def skill_extraction(self, cv) :
        data = ResumeParser(cv, skills_file= os.path.join(self.rootDir, 'training_set/skill_set.csv')).get_extracted_data()
        return data['name'], data['skills']


    def skill_normalization(self, skill_list, normalized_skills):
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

    def skills_from_file(self, csv_file):

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

    def similar_products(self, v, n = 6):
        # https://www.analyticsvidhya.com/blog/2019/07/how-to-build-recommendation-system-word2vec-python/
        # extract most similar skills for the input vector
        ms = model.similar_by_vector(v, topn= n+1)[1:]
        return ms


if __name__ == '__main__':
    skill_class = Skillator('resumes/OmkarResume.pdf')
    cv_skills = skill_class.skill_extraction(os.path.join(skill_class.rootDir, skill_class.cv))
    normalized_skills = skills_from_file(os.path.join(skill_class.rootDir, skill_class.skill_file))
    
    cv_skills = skill_normalization(cv_skills, normalized_skills)
    model = FastText.load(os.path.join(skill_class.dirModel, 'word2vec.model'))

    final_rec = []
    for skill in cv_skills:
        try:
            recommended_skills = similar_products(model[skill])
            final_list = [skill[0] for skill in recommended_skills if skill[0] not in cv_skills and skill[0] not in final_rec and skill[1] > 0.90]
            if len(final_list) != 0 : final_rec.append(' '.join(final_list))
        except KeyError:
            pass
        
    print('recommended skill: ', ' '.join(final_rec))


