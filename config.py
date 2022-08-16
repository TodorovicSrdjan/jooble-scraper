from constants import *

################
# Query params

# string that should be contained in job data
# Values: 
#    any string, e.g. 'developer', 'software engineer', ...
SEARCH = ''

# date since job is posted (upper limit)
# Values: 
#   DATE_ANY, DATE_1_DAY, DATE_3_DAYS, DATE_7_DAYS
DATE = DATE_1_DAY

# place where job will be performed
# Values: 
#   LOC_REMOTE, LOC_EXECT, LOC_10_MILES, LOC_25_MILES
LOCATION = LOC_REMOTE

# two-letter code of the country for which jobs are fetched
# Values: 
#   two-letter code of any country, e.g. 'rs', 'us', 'za', 'ru', ...
COUNTRY_CODE = 'rs'

# town/city in the country whose country code is COUNTRY_CODE
# Values: 
#   any town/city in the chosen contry, 
#   e.g. 'Beograd', 'Los Angeles, CA', 'Frankfurt am Main', 'Αττική' 
REGION = ''

# list of the job types which should be included in the result
# Values (for elements of the list):
#   'full', 'temp', 'part', or empty list: []
JOB_TYPES = ['full', 'temp', 'part']

# experience required for the job
# Values:
#   EXP_ANY, EXP_INTERSHIP 
EXPERIENCE = EXP_ANY

# minimum salary
# Values:
#   any value lower then value for maximum salary
SALARY_MIN = FLAG_MISSING_SALARY_LIMIT

# maximum salary
# Values:
#   any value greater then value for minimum salary
SALARY_MAX = FLAG_MISSING_SALARY_LIMIT

# defines if only jobs with displayed salary should be displayed
# Values:
#   True, False
ONLY_WITH_SALARY = False
################

################
# Request 

# delay (in seconds) between sending each request (for job fetch or notification)
# Values:
#   any non-negative float number
REQ_DELAY = 2

# maximum number of pages to be fetched if maximum number of pages is not passed
# to the request function
# Values:
#   any positive number
MAX_PAGES = 3
################

################
# Output action

# defines wheter results should be exported to a file or not
# Values:
#   True, False
EXPORT_RESULTS = True

# defines wheter results should be send to Telegram as notification or not
# Values:
#   True, False
SEND_NOTIF_TELEGRAM = False
################

################
# Regular expressions

# regular expression for filtering jobs by content
# Values:
#   any string which represents valid regular expression 
CONTENT_REGEX = ''
################

################
# list of keys whose values will be present for each job in the result (and in what order)
# Values (for elements of this list): 
#   'url','isUrlHiddenFromCrawler','uid','dateCaption','salary','content','fullContent','position',  
#   'isNew','isPremium','isEasyApply','isRemoteJob','isResumeRequired','isAdvertLabel','isFavorite', 
#   'destination','similarGroupId','impressionId','recommendId','alreadyAppliedText','hasFewApplies', 
#   'isJobLabelsDisabled','hasQuestions','projectLogoUrl','jobType','isDeleted','robots','id','tags', 
#   'company_isVerified','company_name','company_link','company_isContactsVerified','company_doesHaveHires', 
#   'company_doesHaveManyHires','company_isActiveResponses','company_logoUrl','location_name','location_link', 
#   'location_isWalkingDistanceFromAddress','location_isShiftJob','awayData_domain','awayData_link'
RESULT_KEYS = [
    'url',
    'position',
    'isRemoteJob',
    'dateCaption',
    'location_name',
    'salary',
    'content', 
    'isResumeRequired',
    'company_name',
    'company_link'
    ]
################
