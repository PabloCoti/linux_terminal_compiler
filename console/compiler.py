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
            return "INSTRUCCIONES SOBRE EL USO DE LA APLICACION\n\nNOTA: esta aplicación simula una consola, por lo que ten en cuenta lo siguiente\n\n1. el comando cd emulara un cambio, el proceso no puede ser movido, sin embargo \nse trabajara sobre un path guardado en ram para futuras consultas\n\n2. algunos comandos no funcionan en linux y si en windows, ej. time\n\n------------------------------------------------------------\nCOMANDOS\n    pwd                 muestra el directorio actual, ten en cuenta que la ruta\n                        absoluta no cambiara, pues el proceso no puede cambiar de ruta\n                        pero las consultas que hagas con el programa si se veran reflejados\n                        el puntero será cambiado\n    date                muestra la fecha actual\n    time                muestra la hora actual en la computadora\n    exit                sale del programa\n    clear               limpia la pantalla (consola)\n    Man                 muestra un mensaje con instrucciones e información del programa\n    uname -a            muestra la versión del SO\n    cd <dir>            cambia el path sobre el que estamos trabajando\n    ls [opt] <dir>      muestra los elementos que hay en el directorio\n                        estamos haciendolo basados en linux, por lo que el comando ls no\n                        podra ser ejecutado en windows, es probable que muestre un error\n                        windows utiliza el comando dir\n    rm [files]          borra archivos\n                        files puede ser escrito como un archivo o como un path\n    mkdir <dir>         crea un folder con el nombre de <dir>\n    rmdir <dir>         elimina el folder con el nombre de <dir>, es probable que\n                        no permita borrar carpetas con elementos dentro"
        
        return run_cmd_command(output_command)


    return 'Error: Command not found.'


def run_powershell_command(command):
    # result = subprocess.run(["powershell", "-Command", command], capture_output=True).stdout
    result = subprocess.run(["powershell", "-Command", command], stdout=subprocess.PIPE, text=True)
    return result.stdout

def run_cmd_command(command):
    return system(command)
