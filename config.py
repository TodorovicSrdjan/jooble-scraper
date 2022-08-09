from constants import *

################
# Query params
SEARCH           = ''
DATE             = DATE_1_DAY
LOCATION         = LOC_REMOTE
COUNTRY_CODE     = 'rs'
REGION           = ''
JOB_TYPES        = ['full', 'temp', 'part']
EXPERIENCE       = EXP_ANY
SALARY_MIN       = FLAG_MISSING_SALARY_LIMIT
SALARY_MAX       = FLAG_MISSING_SALARY_LIMIT
ONLY_WITH_SALARY = False
################

################
# Request 
REQ_DELAY = 3
MAX_PAGES = 6
################

################
# Output action
EXPORT_RESULTS      = False
SEND_NOTIF_TELEGRAM = True
################

################
# Result format
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
