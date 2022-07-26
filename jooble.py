import config

import urllib3, json, argparse, csv, sys
from datetime import datetime
from time import sleep

#################################################################

class CountryCodeAction(argparse.Action):
    def __init__(self, check_func, *args, **kwargs):
        """
        argparse custom action.
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

def main(args):
    form_data = get_form_data(args)
    should_export = args['export']
    
    # check if default values from config file should be used
    if len(sys.argv) == 1:
        form_data['country_code'] = config.COUNTRY_CODE
        should_export = config.EXPORT_RESULTS
        
    url = f"https://{form_data['country_code']}.{config.RESOURCE_PATH}"
    del form_data['country_code']
    
    jobs = request_data(url, form_data)
    if len(jobs) == 0:
        print('No matches found for given search filters')
        sys.exit()
        
    normalized_jobs = normalize_job_data(jobs)
    filtered_jobs = filter_job_data(normalized_jobs)
    
    if should_export:
        save_to_csv(normalized_jobs)
        
'''
Prints out program banner
'''
def print_program_banner():
    l = len(config.PROGRAM_NAME)
    line = "="*(l+4)
    print(f"{line}\n= {config.PROGRAM_NAME} =\n{line}")
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch and get notification for filtered jobs from jooble.org")
    
    parser.add_argument('-c', '--country-code', 
                        help='upper limit for number of days since job is posted',
                        type=str,
                        default='us',
                        required='-r' in sys.argv or '--region' in sys.argv,
                        action=CountryCodeAction,
                        check_func=CountryCodeAction.__chk__)
    
    parser.add_argument('-d', '--days-ago', 
                        help='upper limit for number of days since job is posted',
                        type=int,
                        default=0,
                        dest='date',
                        choices=[0, 1, 3, 7])
    
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
                        default=1,
                        dest='salaryMin', 
                        metavar='MIN')
    
    parser.add_argument('-M', '--max-salary', 
                        help='show jobs with salary lower then MAX',
                        type=int,
                        default=999999,
                        dest='salaryMax', 
                        metavar='MAX')
    
    parser.add_argument('-r', '--region', 
                        help='filter by region in the country (-c or --country-code option is necessary for this option since region is part of the country)',
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
    if 'salaryMin' in args and 'salaryMax' in args:
        if int(args['salaryMin']) > int(args['salaryMax']):
            raise ValueError('Minimal salary cannot be greater then maximal salary.')
    
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
            args['date'] = DATE_7_DAYS 
    
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
    jobs = []
    to_be_fetched = 1
    http = urllib3.PoolManager()
        
    while to_be_fetched != npage and to_be_fetched != config.MAX_PAGES:
        form_data['page'] = to_be_fetched
        encoded_data = json.dumps(form_data).encode('utf-8')
        print("Sending request...")
        response = http.request(
            'POST',
            url,
            body=encoded_data,
            headers={'Content-Type':'application/json'}
        )
        
        print(f"Request ID: {to_be_fetched}; Server response: {response.status}", end='')
        if response.status != 200:
            break
        
        data = json.loads(response.data)['jobs']
        print(f"; Fetch jobs: {len(data)}", end='\n\n')
        
        if len(data) == 0:
            break
        
        jobs += data
        to_be_fetched += 1
        
        sleep(config.REQ_DELAY)
            
    return jobs

def normalize_job_data(jobs, nested_objs=config.RESULT_NESTED_OBJS):
    normalized = []
    
    for job in jobs:
        # Flatten nested objects
        for nested_obj in nested_objs:
            for key, value in job[nested_obj].items():
                job[f"{nested_obj}_{key}"] = value
            del job[nested_obj]
        
        # Make the tag list atomic
        job['tags'] = ', '.join(job['tags'])
        
        normalized.append(job)
        
    return normalized

def filter_job_data(jobs, keys=config.RESULT_KEYS):
    return [{key:value for key, value in job.items() if key in keys} for job in jobs]

def save_to_csv(jobs):
    if jobs == []:
        print('Job list is empty. Data export is aborted')
        return
    
    print("Exporting data...")
    
    # get current time without milliseconds
    current_time = str(datetime.now()).split('.')[0]
    
    # replace spaces to avoid problems with filename
    file_name = current_time.replace(' ', '_') + '.csv'
    
    with open(file_name, 'w', newline = '') as csv_file:
        csv_writer = csv.writer( csv_file, quoting=csv.QUOTE_NONNUMERIC )    
        csv_writer.writerow( list(jobs[0].keys()) )
        csv_writer.writerows( [job.values() for job in jobs] )
        
    print(f"Data is successfuly exported to '{file_name}'")    
    
if __name__ == '__main__':
    args = parse_arguments()
    print_program_banner()
    main(args)
