"""
/******************************************************************************
  This source file is part of the Avogadro project.

  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import argparse
import json
import sys


def getOptions():
    return {}


def flattenZ(opts, mol):
    coords = mol['atoms']['coords']['3d']
    # check if the user has any atoms selected
    any_selected = False
    if 'selected' in mol['atoms']:
        for item in mol['atoms']['selected']:
            if item:
                any_selected = True
                break  # we have *some* atoms selected
    indices = []
    atomic_numbers = mol['atoms']['elements']['number']

    for i in range(len(atomic_numbers)):
        if not any_selected:
            indices.append(i)
            # or only do selected atoms
        elif mol['atoms']['selected'][i]:
            indices.append(i)
    j = 0

    for i in range(0, len(coords), 3):
        if j in indices:
            coords[i+2] = 0.0
        j = j+1

    return mol


def runCommand():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
    result = {}
    result['cjson'] = flattenZ(opts, opts['cjson'])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Flatten Z axis.')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Flatten Z-Axis")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
