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
        return 'Error: Comando inexistente.'


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
        return 'Error: Comando inexistente.'


def compile_file_command(command, dynamic_command):
    if re.fullmatch(r'^\s*{}\s+([a-zA-Z0-9_./-]+\s*)$'.format(dynamic_command), command):
        return run_powershell_command(command)

    else:
        return 'Error: Comando inexistente.'


def compile_ls(command):
    if re.fullmatch(r'^\s*ls(\s+-[al])?\s*$', command):
        return run_powershell_command(command)

    else:
        return 'Error: Comando inexistente.'


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
            return ("INSTRUCCIONES SOBRE EL USO DE LA APLICACION\n\nNOTA: Esta aplicación simula una consola de linux, "
                    "por lo que ten en cuenta lo siguiente\n\n1. el comando cd simulará un cambio de directorio, "
                    "el proceso no se va a mover de directorio, sin embargo \nse trabajara sobre un path guardado en "
                    "ram para futuras consultas\n\n2. Algunos comandos no funcionan en linux y sí en windows o "
                    "funcionan de forma diferente, ej. time\n\n3. Existen algunos comandos que no funcionarán debido "
                    "a problemas con permisos que se presentan en windows (como borrar una carpeta con archivos "
                    "dentro).\n\n------------------------------------------------------------\nCOMANDOS\n    pwd      "
                    "           Muestra el directorio en el que se está trabajando\n    date                muestra "
                    "la fecha actual\n    time                Muestra la hora actual en la computadora\n    exit      "
                    "          Salir del programa\n    clear               Limpiar consola\n    Man                 "
                    "Instrucciones de manejo del programa\n    uname -a            Versión del sistema operativo\n    "
                    "cd <dir>            Cambia el path sobre el que estamos trabajando\n    ls [opt] <dir>      "
                    "muestra los elementos que hay en el directorio\n    rm [file]           Borra archivo "
                    "especificado\n                        file puede ser escrito como un archivo o como un path\n    "
                    "mkdir <dir>         Crea un directorio con el nombre de <dir>\n    rmdir <dir>         Elimina "
                    "el directorio con el nombre de <dir>\nVersión: 1.0\nHecho por: Pablo Cotí - 1653221")

        elif c_split == "exit":
            return exit()

        return run_cmd_command(output_command)

    return 'Error: Comando inexistente.'


def run_powershell_command(command):
    result = subprocess.run(["powershell", "-Command", command], stdout=subprocess.PIPE, text=True)
    return result.stdout


def run_cmd_command(command):
    return system(command)
