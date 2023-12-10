# Practicum 

## Usage

```bash
> python3 main.py
```

## Example
Input format is the same as in task description on https://akhcheck.ru/course/31#259
```
2 3 5
SP
cba
S -> Pc
S -> a
S -> abPbS
S -> cSS
P -> P
P
```

## Testing

Get test-coverage of source code (which contains in [coverage.txt](tests/coverage.txt)):

```bash
> pip3 install -r tests/requirements.txt
> pytest --cov=./src/ tests/
```

Run unit-tests:
```bash
> python3 unit_test.py
```

Run Earley-tests:
```bash
> python3 earley_test.py
```
