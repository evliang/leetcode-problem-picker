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
```python lcpp.py [--topic "stack,trie,graph,dp"] [--list "airbnb, blind75, to_revisit"] [-k 5] [-i]```

```
--topic -t          selects from a pool of problems associated with a subject (according to leetcode)
                    see constants.py for list of options
--list -l           chooses problems from one or more text files (comma-delimited)
--count -k          number of problems to get
--interactive -i    interactive mode. Preferred way to input data. See section below for more info.
note: no topic or list will result in a problem randomly being selected
```

```python lcpp.py problem_num```

Displays information about a specific problem: Name, difficulty, Acceptance rate, and a score related to how many companies ask it (last part is a TODO)

## Interactive Mode:
This mode selects and displays a single problem and waits for input:
(TODO: provide screenshot)

```
info                displays details about problem. problem name, difficulty, acceptance rate
hint                displays related topics
y/n,num_errs,time   data regarding attempt. See Completed Problems section for more details
easy                mark as completed with low completion time, then selects a different problem
hard                adds to a hard/skipped list. selects a less similar, less challenging problem
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

## Keeping these lists up-to-date
constants.py contains list of problem numbers associated for every subject
Also included are company files. Possibly outdated, came from another repo.

If you have leetcode premium and want to keep this info up-to-date:
1. Visit desired problem set e.g. ["Facebook"](https://leetcode.com/company/facebook/)
2. Display All rows in one page
3. open up browser's Developer Tools (F12), and from console, run

```console.log(Array.from(document.querySelectorAll('.reactable-data tr td[label="#"]')).map(x => x.textContent).toString())```

4. Copy the resulting list into text file
5. Send PR? :)

## TODO

1. Clean up and prettify what I have. Stay tuned.
2. Support multiple ways to handle completed problems
3. Improve interactive mode
4. Level Up: User maintains a list of attempted problems. Program combines this with each problem’s "acceptance rate" to approximate a "skill range" for each topic (e.g. Hard 24-28% for Trees, Medium 31-45% for graphs).
5. Weighted random