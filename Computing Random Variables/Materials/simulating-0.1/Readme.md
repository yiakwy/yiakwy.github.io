# Stimulating -- Random Alphabet

![logo](https://github.com/yiakwy/yiak.github.io/raw/master/Computing%20Random%20Variables/Materials/simulating-0.1/statics/imgs/demo.png)

## *Usage*

* A test interface for test runner. Ready for use of Random Alphabet problems like ["Given a string T of length L and pattern string P, try to find the possibility of P in T"](https://github.com/yiakwy/Onsite-Blackboard-Code-Interview/blob/master/KMP-Probability/Description.md)

* probtests.hpp contains the skeleton of the programmes.

| # | Module | Member | Functionality | members | purpose |
|---|--------|--------|---------------|---------|---------|
| 1 | probtests.hpp | alphabet\_distribution | similar to other distribution defined in C++111 \<random\> | bool (\*test\_uniform\_checking)(int) | checking the distribution sampled from a stream generated using linux seeds |
| - | - | - | - | bytes (\*operator)() | a generator; in this distribution a chacter generated per time |
| - | - | - | - | const char\* (\*historgram)(\_Tp, const char\*, char32\_t) | basic drawing for server users |
| 2 | probtests.hpp | random\_experiment\_engine | test cases runner interface | (bool)(\*single\_experiment)(char const\*, int, int) | execute once |
| - | - | - | - | string (\*templestr\_gen)(int) | random string generator || - | - | - | - | double (\*run\_ex)(const char\*, int, int, int) | random testing |  
