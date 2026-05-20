# Test Coverage

Created: $(date)

============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /app
plugins: cov-7.1.0
collected 8 items

tests/test_cli.py ....                                                   [ 50%]
tests/test_parser.py ....                                                [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.13-final-0 _______________

Name                   Stmts   Miss  Cover
------------------------------------------
cli/main.py               40     40     0%
parser/apk_parser.py      40      6    85%
------------------------------------------
TOTAL                     80     46    42%
============================== 8 passed in 1.86s ===============================
