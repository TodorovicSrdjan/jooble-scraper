################
# Script flags
FLAG_MISSING_TOKEN_ID     = ''
FLAG_MISSING_CHAT_ID      = -1
FLAG_MISSING_SALARY_LIMIT = -1
################

################
# General 
PROGRAM_NAME       = 'Jooble Scraper'
TELEGRAM_BOT_TOKEN = '5576098565:AAGTxy01G9LnuTkh-kOWH1aqfzgGsJeSOtY'
TELEGRAM_CHAT_ID   = 955586611
################

#############################################################################
# DO NOT CHANGE ANYTHING BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING #
#############################################################################

################
# Links
RESOURCE_PATH    = 'jooble.org/api/serp/jobs'
TELEGRAM_BOT_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=Markdown'
################

################
# Names of nested data objects inside a job object
RESULT_NESTED_OBJS = [
    'company',
    'location',
    'awayData'
    ]
################

################
# Jooble API specific
## Experience
EXP_ANY       = 0
EXP_INTERSHIP = 2

## Date
DATE_ANY    = 7
DATE_1_DAY  = 8
DATE_3_DAYS = 2
DATE_7_DAYS = 3

## Location
LOC_REMOTE   = 2
LOC_EXECT    = 4
LOC_10_MILES = 5
LOC_25_MILES = 6

## Job type
JTYPE_DEFAULT   = 0
JTYPE_FULL_TIME = 1
JTYPE_TEMPORARY = 2
JTYPE_PART_TIME = 3
################
