import config
import db

import urllib3, json, argparse, csv, sys, re
from datetime import datetime
from time import sleep

#################################################################

def main(args):
    '''
    :param args: dictionary of parsed command-line arguments
    '''

    form_data = get_form_data(args)
    regex = args['content_regex']
    should_store = not args['dont_store']
    should_export = args['export']
    should_notify_telegram = args['telegram']
    
    # check if default values from config file should be used
    if len(sys.argv) == 1:
        regex = config.CONTENT_REGEX
        form_data['country_code'] = config.COUNTRY_CODE
        should_store = config.STORE_INTO_DB
        should_export = config.EXPORT_RESULTS
        should_notify_telegram = config.SEND_NOTIF_TELEGRAM
    else:
        del form_data['dont_store']
        del form_data['export']
        del form_data['telegram']
        del form_data['content_regex']
        print('Command-line argument passed. Ignoring search and result values from config file...', end='\n\n')
        
    url = f"https://{form_data['country_code']}.{config.RESOURCE_PATH}"
    del form_data['country_code']
    
    jobs = request_data(url, form_data)
    if len(jobs) == 0:
        print('No matches found for given search filters')
        sys.exit() 
        
    normalized_jobs = normalize_job_data(jobs)
    filtered_jobs = filter_jobs(normalized_jobs, regex)
    filtered_job_details = filter_job_data(filtered_jobs)
    new_jobs = db.exclude_already_stored(filtered_jobs)
    
    print(f'Found {len(filtered_jobs)} job(s) that satisfy set filters.\n')
    
    
    if should_store:
        db.store_results(filtered_jobs)
    
    if should_export:
        save_to_csv(filtered_job_details)
        
    if should_notify_telegram:
        if config.TELEGRAM_BOT_TOKEN != config.FLAG_MISSING_TOKEN_ID and config.TELEGRAM_CHAT_ID != config.FLAG_MISSING_CHAT_ID:
            notify_via_telegram(new_jobs)
        else:
            print('Telegram parameters are not set. Please set valid values for "TELEGRAM_BOT_TOKEN" and "TELEGRAM_CHAT_ID" in the file: constants.py')
        
def print_program_banner():        
    '''Prints out program banner'''
    
    l = len(config.PROGRAM_NAME)
    line = "="*(l+4)
    print(f"{line}\n= {config.PROGRAM_NAME} =\n{line}")
    
def parse_arguments():
    '''Parse command-line arguments and return result on the success

    :return: dictionary of parsed command-line arguments
    '''  
    parser = argparse.ArgumentParser(description="Fetch filtered jobs from jooble.org and get results as notification")
    
    parser.add_argument('-c', '--country-code', 
                        help='upper limit for number of days since job is posted',
                        type=str,
                        default='us',
                        required='-r' in sys.argv or '--region' in sys.argv,
                        action=CountryCodeAction,
                        check_func=CountryCodeAction.__chk__)
    
    parser.add_argument('-cr', '--content-regex', 
                        help='filter jobs by job content regex)',
                        type=str,
                        default='',
                        required=False)
    
    parser.add_argument('-d', '--days-ago', 
                        help='upper limit for number of days since job is posted',
                        type=int,
                        default=0,
                        dest='date',
                        choices=[0, 1, 3, 7])
    
    parser.add_argument('-ds', '--dont-store', 
                        help='do not store results into database', 
                        action='store_true')
    
    parser.add_argument('-e', '--experience', 
                        help='required experience for a job',
                        type=str,
                        default='any',
                        choices=['any', 'intern'])
    
    parser.add_argument('-l', '--location', 
                        help='distance from selected location (in miles)',
                        type=str,
                        default='25',
                        choices=['remote', 'exect', '10', '25'])
    
    parser.add_argument('-m', '--min-salary', 
                        help='show jobs with salary greater then MIN',
                        type=int,
                        default=config.FLAG_MISSING_SALARY_LIMIT,
                        dest='salaryMin', 
                        metavar='MIN')
    
    parser.add_argument('-M', '--max-salary', 
                        help='show jobs with salary lower then MAX',
                        type=int,
                        default=config.FLAG_MISSING_SALARY_LIMIT,
                        dest='salaryMax', 
                        metavar='MAX')
    
    parser.add_argument('-r', '--region', 
                        help='filter by region in the country (-c or --country-code option is necessary for this option since region is a part of the country)',
                        type=str,
                        default='',
                        required=False)
    
    parser.add_argument('-s', '--search', 
                        help='string that will be used as search bar content',
                        type=str,
                        default='')
    
    parser.add_argument('-S', '--only-with-salary', 
                        help='exclude posts which do not have specified salary',
                        dest='withSalary', 
                        action='store_true')
    
    parser.add_argument('-T', '--telegram', 
                        help='send new (not present in DB if DB exists) results as notification (message) to telegram bot',
                        dest='telegram', 
                        action='store_true')
    
    #parser.add_argument('-t', '--job-type', 
                        #help='types of the job (period of employment for a job) which should be included in result',
                        #type=list,
                        #dest='jobTypes',
                        #choices=['full', 'temp', 'part'], 
                        #action='append')
    
    parser.add_argument('-x', '--export', 
                        help='export fetched data into CSV file', 
                        action='store_true')
    
    return vars(parser.parse_args())
    
def adapt_args_for_api(args):
    '''Adapt and validate request parameters to match Jooble's API values.

    :param args: dictionary of arguments to be adapted and valited for the API
    :return: dictionary of adapted arguments
    '''

    if 'salaryMin' in args and args['salaryMin'] == config.FLAG_MISSING_SALARY_LIMIT:
        del args['salaryMin']
        
    if 'salaryMax' in args and args['salaryMax'] == config.FLAG_MISSING_SALARY_LIMIT:
        del args['salaryMax']
    
    if 'salaryMin' in args and 'salaryMax' in args:
        if args['salaryMin'] > args['salaryMax']:
            raise ValueError('Minimal salary cannot be greater then maximal salary.')
    
    # API will treat presence of this arg as True so it should be removed if it has value False
    if 'withSalary' in args and not args['withSalary']:
        del args['withSalary']
    
    if 'experience' in args:
        if args['experience'] == 'any':
            args['experience'] = config.EXP_ANY
        elif args['experience'] == 'intern':
            args['experience'] = config.EXP_INTERSHIP
            
    if 'date' in args:
        if args['date'] == 0:
            args['date'] = config.DATE_ANY
        elif args['date'] == 1:
            args['date'] = config.DATE_1_DAY
        elif args['date'] == 3:
            args['date'] = config.DATE_3_DAYS
        elif args['date'] == 7:
            args['date'] = config.DATE_7_DAYS 
    
    if 'location' in args:
        if args['location'] == 'any':
            del args['location']
        elif args['location'] == 'remote':
            args['location'] = config.LOC_REMOTE
        elif args['location'] == 'exect':
            args['location'] = config.LOC_EXECT
        elif args['location'] == '10':
            args['location'] = config.LOC_10_MILES
        elif args['location'] == '25':
            args['location'] = config.LOC_25_MILES 
           
    #if 'jobTypes' in args:
        #for i, job_type in enumerate(args['jobTypes']):
            #if args['jobTypes'][i] == 'full':
                #args['jobTypes'][i] = config.JTYPE_FULL_TIME
            #elif args['jobTypes'][i] == 'temp':
                #args['jobTypes'][i] = config.JTYPE_TEMPORARY
            #elif args['jobTypes'][i] == 'part':
                #args['jobTypes'][i] = config.JTYPE_PART_TIME
    
    return args

def get_form_data(args):
    '''Prepare data form request form to be sent to Jooble. Depending on number of command-line arguments
    function will either use passed command-line data or data from configuration file.

    :param args: dictionary of parsed command-line arguments.
    :return: dictionary to be sent as request form data.
    '''

    if len(sys.argv) == 1:
        args = {
                'date'       : config.DATE,
                'experience' : config.EXPERIENCE,
                'location'   : config.LOCATION,
                #'jobTypes'   : config.JOB_TYPES,
                'region'     : config.REGION,
                'salaryMin'  : config.SALARY_MIN,
                'salaryMax'  : config.SALARY_MAX,
                'search'     : config.SEARCH,
                'withSalary' : config.ONLY_WITH_SALARY
            }
    return adapt_args_for_api(args)
    
def request_data(url, form_data, npage=0):
    '''Send request to Jooble's API for up to `npage` pages of results or up to `MAX_PAGES` if the `npage` 
    argument is not specified. The jobs that are part of the page are not normalized. 

    :param url: URL for Jooble's API where request will be sent.
    :param form_data: dictionary of parameters to be sent as form data.
    :return: list of dictionaries which contain non-normalized job details.
    '''

    jobs = []
    to_be_fetched = 1
    http = urllib3.PoolManager()
        
    while to_be_fetched != npage and to_be_fetched <= config.MAX_PAGES:
        form_data['page'] = to_be_fetched
        encoded_data = json.dumps(form_data).encode('utf-8')
        print("Sending request...")
        response = http.request(
            'POST',
            url,
            body=encoded_data,
            headers={'Content-Type':'application/json'}
        )
        
        print(f"Request#{to_be_fetched}\n\tServer response: {response.status}", end='')
        if response.status != 200:
            break
        
        data = json.loads(response.data)['jobs']
        print(f"; Fetch jobs: {len(data)}", end='\n\n')
        
        if len(data) == 0:
            break
        
        jobs += data
        
        # Remove HTML tag span
        for i, job in enumerate(jobs):
            jobs[i]['position'] = job['position'].replace(r'<span>', '').replace(r'</span>', '').replace(r'&nbsp', '')
            jobs[i]['content'] = job['content'].replace(r'<span>', '').replace(r'</span>', '').replace(r'&nbsp', '')
        
        to_be_fetched += 1
        
        sleep(config.REQ_DELAY)
            
    return jobs

def normalize_job_data(jobs, nested_objs=config.RESULT_NESTED_OBJS):
    '''Normalize job details by flattening nested objects and by joining multiple values
    into single value. This is done to prepare the data for other functions which require
    normalzed data to function properly.

    :param jobs: list of dictionaries which contain job details.
    :param nested_objs: list of keys of the objects that contain one or more nested objects.
    :return: list of dictionaries which contain normalized job details.
    '''

    normalized = []
    
    for job in jobs:
        # Flatten nested objects
        for nested_obj in nested_objs:
            for key, value in job[nested_obj].items():
                job[f"{nested_obj}_{key}"] = value
            del job[nested_obj]
        
        # Make the tag list atomic
        job['tags'] = ', '.join(job['tags'])
        job['tagsNew'] = ', '.join(job['tagsNew'])
        
        normalized.append(job)
        
    return normalized

def filter_job_data(jobs, keys=config.RESULT_KEYS):
    '''Filter job details by including only details whose key is in provided list of detail keys. 
    If the list is not provided then list from the configuration is used.

    :param jobs: list of dictionaries which contain job details.
    :param keys: list of detail keys that can be present in the result.
    :return: list of dictionaries which contain filtered job details.
    '''

    return [{key:value for key, value in job.items() if key in keys} for job in jobs]

def filter_jobs(jobs, content_regex=config.CONTENT_REGEX):
    '''Filter jobs by regex for job content. If the regex is not provided then list from the 
    configuration is used.

    :param jobs: list of dictionaries which contain job details.
    :param content_regex: regex to be used for filtering jobs by content.
    :return: filtered list of dictionaries which represent a job.
    '''
    
    return [job for job in jobs if re.search(content_regex, job['content'].lower())]

def save_to_csv(jobs):
    '''Save list of job details into a CSV file. The file will be saved in the directory
    from which the script was called.

    :param jobs: list of dictionaries which contain job details.
    '''

    if jobs == []:
        print('Job list is empty. Data export is aborted\n')
        return
    
    jobs = [dict(job) for job in jobs]
    print("Exporting data to csv file...")
    
    # get current time without milliseconds
    current_time = str(datetime.now()).split('.')[0]
    
    # replace spaces to avoid problems with filename
    file_name = current_time.replace(' ', '_') + '.csv'
    
    # Convert HTML bolding into markdown bolding
    for i, job in enumerate(jobs):
        for key in job:
            if isinstance(job[key], str):
                jobs[i][key] = job[key].replace('<b>', '').replace('</b>', '')
    
    with open(file_name, 'w', newline = '') as csv_file:
        csv_writer = csv.writer( csv_file, quoting=csv.QUOTE_NONNUMERIC )    
        csv_writer.writerow( list(jobs[0].keys()) )
        csv_writer.writerows( [job.values() for job in jobs] )
        
    print(f"Data is successfuly exported to '{file_name}'\n")    
    
def notify_via_telegram(jobs, url=config.TELEGRAM_BOT_URL, output_keys=config.RESULT_KEYS):
    '''Send job details as a message using Telegram bot. If bot returns status code 429 (Too Many Requests)
    program will pause for 2 seconds and then exponentialy increese that pause after each unsuccessful 
    request which received this status code. On success pause time will be restored to 2 seconds.

    Between each message sent there is a delay which lasts REQ_DELAY seconds. 
    
    :param jobs: list of dictionaries which contain job details.
    :param url: url of Telegram bot which will send the message. If not specified configuration file will be used.
    :param output_keys: ordered list of detail keys which will be included in the result. Order will be perserved. If not specified configuration file will be used.
    '''
    if jobs is None:
        return
    
    jobs = [dict(job) for job in jobs]
    http = urllib3.PoolManager()
    ord_diff = ord('a') - ord('A')
    
    for i, job in enumerate(jobs):
        html = ''
        
        for key in output_keys:
            if job[key] is not None and job[key] != '':
                # Convert HTML bolding into markdown italic
                if isinstance(job[key], str):
                    job[key] = job[key].replace('<b>', '_').replace('</b>', '_')
                    
                html += f'*{chr( ord(key[0]) - ord_diff ) + key[1:]}*: {job[key]}\n'
        
        exponential_sleep_time = 2
        while True:
            print('Sending notification to Telegram bot...')
            response = http.request(
                'POST',
                url + f'&text={html}',
                headers={'Content-Type':'application/json'}
                )
            
            print(f'Job ID: {i}; Server response: {response.status}', end='\n\n')
            if response.status == 200:
                break
            elif response.status == 429: # Too Many Requests
                sleep(exponential_sleep_time)
                exponential_sleep_time = exponential_sleep_time**2
                    
        sleep(config.REQ_DELAY)
            
    print('Data for all jobs is sent to the bot')
    
#################################################################

class CountryCodeAction(argparse.Action):
    def __init__(self, check_func, *args, **kwargs):
        """argparse custom action.
        
        :param check_func: callable to do the real check.
        """
        self._check_func = check_func
        super(CountryCodeAction, self).__init__(*args, **kwargs)
        
    def __call__(self, parser, namespace, values, option_string=None):
        #print('%r %r %r' % (namespace, values, option_string))
        
        if isinstance(values, list):
            values = [self._check_func(parser, v) for v in values]
        else:
            values = self._check_func(parser, values)
        setattr(namespace, self.dest, values)
    
    @staticmethod
    def __chk__(parser, country_code):
        if len(country_code) > 2 or not country_code.isalpha():
            raise ValueError("country code must have exactly 2 letters")
        
        return country_code
        
#################################################################

if __name__ == '__main__':
    args = parse_arguments()
    print_program_banner()
    main(args)
