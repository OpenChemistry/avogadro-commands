"""
/******************************************************************************
  This source file is part of the Avogadro project.

  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import argparse
import json
import sys

# Some globals:
debug = True


def getOptions():
    userOptions = {}

    userOptions['X Scale'] = {}
    userOptions['X Scale']['label'] = 'X Scale'
    userOptions['X Scale']['type'] = 'float'
    userOptions['X Scale']['default'] = 1.0
    userOptions['X Scale']['precision'] = 3
    userOptions['X Scale']['toolTip'] = 'Multiplier for X coordinates'

    userOptions['Y Scale'] = {}
    userOptions['Y Scale']['label'] = 'Y Scale'
    userOptions['Y Scale']['type'] = 'float'
    userOptions['Y Scale']['default'] = 1.0
    userOptions['Y Scale']['precision'] = 3
    userOptions['Y Scale']['toolTip'] = 'Multiplier for Y coordinates'

    userOptions['Z Scale'] = {}
    userOptions['Z Scale']['label'] = 'Z Scale'
    userOptions['Z Scale']['type'] = 'float'
    userOptions['Z Scale']['default'] = 1.0
    userOptions['Z Scale']['precision'] = 3
    userOptions['Z Scale']['toolTip'] = 'Multiplier for Z coordinates'

    opts = {'userOptions': userOptions}

    return opts


def scale(opts, mol):
    xScale = float(opts['X Scale'])
    yScale = float(opts['Y Scale'])
    zScale = float(opts['Z Scale'])
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
    coords = mol['atoms']['coords']['3d']
    for i in range(0, len(coords), 3):
        if j in indices:
            coords[i] = coords[i] * xScale
            coords[i + 1] = coords[i + 1] * yScale
            coords[i + 2] = coords[i + 2] * zScale
        j = j+1

    return mol


def runCommand():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
    result = {}
    result['cjson'] = scale(opts, opts['cjson'])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Scale molecular coordinates.')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Scale Coords...")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
