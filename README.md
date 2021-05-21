# leetcode-problem-picker

LeetCode-Problem-Picker uses your history to select problems catered to your goals and needs.

Its purpose is to:
Track progress in order to identify and improve on areas of weakness
Choose problems that are most beneficial: frequently asked by the top tech companies
Ensure balance between all subjects with weighted rotation.

During my leetcode journey, I discovered the answer to "which problems should I do next?" depend on goals and progress:
1. **Topic Focus**: Narrow down to 1+ subjects e.g. "trees, graphs or DP". Intended for learning and focusing on weaknesses.
2. **Frequently Asked**: Questions from a list, e.g. ones asked by companies or list of Blind's Curated 75. The default.
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
To maximize this program, you need to maintain a list of completed problems. This can be done in the following ways:
1. interactive mode: After completion of each assigned problem, the result is appended to completed.csv.
2. completed.txt: Best if you have a history of solving leetcode problems. The file expects a comma-delimited list of problem numbers e.g. ```78,5,13,1337```
```
To quickly populate with leetcode data:
- Login to leetcode and visit [your list of solved problems](https://leetcode.com/problemset/all/?status=Solved). Select "All" rows per page in the bottom-left dropdown.
- Open up Developer Tools (F12) and run this line in your Console tab:
console.log(Array.from(document.querySelectorAll('.reactable-data tr td[label="#"]')).map(x => x.textContent).toString())
- Copy the list and save into completed.txt
```
3. completed.csv: The file that interactive mode writes to. Provides details about attempt. One problem per line
Expected format: ```LC number,was solved,[num_errors],[time],[date]```
```
LC number           integer
was solved          string. valid inputs: y/n (or yes/no)
num_errors          number of mistakes made when solving problem
time                amount of time spent on the problem (minutes)
date                DateTime. date completed
```