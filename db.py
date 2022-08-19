from constants import DB_FILE_PATH

import sqlite3
import os

#################################################################

def store_results(jobs):
    '''Store results into a database.
    
    :param jobs: list of dictionaries which contain job details.
    '''
    
    if len(jobs) == 0:
        return
    
    con = sqlite3.connect(DB_FILE_PATH)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS jobs
        (uid integer primary key, url text, isUrlHiddenFromCrawler integer, dateCaption text, salary integer, content text, fullContent text,
        position text, isNew integer, isPremium integer, isEasyApply integer, isRemoteJob integer, isResumeRequired integer, 
        isAdvertLabel integer, isFavorite integer, destination text, similarGroupId integer, impressionId integer, recommendId integer, 
        alreadyAppliedText text, hasFewApplies integer, isJobLabelsDisabled integer, hasQuestions integer, projectLogoUrl text, 
        jobType text, isDeleted integer, robots text, id integer, tags text, tagsNew text, company_isVerified integer,  company_name text, 
        company_link text, company_isContactsVerified integer, company_doesHaveHires integer, company_doesHaveManyHires integer,
        company_isActiveResponses integer, company_logoUrl text, location_name text, location_link text, 
        location_isWalkingDistanceFromAddress integer, location_isShiftJob integer, awayData_domain text, awayData_link text)'''
        )
    
    tuple_jobs = [tuple(job.values()) for job in jobs]
    keys = jobs[0].keys()
    keys_str = ', '.join(keys)
    
    placeholders = ', '.join('?'*len(keys))
    
    query = f"INSERT INTO jobs ({keys_str}) VALUES ({placeholders});"
    for job in tuple_jobs:
        with con:
            try:
                cur.execute(query, job)
            except sqlite3.IntegrityError:
                print(f"Job with uid {job[tuple(keys).index('uid')]} is already stored. Ignoring...")
            else:
                con.commit()
    
    if len(jobs) != con.total_changes:
        print()
            
    print("Result storing is complete. \nNumber of results that are stored this execution:", con.total_changes)
    cur.close()
    con.close()
