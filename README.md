# leetcode-problem-picker

## Original motivation:
A quick answer to the question "Which leetcode problem should I do next?" Because randomly choosing from 1750 questions wasn’t cutting it for me.

## Modes
The answer to that question depends on different needs and goals:
1. Topic Focus: Narrow down to just a few subjects e.g. "only problems related to graphs, tries, and DP".
2. Filtered Lists: Which problems were frequently asked by companies I’m interested in? Also lists like Blind 75
3. Level Up (WIP): Deduces user's "skill range" for each topic in order to challenge (but not discourage).
4. Weighted random (TODO): Weighted towards high like count, high like-dislike ratio, etc.

# State of leetcode-problem-picker
![WIP](https://i.ibb.co/BcSX334/WIP.png)

I wish to share and help others, but what I currently have and use is a product of months of ideas. It is neither presentable nor ready for public consumption. What you see now is just a bunch of stubs.

**If you are interested in this idea, please star this repo** and give me a week or so to clean it up.

## Setup:
```git clone https://github.com/evliang/leetcode-problem-picker.git```

## Usage:
```python lcpp.py [--topic "stack,trie,graph,dp"] [--list "airbnb, blind75, to_revisit"] [-k 5] [-i]```

```
--topic -t          selects from a pool of problems associated with a subject (according to leetcode)
                    options are: array/arr, string/str, hash/hash table, linked list/ll, math, two-pointers/2ptr, binary search/binsearch, divide and conquer, dp/dynamic programming, backtrack(ing), stack/stk, heap, greedy, sort, bit (manipulation), tree, dfs, bfs, union-find, graph, design, top sort, trie, recursion, queue/q, sliding window
--list -l           chooses problems from one or more text files (comma-delimited)
--count -k          number of problems to get
--interactive -i    interactive mode. Another way to input data (and it auto-populates the date). See section below for more information.
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
num_errs            float. errors made while solving the problem. Float because I differentiate minor from major errors.
```
3. interactive mode: Solve a problem after it is assigned, then record results before getting the next problem. Appends results to completed.csv.

## Information regarding lists:
Included in this repo are txt files for each topic. Each one is a comma-separated list of problem #s associated with that subject (provided by leetcode).
Also included are company files. Snatched from a github repo, possibly outdated. See section below if you have leetcode premium and want to keep this info up-to-date.

## How to maintain up-to-date lists
After visiting leetcode in browser, open a page with a problem list (e.g. load up Linked List problems and load All problems in one page)
Then, from Developer Tools, run

```console.log(Array.from(document.querySelectorAll('.reactable-data tr td[label="#"]')).map(x => x.textContent).toString())```

And copy the list into text file

## TODO

1. Refactor what I have. Stay tuned.
2. Level Up: User maintains a list of attempted problems. Program combines this with each problem’s "acceptance rate" to approximate a "skill range" for each topic (e.g. Hard 24-28% for Trees, Medium 31-45% for graphs).