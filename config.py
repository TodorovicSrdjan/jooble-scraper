################
# General 

PROGRAM_NAME   = "Jooble Scraper"
RESOURCE_PATH  = "jooble.org/api/serp/jobs"
REQ_DELAY      = 4
MAX_PAGES      = 6

################
# Constats

## Generic
### Nested objects inside job object
RESULT_NESTED_OBJS=['company', 'location', 'awayData']

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
LOCATION      = LOC_25_MILES
COUNTRY_CODE  = "rs"
REGION        = ''
JOB_TYPES     = ['full', 'temp', 'part']
EXPERIENCE    = EXP_INTERSHIP

SALARY_MIN       = 1
SALARY_MAX       = 999999
ONLY_WITH_SALARY = False
