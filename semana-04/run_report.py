#!/usr/bin/env python3
"""
Wrapper to run the CSV analysis report using the config in report_config.json.
Writes logs to run_report.log.
"""
import json
import subprocess
import sys
from pathlib import Path
import datetime

CONFIG_PATH = Path(__file__).parent / 'report_config.json'
LOG_PATH = Path(__file__).parent / 'run_report.log'
ANALYZE_SCRIPT = Path(__file__).parent / 'analyze_csv_report.py'


def log(msg: str):
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {msg}\n")


def main():
    if not CONFIG_PATH.exists():
        print('Config not found:', CONFIG_PATH)
        sys.exit(1)

    cfg = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
    csv_path = cfg.get('csv_path')
    output_path = cfg.get('output_path', 'relatorio_diario.md')
    focus = cfg.get('focus', '')

    if not csv_path:
        log('csv_path not set in config')
        sys.exit(1)

    csv_full = (Path(__file__).parent / csv_path).resolve()
    out_full = (Path(__file__).parent / output_path).resolve()

    if not csv_full.exists():
        log(f'CSV not found: {csv_full}')
        sys.exit(1)

    cmd = [sys.executable, str(ANALYZE_SCRIPT), '--csv',
           str(csv_full), '--output', str(out_full)]
    if focus:
        cmd.extend(['--focus', focus])

    log('Running: ' + ' '.join(cmd))
    try:
        proc = subprocess.run(cmd, capture_output=True,
                              text=True, timeout=1800)
        log('Return code: ' + str(proc.returncode))
        if proc.stdout:
            log('STDOUT:\n' + proc.stdout)
        if proc.stderr:
            log('STDERR:\n' + proc.stderr)
    except Exception as exc:
        log('Error running analysis: ' + str(exc))
        sys.exit(1)


if __name__ == '__main__':
    main()
