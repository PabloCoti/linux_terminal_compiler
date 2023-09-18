import re
import subprocess
from os import system

static_commands = ['pwd', 'date', 'time', 'exit', 'clear', 'Man', 'uname -a']
dynamic_commands = ['cd', 'ls', 'rm', 'mkdir', 'rmdir']

ls_options = ['-a', '-l']

static_win_equivalent = ['cd', 'date', 'time', 'exit', 'cls', 'man', 'ver']


def compile(command):
    if any(static_commands in command for static_commands in static_commands) or 'uname' in command:
        return compile_static_command(command)

    elif any(dynamic_commands in command for dynamic_commands in dynamic_commands):
        return compile_dynamic_command(command)

    else:
        return 'Error: Command not found.'

def compile_dynamic_command(command):
    if any(dynamic_commands in command for dynamic_commands in dynamic_commands):
        if 'cd' in command:
            return compile_file_command(command, 'cd')

        elif 'ls' in command:
            return compile_ls(command)

        elif 'rmdir' in command:
            return compile_file_command(command, 'rmdir')

        elif 'rm' in command:
            return compile_file_command(command, 'rm')

        elif 'mkdir' in command:
            return compile_file_command(command, 'mkdir')

    else:
        return 'Error: Command not found.'

def compile_file_command(command, dynamic_command):
    if re.fullmatch(r'^\s*{}\s+([a-zA-Z0-9_./-]+\s*)$'.format(dynamic_command), command):
        return run_powershell_command(command)

    else:
        return 'Error: Command not found.'

def compile_ls(command):
    if re.fullmatch(r'^\s*ls(\s+-[al])?\s*$', command):
        return run_powershell_command(command)

    else:
        return 'Error: Command not found.'

def compile_static_command(command):
    general_pattern = r'^\s*(\w+)\s*$'
    uname_pattern = r'^\s*uname\s*-a\s*$'
    if re.fullmatch(uname_pattern, command):
        return run_cmd_command('ver')

    elif re.fullmatch(general_pattern, command):
        expression = re.fullmatch(general_pattern, command)
        c_split = expression.group(1)
        command_index = static_commands.index(c_split)
        output_command = static_win_equivalent[command_index]
        
        if c_split == 'Man':
            return run_powershell_command(output_command)
        
        return run_cmd_command(output_command)


    return 'Error: Command not found.'


def run_powershell_command(command):
    return subprocess.run(["powershell", "-Command", command], capture_output=True)

def run_cmd_command(command):
    return system(command)
