import difflib
import argparse
import json
import subprocess
import os


def run_command(command, stdin=None):
    result = subprocess.run(command.split(
        ' '), capture_output=True, text=True, stdin=stdin)
    return result

def diff_files(file1, file2):
    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            diff = difflib.unified_diff(
                f1.readlines(),
                f2.readlines(),
                fromfile=file1,
                tofile=file2,
            )
            print(''.join(diff))

if __name__ == '__main__':
    test_files = os.listdir('tests')
    for input_file in test_files:
        if input_file.endswith('.in'):
            output_file = input_file.replace('.in', '.out')
            print('Testing {}...'.format(input_file))
            diff_files('tests/'+input_file, 'tests/'+output_file)
            input()
