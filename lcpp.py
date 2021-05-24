import glob
import sys
import os
from enum import Enum
import random
from constants import topics
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
    selected_topics = set(itertools.chain(*[topics.get(topic,[]) for topic in topic_list]))

    skip_set = set(load_completed_list(user_data))
    for maybe_skip in ['hard', 'revisit', 'refresh']:
        skip_set.update(user_data[maybe_skip] if maybe_skip not in args.list else [])

    problem_set = (set(problems) & selected_topics) - skip_set
    if problem_type==ProblemType.Random:
        return random.sample(list(problem_set), min(len(problem_set),k))
    return []

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
    parser.add_argument('--num_problems', '-k', type=int, default=5, help="Determine number of problems to solve")

    args = parser.parse_args()

    user_data = load_user_data()

    easy_set, medium_set, hard_set = set(), set(), set()
    # also store in sorted list for binsearch range lookup: https://stackoverflow.com/a/2899190

    problem_to_companies = load_json('problem_to_companies.json')
    company_to_problems = load_json('company_to_problems.json')
    all_problems = load_json('all_problems.json')
    my_companies = set(user_data["faang"] + user_data["my_companies"])

    #populate company file w/ maximum of 4 lines (sorted). each line is a comma separated list of problem numbers.
        # question: does 1yr,2yr and alltime contain 6mo? does 2yr contain 1yr? I think not?
        # 6mo
        # 1yr
        # 2yr
        # alltime
    problem_set = set()
    for elem in args.list:
        if elem in company_to_problems:
            for duration in company_to_problems[elem]:
                problem_set.update([int(leetcode_id) for leetcode_id in company_to_problems[elem][duration]])
        elif elem.lower() in user_data:
            # load from file
            problem_set.update(user_data[elem.lower()])

    if args.interactive:
        problems = pick_problems(user_data, problems=problem_set, topic_list=args.topic_list, k=args.num_problems)
        problem_set -= set(problems)

        if len(problems) == 0:
            print("You have completed all the problems in the selected set. Re-picking from the entire problem set")
            problems = pick_problems(user_data, problems=set(range(1,1700)), topic_list=args.topic_list, k=args.num_problems)
        if len(problems) == 0:
            print("Your --topic_list is either invalid or all completed. Repicking from all topics.")
            problems = pick_problems(user_data, problems=problem_set, topic_list=topics.keys(), k=args.num_problems)

        valid_inputs = ["info", "hint", "easy", "hard", "quit", "pause", "break"]
        print(f"Other valid inputs: {', '.join(valid_inputs)}")
        
        for (idx,leetcode_id) in enumerate(problems):
            problem = all_problems[str(leetcode_id)]
            msg = "First problem" if idx == 0 else "Last problem" if idx == args.num_problems-1 else "Next up"
            print(f"\n{msg}:\n{leetcode_id}: {problem['Name']} {problem['Link']}")
            start_time = timer()
            while True:
                inp = input('When completed, enter: y/n,[num_errs],[time]\n')
                if inp.startswith('q'):
                    quit()
                if inp == 'hint':
                    # TODO need problem to topic dictionary
                    raise Exception("Not Implemented Yet")
                elif inp == 'info':
                    difficulty_string = "medium difficulty" if problem['Difficulty'] == "Medium" else "considered easy" if problem['Difficulty'] == 'Easy' else problem['Difficulty']
                    print(f"{leetcode_id} {problem['Name']} is {difficulty_string}: {problem['Acceptance']} of submissions pass")
                    company_list = my_companies & set(problem_to_companies[str(leetcode_id)])
                    company_list_string = f"including: {', '.join(company_list)}" if len(company_list) > 0 else f"including: {','.join(problem_to_companies[str(leetcode_id)][:5])}"
                    print(f"{len(company_list)} companies have asked this question {company_list_string}")
                elif inp == 'pause':
                    pause_time = timer()
                    input("Paused. Press Enter to continue the clock\n")
                    start_time = pause_time - start_time + timer()
                elif inp == 'break':
                    input("Paused. Press Enter to reset the clock and start the problem\n")
                    start_time = timer()
                elif inp == 'easy':
                    mark_completed(leetcode_id, 'yes', '0', '5')
                    # Replace with new problem not in problems
                    leetcode_id = pick_problems(user_data, problems=problem_set, topic_list=args.topic_list, k=1)[0]
                    problem_set.discard(leetcode_id)
                    problem = all_problems[str(leetcode_id)]
                    print(f"\n{msg}:\n{leetcode_id}: {problem['Name']} {problem['Link']}")
                    start_time = timer()
                elif inp == 'hard':
                    mark_problem(user_data, 'hard', leetcode_id)
                    leetcode_id = pick_problems(user_data, problems=problem_set, topic_list=args.topic_list, k=1)[0]
                    problem_set.discard(leetcode_id)
                    problem = all_problems[str(leetcode_id)]
                    print(f"\n{msg}:\n{leetcode_id}: {problem['Name']} {problem['Link']}")
                    # TODO pick problem with same topic and higher acceptance rate (if possible). If none, default to above line
                    start_time = timer()
                elif inp == 'skip':
                    leetcode_id = pick_problems(user_data, problems=problem_set, topic_list=args.topic_list, k=1)[0]
                    start_time = timer()
                elif inp.startswith('revisit'):
                    marked_id = int(inp.split(' ')[1]) if len(inp.split(' ')) > 0 else leetcode_id
                    mark_problem(user_data, 'revisit', marked_id)
                elif inp.startswith('refresh'):
                    marked_id = int(inp.split(' ')[1]) if len(inp.split(' ')) > 0 else leetcode_id
                    mark_problem(user_data, 'refresh', marked_id)
                elif inp.startswith('y') or inp.startswith('n'):
                    # log entry into csv
                    entry = inp.split(',')
                    was_solved = 'yes' if entry[0].startswith('y') else 'no'
                    num_errs = entry[1] if len(entry) > 1 else '0'
                    true_time = round((timer()-start_time)/60)
                    time = entry[2] if len(entry) > 2 else true_time

                    mark_completed(leetcode_id, was_solved, num_errs, time)
                    print(f"completed in {true_time}min")
                    break
                elif inp == 'help':
                    #print_help_screen()
                    print("TODO. For now, read the code or just try it out")
                    None
                else:
                    print(f"Invalid input. Type help for more options")
    else:
        print(pick_problems(user_data, problems=problem_set, topic_list=args.topic_list, k=args.num_problems))