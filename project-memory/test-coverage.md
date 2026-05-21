# Test Coverage

Created: $(date)

============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /app
plugins: cov-7.1.0
collected 10 items

tests/test_cli.py ....                                                   [ 40%]
tests/test_desktop.py ..                                                 [ 60%]
tests/test_parser.py ....                                                [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.13-final-0 _______________

Name                     Stmts   Miss  Cover
--------------------------------------------
cli/main.py                 40     40     0%
desktop/browser.py          77     77     0%
desktop/integration.py      83     46    45%
desktop/launcher.py         28      8    71%
parser/apk_parser.py        40      6    85%
--------------------------------------------
TOTAL                      268    177    34%
============================== 10 passed in 2.13s ==============================
