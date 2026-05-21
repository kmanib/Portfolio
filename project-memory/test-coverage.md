# Test Coverage

Created: $(date)

============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /app
plugins: cov-7.1.0
collected 16 items

tests/test_api.py ...                                                    [ 18%]
tests/test_cli.py ....                                                   [ 43%]
tests/test_desktop.py ..                                                 [ 56%]
tests/test_parser.py ....                                                [ 81%]
tests/test_runtime.py ...                                                [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.13-final-0 _______________

Name                                   Stmts   Miss  Cover
----------------------------------------------------------
runtime/api_stubs/__init__.py              0      0   100%
runtime/api_stubs/context.py              10      5    50%
runtime/api_stubs/file.py                 14      8    43%
runtime/api_stubs/intent.py               17      3    82%
runtime/api_stubs/log.py                  20      6    70%
runtime/api_stubs/network.py              17      7    59%
runtime/api_stubs/router.py               37      4    89%
runtime/dalvik/class_loader.py            17      3    82%
runtime/dalvik/dex_parser.py              34     21    38%
runtime/dalvik/opcode_interpreter.py      23      4    83%
----------------------------------------------------------
TOTAL                                    189     61    68%
============================== 16 passed in 2.37s ==============================
