Unzip the package and either import it to an IDE or in a terminal run the following command from the correct directory:
    py -YourPythonVersion main.py
Example with python3:
    py -3 main.py

The two following packages needs to be installed:
    sympy
    itertools

When running the program you can make a belief state with any of the following symbols:
    ~ (negation)
    & (and)
    | (or)
    >> (implication)
    <-> (bi-implication)
    () (grouping)

If multiple states need to be declared this is done by writing a ' , ' and then the next state

Example of belief state:
    ((a|b)&c)>>d,e|f
