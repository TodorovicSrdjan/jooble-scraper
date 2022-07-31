################
# Script flags
FLAG_MISSING_TOKEN_ID     = ''
FLAG_MISSING_CHAT_ID      = -1
FLAG_MISSING_SALARY_LIMIT = -1

################
# General 

PROGRAM_NAME        = 'Jooble Scraper'
REQ_DELAY           = 3
MAX_PAGES           = 6
EXPORT_RESULTS      = False
SEND_NOTIF_TELEGRAM = True

TELEGRAM_BOT_TOKEN  = FLAG_MISSING_TOKEN_ID
TELEGRAM_CHAT_ID    = FLAG_MISSING_CHAT_ID

################
# Constats

## Generic
### Links
RESOURCE_PATH    = 'jooble.org/api/serp/jobs'
TELEGRAM_BOT_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=Markdown'

### Names of nested data objects inside a job object
RESULT_NESTED_OBJS = [
    'company',
    'location',
    'awayData'
    ]

### Result format
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

## Jooble-related
### Experience
EXP_ANY       = 0
EXP_INTERSHIP = 2

### Date
DATE_ANY        = 7
DATE_1_DAY      = 8
DATE_3_DAYS     = 2
DATE_7_DAYS     = 3

### Location
LOC_REMOTE   = 2
LOC_EXECT    = 4
LOC_10_MILES = 5
LOC_25_MILES = 6

### Job type
JTYPE_DEFAULT   = 0
JTYPE_FULL_TIME = 1
JTYPE_TEMPORARY = 2
JTYPE_PART_TIME = 3

################
# Default params

SEARCH        = ''
DATE          = DATE_1_DAY
LOCATION      = LOC_REMOTE
COUNTRY_CODE  = 'rs'
REGION        = ''
JOB_TYPES     = ['full', 'temp', 'part']
EXPERIENCE    = EXP_ANY

SALARY_MIN    = FLAG_MISSING_SALARY_LIMIT
SALARY_MAX    = FLAG_MISSING_SALARY_LIMIT

ONLY_WITH_SALARY = False
