"""Python sandbox for the agent to execute arbitrary analysis code."""

import subprocess
import sys
import tempfile
import os
from pathlib import Path


SANDBOX_PREAMBLE = """\
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats
from datetime import datetime, timedelta

def get_prices(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, progress=False)
    if hasattr(df.columns, 'levels'):
        df.columns = df.columns.get_level_values(0)
    return df

"""

MAX_OUTPUT_CHARS = 15000
TIMEOUT_SECONDS = 60


def execute_python(code: str) -> str:
    full_code = SANDBOX_PREAMBLE + code

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full_code)
        script_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=str(Path(__file__).parent.parent.parent),
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            stderr = result.stderr.strip()
            # Filter out yfinance download noise
            lines = [l for l in stderr.split('\n')
                     if not any(skip in l for skip in ['Failed download', 'possibly delisted', '$'])]
            if lines:
                output += "\n[stderr]\n" + '\n'.join(lines)

        if not output.strip():
            output = "(no output)"

        if len(output) > MAX_OUTPUT_CHARS:
            output = output[:MAX_OUTPUT_CHARS] + f"\n\n[truncated — {len(output)} chars total]"

        return output
    except subprocess.TimeoutExpired:
        return f"[Execution timed out after {TIMEOUT_SECONDS}s]"
    except Exception as e:
        return f"[Sandbox error: {e}]"
    finally:
        os.unlink(script_path)
