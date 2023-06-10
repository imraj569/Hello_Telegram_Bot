import psutil , os ,time

def check_script_running(script_name):
    for process in psutil.process_iter(['name', 'cmdline']):
        if process.info['name'] == 'pythonw.exe' and len(process.info['cmdline']) > 1:
            if script_name in process.info['cmdline'][1]:
                return True
    return False

def checker():
    script_name = "main.pyw"  # Replace with the name of your script
    is_running = check_script_running(script_name)
    if is_running:
        print(f"The script '{script_name}' is running in the background.")
        ab = input("do i kill main.pyw [yes/no]:")
        if "yes" in ab:
            killer()
        else:
            print("as your wish")

    else:
        print(f"The script '{script_name}' is not running in backgroud.")
        ab = input("do i run main.pyw [yes/no]:")
        if "yes" in ab:
            os.startfile("D:\\hello\\main.pyw")
            print("main.pyw started...")
        else:
            print("as your wish")

def kill_script(script_name):
    for process in psutil.process_iter(['name', 'cmdline']):
        if process.info['name'] == 'pythonw.exe' and len(process.info['cmdline']) > 1:
            if script_name in process.info['cmdline'][1]:
                process.kill()
                return True
    return False

def killer():
    script_name = "main.py"  # Replace with the name of your script
    is_killed = kill_script(script_name)
    if is_killed:
        print(f"The script '{script_name}' has been killed.")
    else:
        print(f"The script '{script_name}' is not running.")

def controler():
    button = input("press [1-check running/2-kill process/3-run main.pyw]: ")
    os.system("cls")
    if "1" in button:
        checker()

    elif "2" in button:
        killer()
    
    elif "3" in button:
        script_name = "main.pyw"  # Replace with the name of your script
        is_running = check_script_running(script_name)
        if is_running:
            print(f"The script '{script_name}' is already running in the background.")
        else:
            print(f"The script '{script_name}' is not running in background.")
            a = input("do i start main.pyw [yes/no]:")
            if "yes" in a:
                os.startfile("D:\\hello\\main.pyw")
                print("main.pyw started...")
            else:
                print("as your wish")
    else:
        print("command not found!")

if __name__ == "__main__":
    os.system("cls")
    controler()
    time.sleep(3)