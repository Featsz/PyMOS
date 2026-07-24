import os
import time
import random
from datetime import datetime
from colorama import Fore, Style, init
import whatismyip, requests
import platform
import json
import sys

init(autoreset=True)

try:
    import readline
    readline.parse_and_bind('set history-length 1000')
except:
    pass

user_name = os.getlogin()
host_name = "PyMOS"
home_folder = os.path.dirname(os.path.abspath(__file__))
PHYSICAL_HOME = os.path.join(home_folder, "home", "user")
if not os.path.exists(PHYSICAL_HOME):
    os.makedirs(PHYSICAL_HOME)

CONFIG_DIR = os.path.join(PHYSICAL_HOME, ".pymos")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

if not os.path.exists(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)
    if platform.system() == "Windows":
        os.system(f'attrib +h "{os.path.normpath(CONFIG_DIR)}"')

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        f.write('{"user_name": "user", "host_name": "PyMOS", "auto_command": "", "prompt": ""}')

config = {}
custom_prompt = ""

def load_config():
    global user_name, host_name, config, auto_command, VIRTUAL_HOME, custom_prompt, PHYSICAL_HOME
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            user_name = config.get("user_name", "user")
            host_name = config.get("host_name", "PyMOS")
            auto_command = config.get("auto_command", "")
            custom_prompt = config.get("prompt", "")
            
    except:
        pass

#user_name = "user"
#host_name = "PyMOS"
#auto_command = ""

load_config()

def cmd_resetconfig(args):
    global config, user_name, host_name, custom_prompt
    try:
        default_config = {
            "user_name": "user", 
            "host_name": "PyMOS", 
            "auto_command": "",
            "prompt": ""
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=4)
        config = default_config
        user_name = default_config["user_name"]
        host_name = default_config["host_name"]
        custom_prompt = default_config["prompt"]
        print(f"{Fore.GREEN}Config has been reset to default.")
        
        #load_config()
        

    except Exception as e:
        print(f"resetconfig: {Fore.RED}Error: {e}")

def clear(args=None):
    os.system('cls' if os.name == 'nt' else 'clear')

now = datetime.now()
now_time = now.strftime("%H:%M:%S")
now_time_Ymd = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

cur_dir = f"~"
input_nick = f"~"

def start():
    global input_nick, uptime, PHYSICAL_HOME
    uptime = time.time()
    print(Fore.LIGHTGREEN_EX + "Python Mini-OS v1.0 Alpha Booting..." + Fore.WHITE)
    os.chdir(PHYSICAL_HOME)
    input_nick = get_prompt()
    
    print(Fore.GREEN + f"""
    =====================
    |  Python Mini-OS  |
    |Version: 1.0 Alpha|
    |  Made by Feat.   |
    |     {now_time}     |
    =====================""" + Fore.WHITE)
    print(f"""
    {Fore.GREEN}Welcome to PyMOS{Fore.WHITE}

 - Github : {Fore.LIGHTBLUE_EX}https://github.com/Featsz/PyMOS{Fore.RESET}
 - Community : {Fore.LIGHTBLUE_EX}https://t.me/feat_sz{Fore.RESET}
 - Report : {Fore.LIGHTBLUE_EX}https://t.me/feat_chat{Fore.RESET}
 - Your name : {Fore.LIGHTBLUE_EX}{user_name}
 """)
    
    print(f"{Fore.LIGHTGREEN_EX}Start Time{Fore.LIGHTBLUE_EX} >>> {Style.RESET_ALL + now_time_Ymd}")

    if config.get("auto_command"):
        raw = config["auto_command"].strip()
        parts = raw.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd in commands:
            commands[cmd](args)
        else:
            print(f"auto_command: {Fore.RED}Command '{cmd}' not found")
    
def get_prompt():
    current_path = os.getcwd()
    virtual_home = f"/home/{user_name}"

    if current_path == PHYSICAL_HOME:
        return virtual_home
    elif current_path.startswith(PHYSICAL_HOME):
        return virtual_home + current_path.replace(PHYSICAL_HOME, "")
    elif current_path.startswith(home_folder):
        releative = current_path.replace(home_folder, "")
        if releative.startswith("/"):
            return releative
        else:
            return "/" + releative
    else:
        return current_path

def cmd_ls(args):
    
    for item in os.listdir('.'):
        if item.startswith('.'):
            continue
        if os.path.isdir(item):
            print(f"{Fore.LIGHTBLUE_EX + item + Fore.RESET}")
        else:
            print(item)

def cmd_cd(args):
    args_com = ' '.join(args)
    try:
        global cur_dir, input_nick
        if not args:
            os.chdir(PHYSICAL_HOME)
            cur_dir = "~"
            return
        target_path = os.path.abspath(args[0] if args else os.path.expanduser('~'))
        if args[0] == ".." and cur_dir == "~":
            return
        if not target_path.startswith(home_folder):
            print(f"cd: {Fore.RED}No such directory")
            return
        os.chdir(args[0] if args else os.path.expanduser('~'))
        cur_dir = args_com
    except FileNotFoundError:
         print(f"cd: {Fore.RED + Style.BRIGHT}No such directory")
    except NotADirectoryError:
         print(f"cd: {Style.BRIGHT}'{args[0]}'{Fore.RED} is not a directory")

def cmd_exit(args):
    print(f"exit: {Fore.RED + Style.BRIGHT}System shutdown")
    time.sleep(1)
    print("\n" * 100)
    clear()
    print(f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}Bye-Bye!")
    exit()

def cmd_mkdir(args):
    if not args:
        print("mkdir: missing operand")
        return
    clean_args = [arg for arg in args if arg != '-v']
    folder_name = ' '.join(clean_args)
    verbose = "-v" in args
    try:
        os.mkdir(folder_name)
        if verbose:
            print(f"mkdir: created directory '{folder_name}'")
                
    except FileExistsError:
            
        print(f"mkdir: cannot create directory '{folder_name}': File exists")
    except FileNotFoundError:
        print(f"mkdir: cannot create directory '{folder_name}': No such file or directory")
    
def cmd_sudo(args):
    cmd_name = ' '.join(args)
    if "rm -rf /*" in cmd_name or "rm -rf /" in cmd_name:
        print(f"{Fore.RED + Style.BRIGHT}The system is being completely removed, please wait a moment.")
        for i in range(101):
            bar = "█" * (i // 2) + "░" * (50 - i // 2)
            print(f"\r[{bar}] {i}%", end="")
            time.sleep(0.1)
            
        print("\r" + " " * 100 + "\r", end="")
                    
        print("\n" * 100)
        clear()
        print(f"{Fore.RED + Style.BRIGHT}Bye-Bye!")
        exit()
        return
        
    print(f"sudo: {Fore.RED + Style.BRIGHT}Permission denied{Style.RESET_ALL}")

  
def cmd_fm(args):
    if not args or args[0] == "--help" or args[0] == "-":
        print("""
    fm - Universal file manager
        
    USAGE:
        fm [option] <filename> [content]
        
    OPTIONS:
        -c <filename> Create an empty file
        -d <filename> Delete the file (rm)
        -r <filename> Read (print) file content (cat)
        -a <filename> <text> Append text to the file
        --help Show this help message
        """)
        return

    option = args[0]
    filename = args[1] if len(args) > 1 else None
    
    if option == "-c" or option == "-mk":
        if not filename:
            print("fm: missing filename for -c")
            return
        try:
            with open(filename, 'x'): 
                pass
            print(f"fm: created file '{filename}'")
        except FileExistsError:
            print(f"fm: cannot create '{filename}': File exists")
    
    elif option == "-d" or option == "-rm":
        cur_path = os.path.abspath(__file__)
        if not filename:
            print("fm: missing filename for -d")
            return
        elif filename == cur_path:
            print("no")
            return
        try:
            os.remove(filename)
            print(f"fm: deleted file '{filename}'")
        except FileNotFoundError:
            print(f"fm: cannot delete '{filename}': No such file or directory")
        except IsADirectoryError:
            print(f"fm: cannot delete '{filename}': Is a directory")
    
    elif option == "-r":
        if not filename:
            print("fm: missing filename for -r")
            return
        try:
            with open(filename, 'r', encoding="UTF-8") as f:
                print(f"{Fore.GREEN + Style.BRIGHT + filename}:")
                print(Fore.WHITE + f.read())
        except FileNotFoundError:
            print(f"fm: cannot read '{filename}': No such file or directory")
        except IsADirectoryError:
            print(f"fm: '{filename}' is a directory")
        except UnicodeDecodeError:
            print(f"fm: cannot read '{filename}': Binary or unsupported file format")
    
    elif option == "-a":
        if not filename:
            print("fm: missing filename for -a")
            return
        if len(args) < 3:
            print("fm: missing text to append")
            return
        content = ' '.join(args[2:])
        try:
            with open(filename, 'a') as f:
                f.write(content + "\n")
            print(f"fm: appended text to '{filename}'")
        except FileNotFoundError:
            print(f"fm: cannot append to '{filename}': No such file or directory")
        except IsADirectoryError:
            print(f"fm: '{filename}' is a directory")
    
    else:
        print(f"fm: unknown option '{option}'. Use fm --help")
        
                    
def cmd_help(args):
    commands_help = {
    'ls': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}list files in current directory',
    'cd': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}change directory',
    'exit': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}exit the program',
    'sudo': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}execute with superuser privileges (if root access is available)',
    'help': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}show this help message',
    'sysfetch': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}show information',
    'rmdir': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}remove directory',
    'pwd': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}show current directory',
    'reboot': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}restarting system',
    'shutdown': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}shutdown',
    'date': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}show time (with args)',
    'whoami': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}show current user',
    'mkdir': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}create a new directory',
    'echo': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}print text on the screen',
    'matrix': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}display the Matrix falling code effect',
    'fm': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}universal File Manager (for help: fm --help)',
    'ip': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}show public/local IP or (and) address (city, country, provider: -a or -all)',
    'clear': f'{Fore.LIGHTBLUE_EX + Style.BRIGHT}Clear all',
    'setconfig': f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}Allows you to set your own configuration",
    }
    print("\nAvailable commands:")
    print()
    for cmd, desc in commands_help.items():
        print(f" {cmd:<10} - {desc}")

def cmd_systemfetch(args):
    uptime_seconds = time.time() - uptime
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    nice_uptime = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
    

    user = os.getlogin()
    host = os.uname().nodename

    if os.getcwd() == PHYSICAL_HOME:
        display_path = f"/home/{user_name}"
    elif os.getcwd().startswith(PHYSICAL_HOME):
        display_path = f"/home/{user_name}" + os.getcwd().replace(PHYSICAL_HOME, "")
    else:
        display_path = os.getcwd()

    system_platform = platform.system()
    split = os.uname().release.split('-')[1]
    
    print(f""" {Fore.GREEN + Style.BRIGHT}PYTHON MINI-OS SYSTEM INFO{Fore.RESET} \n\n{Fore.RESET}
     —{Fore.LIGHTGREEN_EX} User{Fore.WHITE} : {Fore.LIGHTBLUE_EX}{user_name}
     {Fore.WHITE}—{Fore.LIGHTGREEN_EX} Hostname{Fore.WHITE} : {Fore.LIGHTBLUE_EX}{host_name}
     {Fore.WHITE}—{Fore.LIGHTGREEN_EX} Uptime{Fore.WHITE} : {Fore.LIGHTBLUE_EX}{nice_uptime}
     {Fore.WHITE}—{Fore.LIGHTGREEN_EX} Directory{Fore.WHITE} : {Fore.LIGHTBLUE_EX}{display_path}
     {Fore.WHITE}—{Fore.LIGHTGREEN_EX} OS{Fore.WHITE} : {Fore.LIGHTBLUE_EX}PyMOS v1.0 Alpha ({system_platform})
     {Fore.WHITE}—{Fore.LIGHTGREEN_EX} help {Fore.WHITE} : {Fore.LIGHTBLUE_EX}help{Fore.RESET + Style.RESET_ALL}""")

def cmd_pwd(args):
    print(os.getcwd())

def cmd_rmdir(args):
    if not args:
        print(f"rmdir: {Fore.RED}missing operand{Fore.WHITE}")
        return   
    folder_name = str(' '.join(args).strip())
    try:
        os.rmdir(folder_name)
        print(f"rmdir: directory '{folder_name}' removed")
    except FileNotFoundError:
        print(f"rmdir: {Fore.RED} cannot delete{Fore.WHITE} '{folder_name}':{Fore.RED} No such file or directory{Fore.WHITE}")
    except OSError:
        print(f"rmdir: {Fore.RED}cannot delete{Fore.WHITE} '{folder_name}': {Fore.RED}Directory not empty{Fore.WHITE}")

def cmd_reboot(args):
    print(f"reboot: {Fore.RED + Style.BRIGHT}Restarting system{Fore.RESET}")
    time.sleep(1)
    clear()
    start()

def cmd_date(args):
    if not args:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return
    format_string = ' '.join(args)
    
    try:
        clean_format = format_string.replace('+', '').replace("-", "").replace('"', "").replace("'", "")
        print(datetime.now().strftime(clean_format))
    except ValueError:
        print(f"date: {Fore.RED}invalid format" + Fore.WHITE)

def cmd_whoami(args):
    print(" " * 3 + Fore.LIGHTBLUE_EX + Style.BRIGHT + user_name)

def cmd_echo(args):
    print(' '.join(args)) 

def cmd_matrix(args):
    clear()
    symbols = ['0', '1']
    try:
        start_time = time.time()
        print("\033[?25l", end="")
        while True:
            line = ''.join(random.choice(symbols) for _ in range(65))
            print(Fore.GREEN + line)
            if time.time() - start_time > 10:
                print()
                clear()
                print("\033[?25h", end="")
                break
            time.sleep(0.033)
    except KeyboardInterrupt:
        pass

def cmd_ip(args):
        try:
            localip = whatismyip.whatismylocalip()
            if not args or "-all" in args:
                print(f"Global-Ip: {whatismyip.whatismyip()}")
                print(f"Local-Ip: {whatismyip.whatismylocalip()[0]}")
            if "-a" in args or "-all" in args:
                data = requests.get('http://ip-api.com/json').json()
                print(f"City: {data['city']}, country: {data['country']}, Provider: {data['isp']}")
            if "-help" in args or "--help" in args:
                print(f"""
Usage: ip [option]

Ip help:
        -all : Show public, local ip, country, city, provider
        -a : Show country, city and provider
        -help : Show this information
        (default): Show global and local Ip""")
        except Exception as error:
            print(f"ip: {Fore.RED}{error}{Fore.RESET}")
            
def cmd_set(args):
    if len(args) < 2:
        print("Usage: set <key> <value>")
        return
    key = args[0]
    value = ' '.join(args[1:])
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            new_config = json.load(f)
        
        if key in new_config:
            new_config[key] = repr(value)[1:-1]
            with open(CONFIG_FILE, 'w') as f:
                json.dump(new_config, f, indent=4)
            print(f"set: '{key}' changed to '{value}'")
            load_config()
        else:
            print(f"set: '{key}' is not a valid config key")
    except Exception as e:
        print(f"set: Error: {e}")
        
def cmd_yes(args):
    try:
        print("\033[?25l", end="")
        while True:
            time.sleep(0.02)
            print("Y")
    except KeyboardInterrupt:
        print("\n^C")
        print("\033[?25h", end="")
        return
        
def cmd_cat(args):
    cmd_fm(["-r"] + args)

def cmd_rm(args):
    cmd_fm(["-d"] + args)
        
commands = {
    'ls': cmd_ls,
    'sl': cmd_ls,
    'файлы': cmd_ls,
    'cd': cmd_cd,
    'chdir': cmd_cd,
    'перейти': cmd_cd,
    'exit': cmd_exit,
    'q': cmd_exit,
    'й': cmd_exit,
    'bye': cmd_exit,
    'quit': cmd_exit,
    'shutdown': cmd_exit,
    'poweroff': cmd_exit,
    'halt': cmd_exit,
    'выход': cmd_exit,
    'sudo': cmd_sudo,
    'help': cmd_help,
    'помощь': cmd_help,
    'mkdir': cmd_mkdir,
    'md': cmd_mkdir,
    'сп': cmd_mkdir,
    'systemfetch': cmd_systemfetch,
    'fetch': cmd_systemfetch,
    'sysfetch': cmd_systemfetch,
    'sys': cmd_systemfetch,
    'system': cmd_systemfetch,
    'pwd': cmd_pwd,
    'rmdir': cmd_rmdir,
    'rd': cmd_rmdir,
    'reboot': cmd_reboot,
    'restart': cmd_reboot,
    'date': cmd_date,
    'time': cmd_date,
    'whoami': cmd_whoami,
    'wai': cmd_whoami,
    'echo': cmd_echo,
    'matrix': cmd_matrix,
    'fm': cmd_fm,
    'cat': cmd_cat,
    'rm': cmd_rm,
    'clear': clear,
    'ip': cmd_ip,
    'setconfig': cmd_set,
    'yes': cmd_yes,
    'resetconfig': cmd_resetconfig,
}

hist_cmd = 0

clear()
start()

while True:
    custom_prompt = config.get("prompt", "")
    path_display = get_prompt()
    user_display = user_name
    host_display = host_name
    date = datetime.now().strftime("%H:%M")
    system = platform.system()

    parts = []
    
    if path_display == f"/home/{user_name}":
        path_display = "~"

    if custom_prompt:
        raw_prompt = custom_prompt
        raw_prompt = raw_prompt.replace("\\n", "\n")

        try:
            formatted_prompt = raw_prompt.format(
                ## base
                user_name=user_name,
                host_name=host_name,
                path=path_display,
                date=date,
                hcmd=hist_cmd,
                system=system,

                ## system commands
                n="\n",
                spc=" ",

                ## colors
                green=Fore.GREEN,
                red=Fore.RED,
                blue=Fore.BLUE,
                yellow=Fore.YELLOW,
                grey=Fore.LIGHTBLACK_EX,
                gray=Fore.LIGHTBLACK_EX,
                bold=Style.BRIGHT,
                black=Fore.BLACK,
                white=Fore.WHITE,
                RESET_COLOR=Fore.RESET,
                RESET=Style.RESET_ALL,
            )
            prompt_lines = formatted_prompt.split('\n')
            for line in prompt_lines[:-1]:
                print(line)
            parts = input(prompt_lines[-1]).split()
        except (ValueError, KeyError) as e:
            print()
            print(e)
            while True:
                answer = input("Invalid prompt detected. Reset to default? [Y/n] ").strip().lower()
                if answer in ["y", "yes", ""]:
                    cmd_resetconfig(None)
                    break
                elif answer in ["n", "no"]:
                    print("\nSkipping reset\n")
                    print(f"{Style.BRIGHT}Invalid prompt detected.\nDelete {Fore.BLUE}/home/user/pymos/config.json{Fore.RESET} and restart to reset to default.")
                    exit()
                else:
                    pass
    else:
        upper_line = f"\n{Style.BRIGHT + Fore.WHITE}┌──({Fore.LIGHTGREEN_EX}{user_display}{Fore.WHITE}@{Fore.LIGHTBLUE_EX}{host_display}{Fore.WHITE})-[{Fore.LIGHTBLUE_EX}{path_display}{Fore.WHITE}]"
        lower_line = f"{Style.RESET_ALL + Style.BRIGHT}└─{Fore.LIGHTBLUE_EX + Style.BRIGHT}$ {Fore.LIGHTBLACK_EX}"
        
        print(upper_line)

        try:
            parts = input(lower_line).split()
        except KeyboardInterrupt:
            print()
            continue
    
    print(Style.RESET_ALL, end="")
    if not parts:
        continue
    cmd = parts[0]
    args = parts[1:]
    if cmd in commands:
        commands[cmd](args)
        hist_cmd += 1
    else:
        print(f"'{cmd}'{Fore.RED + Style.BRIGHT} not found. use{Style.RESET_ALL} 'help'")

## By FEAT.
