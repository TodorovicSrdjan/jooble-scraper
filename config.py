################
# General 

PROGRAM_NAME   = 'Jooble Scraper'
RESOURCE_PATH  = 'jooble.org/api/serp/jobs'
REQ_DELAY      = 3
MAX_PAGES      = 6
EXPORT_RESULTS = True

################
# Constats

## Generic
### Names of nested data objects inside a job object
RESULT_NESTED_OBJS = [
    'company',
    'location',
    'awayData'
    ]

### Result format
RESULT_KEYS = [
    'url',
    'dateCaption',
    'salary',
    'content', 
    'position',
    'isRemoteJob',
    'isResumeRequired',
    'company_name',
    'company_link',
    'location_name'
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

SALARY_MIN       = 1
SALARY_MAX       = 999999
ONLY_WITH_SALARY = False
