import subprocess
import shutil

def launch_app(app_name):
    """
    Launch an application by name.
    It searches for the application in the system's PATH.
    """
    app_path = shutil.which(app_name)
    if app_path:
        try:
            subprocess.call([app_path])
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print(f"Application '{app_name}' not found.")
        return False