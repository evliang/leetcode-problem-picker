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
import argparse
import itertools
import json
import re

ProblemType = Enum('ProblemType', 'Top Freq Easiest Hardest Common Random')

def load_completed_list(user_data):
    completed1 = set()
    with open('completed.csv', 'r') as f:
        for line in f.read().splitlines():
            try:
                completed1.add(int(line.split(',')[0].strip()))
            except ValueError:
                continue
    completed2 = set(user_data["completed"])
    # TODO handle skipped, revisit, refresh lists
    return completed1.union(completed2)

def load_json(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def load_user_data():
    return load_json('user.json')

def pick_problems(user_data, problems, topic_list, k=5, problem_type=ProblemType.Random):
    completed = load_completed_list(user_data)

    skipped_hard = user_data['hard']
    revisit = user_data['revisit']

    selected_topics = set(itertools.chain(*[topics[topic] for topic in topic_list]))
    problem_set = (set(problems) & selected_topics) - completed - skipped_hard - revisit
    if problem_type==ProblemType.Random:
        return random.sample(list(problem_set), k)
    return []

def writef():
    with open('user.json', 'w') as f:
        f.write(re.sub(r',\n    ', ',', json.dumps(d, indent=2)))

def mark_completed(leetcode_id, was_solved, num_errs, time):
    # problem# / was completed / time spent / num mistakes (if completed)
    # todo: internally track: last attempted date, too long, easy/medium/hard, acceptance rate, thumbs up/down, number attempts
    with open('completed.csv', 'a') as f:
        f.write(f'\n{leetcode_id},{was_solved},{num_errs},{time},{datetime.datetime.now():%Y-%m-%d}')

def mark_problem(user_data, mark_type, leetcode_id):
    user_data[mark_type].append(leetcode_id)
    with open('user.json', 'w') as f:
        f.write(re.sub(r',\n    ', ',', json.dumps(user_data, indent=2)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="",

    )
    parser.add_argument('--interactive', '-i', action='store_true', default=False, help='Easily log results while doing leetcode problems')
    parser.add_argument('--topic_list', '-t', nargs='+', default=topics.keys(),
                        help='List of subjects to filter on'
                             'Options are:'
                             'array hash table ll greedy backtrack graph etc')
    parser.add_argument('--list', '-l', nargs='+', default=['blind75'], help="Companies interested in (or file(s) containing comma-delimited problems)")
    parser.add_argument('--num_problems', '-k', type=int, default=5, choices=range(1,50), help="Determine number of problems to solve")

    args = parser.parse_args()

    user_data = load_user_data()
    mark_problem(user_data, 'hard', 3)
    mark_problem(user_data, 'hard', 7)
    mark_problem(user_data, 'hard', 76)
    mark_problem(user_data, 'revisit', 3)
    mark_problem(user_data, 'revisit', 5)
    mark_problem(user_data, 'refresh', 268)

    faang_companies = ['amazon', 'apple', 'google', 'netflix', 'facebook']
    my_companies = ['adobe', 'microsoft', 'airbnb', 'linkedin', 'tesla', 'twitter', 'hulu', 'redfin', 'snapchat',
                'paypal', 'pinterest', 'audible', 'atlassian', 'lyft', 'uber', 'twitch', 'twilio', 'robinhood',
                'cruise', 'reddit', 'valve', 'walmart', 'dropbox']

    easy_set, medium_set, hard_set = set(), set(), set()
    # also store in sorted list for binsearch range lookup: https://stackoverflow.com/a/2899190

    with open('problem_to_companies.json') as json_file:
        problem_to_companies = json.load(json_file)
    
    with open('company_to_problems.json') as json_file:
        company_to_problems = json.load(json_file)
    
    with open('all_problems.json') as json_file:
        all_problems = json.load(json_file)

    #populate company file w/ maximum of 4 lines (sorted). each line is a comma separated list of problem numbers.
        # question: does 1yr,2yr and alltime contain 6mo? does 2yr contain 1yr? I think not?
        # 6mo
        # 1yr
        # 2yr
        # alltime
    full_list = set()
    for elem in args.list:
        if elem in company_to_problems:
            for duration in company_to_problems[elem]:
                full_list.add(company_to_problems[elem][duration])
        elif elem.lower() in user_data:
            # load from file
            full_list.update(user_data[elem.lower()])

    if args.interactive:
        problems = pick_problems(user_data, problems=full_list, topic_list=args.topic_list, k=args.num_problems)

        companies = faang_companies + my_companies # all companies?
        d = {}
        #for company in companies:
        #    d[company] = get_the_question_set(get_frequencies([company]))

        valid_inputs = ["info", "hint", "easy", "hard", "quit", "pause", "break"]
        print(f"Other valid inputs: {', '.join(valid_inputs)}")
        
        for (idx,leetcode_id) in enumerate(problems):
            problem = all_problems[leetcode_id]
            msg = "First problem" if idx == 0 else "Last problem" if idx == len(problems)-1 else "Next up"
            print(f"\n{msg}:\n{leetcode_id}: {problem['Name']} {problem['Link']}")
            start_time = timer()
            while True:
                inp = input('When completed, enter: y/n,[num_errs],[time]\n')
                if inp.startswith('q'):
                    quit()
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
                    company_list = problem_to_companies[leetcode_id]
                    difficulty_string = "medium difficulty" if problem['Difficulty'] == "Medium" else "considered easy" if problem['Difficulty'] == 'Easy' else problem['Difficulty']
                    print(f"{leetcode_id} {problem['Name']} is {difficulty_string}: {problem['Acceptance']} of submissions pass")
                    print(f"{len(company_list)} have asked this question: {', '.join(company_list)}")
                elif inp == 'pause':
                    input("Paused. Press Enter to continue the clock\n")
                elif inp == 'break':
                    input("Paused. Press Enter to reset the clock and start the problem\n")
                    start_time = timer()
                elif inp == 'easy':
                    # Replace with new problem not in problems
                    partial_list = list(set(full_list) - set(problems))
                    leetcode_id = pick_problems(user_data, problems=partial_list, topic_list=args.topic_list, k=1)[0]
                elif inp == 'hard':
                    mark_problem(user_data, 'hard', leetcode_id)
                elif inp.startswith('revisit'):
                    leetcode_id = inp.split(' ')[1] if len(inp.split(' ')) > 0 else leetcode_id
                    mark_problem(user_data, 'revisit', leetcode_id)
                elif inp.startswith('refresh'):
                    leetcode_id = inp.split(' ')[1] if len(inp.split(' ')) > 0 else leetcode_id
                    mark_problem(user_data, 'refresh', leetcode_id)
                elif inp.startswith('y') or inp.startswith('n'):
                    # log entry into csv
                    entry = inp.split(',')
                    was_solved = 'yes' if entry[0].startswith('y') else 'no'
                    num_errs = entry[1] if len(entry) > 1 else '0'
                    time = entry[2] if len(entry) > 2 else (timer() - start_time)//60

                    mark_completed(leetcode_id, was_solved, num_errs, time)
                    break
                elif inp == 'help':
                    #print_help_screen()
                    print("TODO. For now, read the code or just try it out")
                    None
                else:
                    print(f"Invalid input. Type help for more options")
    else:
        print(pick_problems(user_data, problems=full_list, topic_list=args.topic_list, k=args.num_problems))