# leetcode-problem-picker

## "Which problem should I do next?"

When a problem is too easy, you're wasting your time. Too difficult, and you may soon get discouraged.

During my leetcode journey, I discovered the answer to "which problems should I do next?" depend on goals and progress. I categorized these and gave them names.
1. **Topic Focus**: Narrow down to 1+ subjects e.g. "trees, graphs or DP". Intended for learning and retaining.
2. **Frequently Asked**: Questions from a list, e.g. ones asked by companies or list of Blind's Curated 75.
3. **Level Up** (WIP): Deduces user's "skill range" for each topic in order to challenge appropriately.
4. **Weighted random** (TODO): Weighted towards questions with high like count, greater like/dislike ratio, etc.

## Setup:
```git clone https://github.com/evliang/leetcode-problem-picker.git```

## Usage:
```python lcpp.py [-t stack trie graph dp] [--list airbnb google blind75 skipped] [-k 5] [-i]```

```
--topic_list -t     selects from a pool of problems associated with a subject (e.g. trie, greedy, graph)
--list -l           chooses problems from one or more text files (comma-delimited)
--num_problems -k   number of problems to get
--interactive -i    interactive mode. Preferred way to input data. See section below for more info.
note: no topic or list will result in a problem randomly being selected
```

```python lcpp.py problem_num```

Displays information about a specific problem: Name, difficulty, Acceptance rate, and a score related to how many companies ask it (last part is a TODO)

## Interactive Mode:
This mode selects and displays a single problem and waits for input:

```
info                displays details about problem: problem name, difficulty, acceptance rate
hint                displays topics related to a solution
y/n,num_errs,time   Enter data regarding attempt. See next section for details
easy                mark as completed (quickly), then selects a different problem
hard                adds to a hard/skipped list. selects a less similar, less challenging problem
revisit [ID]        mark problem as one to revisit later
refresh [ID]        mark problem as one to "refresh" on later
pause               pause the timer
break               take a break. restarts the timer
quit                stop the program
```

## Completed Problems (optional/recommended):
To maximize this program, you need to maintain a list of completed problems. This is to avoid being suggested problems you’ve done before, and in the case of "Level Up," to select problems slightly out of comfort zone
This can be done in three ways:
1. completed.txt: Format is a comma-delimited list of problem numbers e.g. "78,5,13,1337". Very simple, but not compatible with "Level Up"
2. completed.csv: One problem, one line
Expected format: ```LC number, [was solved],[time],[date],[num_errors]```
```
LC number           integer. The only required field
was solved          string. valid inputs: y/n (or yes/no). case insensitive
time                integer. number of minutes spent on the problem
date                DateTime. date completed
num_errs            float. # mistakes made. Float to differentiate minor from major errors.
```
3. interactive mode: Solve a problem after it is assigned, then record results before getting the next problem. Appends results to completed.csv.