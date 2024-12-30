import sys
import json
import traceback
from io import StringIO
from contextlib import redirect_stderr, redirect_stdout

def execute_code(code: str) -> dict:
    stdout_capture = StringIO()
    stderr_capture = StringIO()

    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, {})

            return {
                "success": True,
                "output": stdout_capture.getvalue(),
                "error": stderr_capture.getvalue()
            }

    except Exception as e:
        return {
            "success": False,
            "output": stdout_capture.getvalue(),
            "error": traceback.format_exc()
        }


def main():
    code = sys.stdin.read()
    result = execute_code(code)
    print(json.dumps(result))

if __name__ == '__main__':
    main()
    