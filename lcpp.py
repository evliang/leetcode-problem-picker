import glob
import sys
import os
from enum import Enum
import random
from constants import topics, blind75
import csv
from collections import defaultdict
from timeit import default_timer as timer
import datetime

ProblemType = Enum('ProblemType', 'Top Freq Easiest Hardest Common Random')

def load_completed_list():
    completed1 = set()
    with open('completed.csv', 'r') as f:
        for line in f.read().splitlines():
            try:
                completed1.add(int(line.split(',')[0].strip()))
            except ValueError:
                continue
    completed2 = load_problem_nums('completed.txt')
    # TODO handle skipped, revisit, refresh lists
    return completed1.union(completed2)

def load_problem_nums(file_name):
    ret = set()
    with open(file_name, 'r') as f:
        for num_string in f.read().split(','):
            try:
                ret.add(int(num_string.strip()))
            except ValueError:
                continue
    return ret

def pick_problems(problem_type=ProblemType.Random, categories=[], companies=[], k=5):
    completed = load_completed_list()
    skipped_hard = load_problem_nums('skipped.txt')
    revisit = load_problem_nums('revisit_later.txt')
    problem_set = set(companies) - completed - skipped_hard - revisit
    if problem_type==ProblemType.Random:
        return random.sample(list(problem_set), k)
    return []

def record_problems():
    # problem# / was completed / time spent / num mistakes (if completed)
    # internal: last attempted date, too long, easy/medium/hard, acceptance rate, thumbs up/down, number attempts
    None

if __name__ == "__main__":
    faang_companies = ['amazon', 'apple', 'google', 'netflix', 'facebook']
    my_companies = ['adobe', 'microsoft', 'airbnb', 'linkedin', 'tesla', 'twitter', 'hulu', 'redfin', 'snapchat',
                'paypal', 'pinterest', 'audible', 'atlassian', 'lyft', 'uber', 'twitch', 'twilio', 'robinhood',
                'cruise', 'reddit', 'valve', 'walmart', 'dropbox']

    all_problems = {}
    easy_set, medium_set, hard_set = set(), set(), set()
    # also store in sorted list for binsearch range lookup: https://stackoverflow.com/a/2899190

    companies = defaultdict(dict)
    problem_to_company = defaultdict(set)

    for fi in glob.glob('companies//*.csv'):
        (company,duration) = fi[10:-4].rsplit('_')
        companies[company][duration] = dict()
        with open(fi, 'r') as f:
            for line in csv.DictReader(f, fieldnames=('ID', 'Name', 'Acceptance', 'Difficulty', 'Frequency', 'Link')):
                problem_num = int(line.pop('ID'))
                all_problems[problem_num] = line
                companies[company][duration][problem_num] = line.pop('Frequency')
                problem_to_company[problem_num].add(company)

    #populate company file w/ maximum of 4 lines (sorted). each line is a comma separated list of problem numbers.
        # question: does 1yr,2yr and alltime contain 6mo? does 2yr contain 1yr? I think not?
        # 6mo
        # 1yr
        # 2yr
        # alltime
    if len(sys.argv) == 1:
        None
        #print(pick_problems(companies=blind_list, k=5))
    elif sys.argv[1] == 'interactive':
        problems = pick_problems(companies=blind75, k=5)

        companies = faang_companies + my_companies # all companies?
        d = {}
        #for company in companies:
        #    d[company] = get_the_question_set(get_frequencies([company]))

        print("Other valid inputs: info, hint, easy, hard, quit, help")
        
        for (idx,leetcode_id) in enumerate(problems):
            problem = all_problems[leetcode_id]
            msg = "First problem" if idx == 0 else "Last problem" if idx == len(problems)-1 else "Next up"
            print(f"\n\n{msg}:\n{leetcode_id}: {problem['Name']} {problem['Link']}")
            start_time = timer()
            while True:
                inp = input('When completed, enter: y/n,[num_errs],[time]\n')
                if inp == '' or inp.startswith('q'):
                    break # TODO
                if inp == 'hint':
                    ret = []
                    # problem # =>
                    #   details: name, difficulty, accept rate. need to set up dict. can just grab one from company.
                    #   [company (%)] dict from problem# => companyname => %
                    for company in d:
                        if int(inp) in d[company]:
                            ret.append(company)
                    print(f'\t {len(ret)}: ' + ', '.join(ret))
                elif inp == 'info':
                    company_list = problem_to_company[leetcode_id]
                    difficulty_string = "medium difficulty" if problem['Difficulty'] == "Medium" else "considered easy" if problem['Difficulty'] == 'Easy' else problem['Difficulty']
                    print(f"{leetcode_id} {problem['Name']} is {difficulty_string}: {problem['Acceptance']} of submissions pass")
                    print(f"{len(company_list)} have asked this question: {', '.join(company_list)}")
                elif inp.startswith('y') or inp.startswith('n'):
                    end_time = timer()
                    entry = inp.split(',')
                    was_solved = 'yes' if entry[0].startswith('y') else 'no'
                    num_errs = entry[1] if len(entry) > 1 else '0'
                    time = entry[2] if len(entry) > 2 else (start_time - end_time)//60
                    with open('completed.csv', 'a') as f:
                        f.write(f'{leetcode_id},{was_solved},{num_errs},{time},{datetime.datetime.now():%Y-%m-%d}')
                    # log entry into csv
                    break
                else:
                    print("Invalid input. Type help for options")