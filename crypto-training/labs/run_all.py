#!/usr/bin/env python3
"""Run sessions discovered under sessions/basic, sessions/intermediate, sessions/advanced
"""
import subprocess, time, os

ROOT = os.path.dirname(os.path.dirname(__file__))
ENGINE_SCRIPT = os.path.join(ROOT, 'engine', 'engine_server.py')
LEVELS = ['basic', 'intermediate', 'advanced']

if __name__ == '__main__':
    print('Starting engine...')
    proc = subprocess.Popen([os.sys.executable, ENGINE_SCRIPT])
    try:
        time.sleep(0.3)
        for level in LEVELS:
            level_dir = os.path.join(ROOT, 'sessions', level)
            if not os.path.isdir(level_dir):
                continue
            print('\n=== Running level:', level, '===')
            for root, dirs, files in os.walk(level_dir):
                files = sorted(files)
                for f in files:
                    if not f.endswith('.py'):
                        continue
                    if f in ('__init__.py',):
                        continue
                    path = os.path.join(root, f)
                    rel = os.path.relpath(path, ROOT)
                    print('\n--- RUNNING', rel, '---')
                    try:
                        subprocess.run([os.sys.executable, path], check=False)
                    except Exception as e:
                        print('Failed to run', rel, e)
                    time.sleep(0.1)
    finally:
        proc.terminate()
        proc.wait()
        print('Engine stopped')
