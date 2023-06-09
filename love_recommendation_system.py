
"""Love_Recommendation_System

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LVc3TG8s2gm2lEnzEwAhKykcl_8VuBZZ

# Love Match - Recommendation Model

## Problem Description
In a world ditacted by image and looks, imagine you can match people basing on charateristics, interets, beliefs and likes/dislikes? In other words, imagine you can match people without adding the pyhisical apparence to the math. This idea has been gaining attention after reality shows like "Love is Blind", created and streamed by Netflix, made huge success across the globe. This model aims to begin to understand what people look for in a potential partner. Then, we may have enough information to train a matchmaker recommendation model.  

## Goal
Love Recommendation with Unsupervised Machine Learning.

## Dataset description
This dataset was created with the use of a python script that pulled the data from public profiles on www.okcupid.com. It has an n=59946, which includes people within a 25 mile radius of San Francisco, who were online in the last year prior to date X, with at least one profile picture.

## Acknowledgements
This dataset is from the article: "OkCupid Data for Introductory Statistics and Data Science Courses" of the authors Kim, Albert and Escobedo-Land, Adriana published on the Journal of Statistics Education, volume 23, month 07, year 2015, numer 2 (doi = 10.1080/10691898.2015.11889737).

Links: 
*   https://jse.amstat.org/v23n2/abstracts.html
*   https://www.kaggle.com/datasets/andrewmvd/okcupid-profiles?resource=download
*   https://github.com/rudeboybert/JSE_OkCupid/tree/master

## Hypothesis
- By selecting some characterists/opinions/tastes in a person, we can have a more "compatible" match without even seeing a person's face.

## Importing Libraries
"""

import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import OneHotEncoder
import streamlit as st


"""Opening the dataset"""

ok_cupid = pd.read_csv("okcupid_profiles 2.csv")

"""Grouping categories"""

def grouping_categories(ok_cupid):
    #Status
    ok_cupid['status'] = ok_cupid['status'].replace('married', 'married or seeing someone')
    ok_cupid['status'] = ok_cupid['status'].replace('seeing someone', 'married or seeing someone')
    ok_cupid['status'] = ok_cupid['status'].replace('married or seeing someone already', 'married or seeing someone')
    ok_cupid['status'] = ok_cupid['status'].replace('available', 'unknown')

    ok_cupid["status"].value_counts()

    #Education
    #Working on or Finished Bachelor Degree
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from college/university', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from two-year college', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('college/university', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('working on college/university', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('working on two-year college', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('two-year college', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of masters program', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of law school', 'Working on or Finished Bachelor Degree')
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of med school', 'Working on or Finished Bachelor Degree')

    #Working on or Finished Graduate Degree (Masters, Law or Med School)
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from masters program', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from law school', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from med school', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('working on law school', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('working on masters program', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('working on med school', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('med school', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('masters program', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('law school', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of ph.d program', 'Working on or Finished Graduate Degree (Masters, Law or Med School)')

    #Working on or Finished ph.d Program
    ok_cupid['education'] = ok_cupid['education'].replace('working on ph.d program', 'Working on or Finished ph.d Program')
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from ph.d program', 'Working on or Finished ph.d Program')
    ok_cupid['education'] = ok_cupid['education'].replace('ph.d program', 'Working on or Finished ph.d Program')

    #Working on or Finished High School
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from high school', 'Working on or Finished High School')
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of college/university', 'Working on or Finished High School')
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of two-year college', 'Working on or Finished High School')
    ok_cupid['education'] = ok_cupid['education'].replace('high school', 'Working on or Finished High School')
    ok_cupid['education'] = ok_cupid['education'].replace('working on high school', 'Working on or Finished High School')

    #Working on or Finished Space Camp
    ok_cupid['education'] = ok_cupid['education'].replace('graduated from space camp', 'Working on or Finished Space Camp')
    ok_cupid['education'] = ok_cupid['education'].replace('working on space camp', 'Working on or Finished Space Camp')
    ok_cupid['education'] = ok_cupid['education'].replace('space camp', 'Working on or Finished Space Camp')

    #Dropped out of High School or Space Camp
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of high school', 'Dropped out of High School or Space Camp')
    ok_cupid['education'] = ok_cupid['education'].replace('dropped out of space camp', 'Dropped out of High School or Space Camp')

    ok_cupid["education"].value_counts()

    #Ethnicity
    ethnicity = ['asian', 'middle eastern', 'black', 'native american', 'indian', 'pacific islander', 'hispanic / latin', 'white', 'other']
    mixed = ok_cupid[~(ok_cupid['ethnicity'].isin(ethnicity))]
    list_mixed_races = mixed['ethnicity'].dropna().tolist()
    for value in list_mixed_races:
        ok_cupid['ethnicity'] = ok_cupid['ethnicity'].replace(value, 'mixed-ethnicity')

    ok_cupid["ethnicity"].value_counts()

    #Sign
    #gemini
    ok_cupid['sign'] = ok_cupid['sign'].replace('gemini and it&rsquo;s fun to think about', 'gemini')
    ok_cupid['sign'] = ok_cupid['sign'].replace('gemini but it doesn&rsquo;t matter', 'gemini')
    ok_cupid['sign'] = ok_cupid['sign'].replace('gemini and it matters a lot', 'gemini')

    #aries
    ok_cupid['sign'] = ok_cupid['sign'].replace('aries and it&rsquo;s fun to think about', 'aries')
    ok_cupid['sign'] = ok_cupid['sign'].replace('aries but it doesn&rsquo;t matter', 'aries')
    ok_cupid['sign'] = ok_cupid['sign'].replace('aries and it matters a lot', 'aries')

    #taurus
    ok_cupid['sign'] = ok_cupid['sign'].replace('taurus and it&rsquo;s fun to think about', 'taurus')
    ok_cupid['sign'] = ok_cupid['sign'].replace('taurus but it doesn&rsquo;t matter', 'taurus')
    ok_cupid['sign'] = ok_cupid['sign'].replace('taurus and it matters a lot', 'taurus')

    #cancer
    ok_cupid['sign'] = ok_cupid['sign'].replace('cancer and it&rsquo;s fun to think about', 'cancer')
    ok_cupid['sign'] = ok_cupid['sign'].replace('cancer but it doesn&rsquo;t matter', 'cancer')
    ok_cupid['sign'] = ok_cupid['sign'].replace('cancer and it matters a lot', 'cancer')

    #leo
    ok_cupid['sign'] = ok_cupid['sign'].replace('leo and it&rsquo;s fun to think about', 'leo')
    ok_cupid['sign'] = ok_cupid['sign'].replace('leo but it doesn&rsquo;t matter', 'leo')
    ok_cupid['sign'] = ok_cupid['sign'].replace('leo and it matters a lot', 'leo')

    #virgo
    ok_cupid['sign'] = ok_cupid['sign'].replace('virgo and it&rsquo;s fun to think about', 'virgo')
    ok_cupid['sign'] = ok_cupid['sign'].replace('virgo but it doesn&rsquo;t matter', 'virgo')
    ok_cupid['sign'] = ok_cupid['sign'].replace('virgo and it matters a lot', 'virgo')

    #libra
    ok_cupid['sign'] = ok_cupid['sign'].replace('libra and it&rsquo;s fun to think about', 'libra')
    ok_cupid['sign'] = ok_cupid['sign'].replace('libra but it doesn&rsquo;t matter', 'libra')
    ok_cupid['sign'] = ok_cupid['sign'].replace('libra and it matters a lot', 'libra')

    #scorpio
    ok_cupid['sign'] = ok_cupid['sign'].replace('scorpio and it&rsquo;s fun to think about', 'scorpio')
    ok_cupid['sign'] = ok_cupid['sign'].replace('scorpio but it doesn&rsquo;t matter', 'scorpio')
    ok_cupid['sign'] = ok_cupid['sign'].replace('scorpio and it matters a lot', 'scorpio')

    #sagittarius
    ok_cupid['sign'] = ok_cupid['sign'].replace('sagittarius and it&rsquo;s fun to think about', 'sagittarius')
    ok_cupid['sign'] = ok_cupid['sign'].replace('sagittarius but it doesn&rsquo;t matter', 'sagittarius')
    ok_cupid['sign'] = ok_cupid['sign'].replace('sagittarius and it matters a lot', 'sagittarius')

    #capricorn
    ok_cupid['sign'] = ok_cupid['sign'].replace('capricorn and it&rsquo;s fun to think about', 'capricorn')
    ok_cupid['sign'] = ok_cupid['sign'].replace('capricorn but it doesn&rsquo;t matter', 'capricorn')
    ok_cupid['sign'] = ok_cupid['sign'].replace('capricorn and it matters a lot', 'capricorn')

    #aquarius
    ok_cupid['sign'] = ok_cupid['sign'].replace('aquarius and it&rsquo;s fun to think about', 'aquarius')
    ok_cupid['sign'] = ok_cupid['sign'].replace('aquarius but it doesn&rsquo;t matter', 'aquarius')
    ok_cupid['sign'] = ok_cupid['sign'].replace('aquarius and it matters a lot', 'aquarius')

    #pisces
    ok_cupid['sign'] = ok_cupid['sign'].replace('pisces and it&rsquo;s fun to think about', 'pisces')
    ok_cupid['sign'] = ok_cupid['sign'].replace('pisces but it doesn&rsquo;t matter', 'pisces')
    ok_cupid['sign'] = ok_cupid['sign'].replace('pisces and it matters a lot', 'pisces')

    ok_cupid["sign"].value_counts()

    #Religon
    #Atheist or agnostic
    ok_cupid['religion'] = ok_cupid['religion'].replace('agnosticism', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('agnosticism but not too serious about it', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('agnosticism and laughing about it', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('agnosticism and somewhat serious about it', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('agnosticism and very serious about it', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('atheism', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('atheism and laughing about it', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('atheism but not too serious about it', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('atheism and somewhat serious about it', 'atheist or agnostic')
    ok_cupid['religion'] = ok_cupid['religion'].replace('atheism and very serious about it', 'atheist or agnostic')

    #Other
    ok_cupid['religion'] = ok_cupid['religion'].replace('other but not too serious about it', 'other')
    ok_cupid['religion'] = ok_cupid['religion'].replace('other and laughing about it', 'other')
    ok_cupid['religion'] = ok_cupid['religion'].replace('other and somewhat serious about it', 'other')
    ok_cupid['religion'] = ok_cupid['religion'].replace('other and very serious about it', 'other')

    #christianity not serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('christianity and laughing about it', 'christianity not serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('christianity but not too serious about it', 'christianity not serious')

    #christianity serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('christianity and somewhat serious about it', 'christianity serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('christianity and very serious about it', 'christianity serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('christianity', 'christianity serious')

    #judaism not serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('judaism and laughing about it', 'judaism not serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('judaism but not too serious about it', 'judaism not serious')

    #judaism serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('judaism and somewhat serious about it', 'judaism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('judaism and very serious about it', 'judaism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('judaism', 'judaism serious')

    #catholicism not serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('catholicism and laughing about it', 'catholicism not serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('catholicism but not too serious about it', 'catholicism not serious')

    #catholicism serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('catholicism and somewhat serious about it', 'catholicism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('catholicism and very serious about it', 'catholicism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('catholicism', 'catholicism serious')

    #islam not serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('islam and laughing about it', 'islam not serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('islam but not too serious about it', 'islam not serious')

    #islam serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('islam and somewhat serious about it', 'islam serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('islam and very serious about it', 'islam serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('islam', 'islam serious')

    #hinduism not serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('hinduism and laughing about it', 'hinduism not serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('hinduism but not too serious about it', 'hinduism not serious')

    #hinduism serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('hinduism and somewhat serious about it', 'hinduism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('hinduism and very serious about it', 'hinduism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('hinduism', 'hinduism serious')

    #buddhism not serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('buddhism and laughing about it', 'buddhism not serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('buddhism but not too serious about it', 'buddhism not serious')

    #buddhism serious
    ok_cupid['religion'] = ok_cupid['religion'].replace('buddhism and somewhat serious about it', 'buddhism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('buddhism and very serious about it', 'buddhism serious')
    ok_cupid['religion'] = ok_cupid['religion'].replace('buddhism', 'buddhism serious')


    ok_cupid["religion"].value_counts()

    #Diet
    #vegetarian
    ok_cupid['diet'] = ok_cupid['diet'].replace('mostly vegetarian', 'vegetarian')
    ok_cupid['diet'] = ok_cupid['diet'].replace('strictly vegetarian', 'vegetarian')

    #vegan
    ok_cupid['diet'] = ok_cupid['diet'].replace('mostly vegan', 'vegan')
    ok_cupid['diet'] = ok_cupid['diet'].replace('strictly vegan', 'vegan')

    #kosher
    ok_cupid['diet'] = ok_cupid['diet'].replace('mostly kosher', 'kosher')
    ok_cupid['diet'] = ok_cupid['diet'].replace('strictly kosher', 'kosher')

    #halal
    ok_cupid['diet'] = ok_cupid['diet'].replace('mostly halal', 'halal')
    ok_cupid['diet'] = ok_cupid['diet'].replace('strictly halal', 'halal')

    #other
    ok_cupid['diet'] = ok_cupid['diet'].replace('mostly other', 'other')
    ok_cupid['diet'] = ok_cupid['diet'].replace('strictly other', 'other')

    #anything
    ok_cupid['diet'] = ok_cupid['diet'].replace('mostly anything', 'anything')
    ok_cupid['diet'] = ok_cupid['diet'].replace('strictly anything', 'anything')

    ok_cupid["diet"].value_counts()

    #speaks
    learning_english = ok_cupid['speaks'].dropna().tolist()
    english_substitute = []
    for value in learning_english:
        if value=="english (poorly)" or value=="english (okay)":
            english_substitute.append(value)

    len(english_substitute)

    ok_cupid['speaks']

    #rename the column offsring, essay0, essay1, essay2, essay3, essay4, essay5
    new_columns_name = {"offspring": "kids", "essay0": "About me", "essay1": "What I’m doing with my life", 'essay2': "I’m really good at","essay3": "The first thing people usually notice about me", "essay4": "Favorite books, movies, show, music, and food", "essay5": "The six things I could never do without", 'essay6': "I spend a lot of time thinking about", "essay7": "On a typical Friday night I am", "essay8": "The most private thing I am willing to admit", "essay9": "You should message me if..."}
    ok_cupid = ok_cupid.rename(columns=new_columns_name)

    """## Dropping Columns"""

    #last online, location,body_type,height,ethnicity
    ok_cupid = ok_cupid.drop(labels=['location','last_online','body_type','height','ethnicity'], axis=1)

    return ok_cupid


def zodiadic_sign(individual_day, individual_month):
    day = individual_day
    month = individual_month
    if month == 12:
        astro_sign = 'Sagittarius' if (day < 22) else 'capricorn'
    elif month == 1:
        astro_sign = 'Capricorn' if (day < 20) else 'aquarius'
    elif month == 2:
        astro_sign = 'Aquarius' if (day < 19) else 'pisces'
    elif month == 3:
        astro_sign = 'Pisces' if (day < 21) else 'aries'
    elif month == 4:
        astro_sign = 'Aries' if (day < 20) else 'taurus'
    elif month == 5:
        astro_sign = 'Taurus' if (day < 21) else 'gemini'
    elif month == 6:
        astro_sign = 'Gemini' if (day < 21) else 'cancer'
    elif month == 7:
        astro_sign = 'Cancer' if (day < 23) else 'leo'
    elif month == 8:
        astro_sign = 'Leo' if (day < 23) else 'virgo'
    elif month == 9:
        astro_sign = 'Virgo' if (day < 23) else 'libra'
    elif month == 10:
        astro_sign = 'Libra' if (day < 23) else 'scorpio'
    elif month == 11:
        astro_sign = 'scorpio' if (day < 22) else 'sagittarius'
    return astro_sign

def dataset_filter(ok_cupid_clean, filters):
    result = ok_cupid_clean.copy()

    bisexual = [f["value"] for f in filters if f["column"]=="to_exclude"]
    if len(bisexual) > 0:
        result = result.query(bisexual[0])

    for filter in filters:
        column = filter['column']
        value = filter['value']
        if column == "to_exclude":
            pass
        else:
            if isinstance(value,list):
                if isinstance(value[0],str):
                    result = result.loc[result[column].isin(value)]
                else:
                    result = result.loc[result[column].between(value[0],value[-1])]
            else:   
                result = result.loc[result[column]==value]
            
    return result

def columns_enconder(recommendations):
    user = pd.DataFrame()
    for key,value in recommendations.items():
        if isinstance(value,(str,int,float)):
            user[f'{key}_{value}'] = [1]
        else:
            for v in value:
                user[f'{key}_{v}'] = [1]
    return user

#order_recommendations = dataset_recommendation(ok_cupid_clean, filters, recommendations_dummy,columns=recommendations.keys())

def dataset_recommendation(ok_cupid_clean, filters, recommendations,columns):
    encoder = OneHotEncoder()

    result_test = dataset_filter(ok_cupid_clean, filters)
    if len(result_test)==0: 
        return "It was not possible to find an ideal match. Please, dismiss some dealbreaker(s) to continue."
    
    result_test_recommendation = result_test[columns]
    result_dummy = encoder.fit_transform(result_test_recommendation)
    result_dummy_dataframe = pd.DataFrame(result_dummy.toarray(), columns=encoder.get_feature_names_out())
    missing_columns = set(result_dummy_dataframe)-set(recommendations.columns)

    for c in missing_columns:
        recommendations[c] = [0]
    
    recommendations = recommendations[result_dummy_dataframe.columns]
    return pd.DataFrame(1/(1+pairwise_distances(result_dummy,recommendations)),index=result_test.index).sort_values(by=0, ascending = False)