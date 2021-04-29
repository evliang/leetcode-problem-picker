import glob
import sys
import os
from enum import Enum
import random
from constants import topics

ProblemType = Enum('ProblemType', 'Top Freq Easiest Hardest Common Random')

def load_completed():
    # completed.csv
    with open('completed.csv', 'r') as f:
        completed1 = f.read().splitlines()
    # completed.txt
    with open('completed.txt', 'r') as f:
        completed2 = f.read().splitlines()
    # merge

    # handle skipped, revisit, refresh lists
    return set()

def pick_problems(problem_type=ProblemType.Random, categories=[], companies=[], k=5):
    problem_set = set(companies) - completed - skipped_hard - revisit
    if problem_type==ProblemType.Random:
        return random.sample(list(problem_set), k)
    return []

def record_problems():
    # problem# / was completed / time spent / num mistakes (if completed)
    # internal: last attempted date, too long, easy/medium/hard, acceptance rate, thumbs up/down, number attempts
    None

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(pick_problems(companies=blind_list, k=5))
    elif sys.argv[1] == 'interactive':
        probs = pick_problems(companies=blind_list, k=5)
        print(probs)

        companies = faang_companies + my_companies # all companies?
        d = {}
        for company in companies:
            d[company] = get_the_question_set(get_frequencies([company]))

        while True:
            inp = input('leetcode ID? ')
            if inp == '' or inp.startswith('q'):
                break
            if inp.isdigit():
                ret = []
                # problem # =>
                #   details: name, difficulty, accept rate. need to set up dict. can just grab one from company.
                #   [company (%)] dict from problem# => companyname => %
                for company in d:
                    if int(inp) in d[company]:
                        ret.append(company)
                print(f'\t {len(ret)}: ' + ', '.join(ret))
