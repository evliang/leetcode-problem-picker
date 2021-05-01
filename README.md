# leetcode-problem-picker

## Purpose:
This project was a response to my reoccurring question *"Which leetcode problem should I do next?"*

Over time I found that the answer varies, depending on progress, needs, and goals:
1. **Topic Focus**: Narrow down to 1+ subjects e.g. "only do problems related to graphs or DP".
2. **Filtered Lists**: Honing in on questions asked by desired companies. Applies to lists like Blind's Curated 75.
3. **Level Up** (WIP): Deduces user's "skill range" for each topic in order to challenge (but not discourage).
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
info                displays details about problem. problem name, difficulty, acceptance rate
hint                displays related topics
y/n,num_errs,time   data regarding attempt. See Completed Problems section for more details
easy                mark as completed with low completion time, then selects a different problem
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