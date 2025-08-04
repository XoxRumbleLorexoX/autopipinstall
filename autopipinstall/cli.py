#!/usr/bin/env python3

# autopipinstall.py

import sys
import importlib
print("importlib file path:", getattr(importlib, '__file__', 'frozen or builtin'))
import subprocess
import re
import os

def print_alias_instruction():
    print("\n[autopipinstall] To automatically use this tool for all python3 scripts,")
    print("Add this line to your ~/.bashrc or ~/.zshrc:")
    print(f'  alias python3="python3 {os.path.abspath(__file__)}"\n')

def run_script(script_path, args):
    proc = subprocess.Popen([sys.executable, script_path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    return out, err, proc.returncode

MAPPING = {
    "Crypto": "pycryptodome",
    "PIL": "pillow",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "bs4": "beautifulsoup4",
    "yaml": "pyyaml",
    "lxml": "lxml",
    "matplotlib": "matplotlib",
    "mpl_toolkits": "matplotlib",
    "OpenGL": "pyopengl",
    "serial": "pyserial",
    "pd": "pandas",
    "sns": "seaborn",
    "tf": "tensorflow",
    "plt": "matplotlib",
    "np": "numpy",
    # ...add more as needed
}

def get_pip_name(import_name):
    base_name = import_name.split('.')[0]
    # Prefer full mapping, then base name mapping, then base name itself
    return MAPPING.get(import_name) or MAPPING.get(base_name) or base_name

def main():
    if "--show-alias" in sys.argv:
        print_alias_instruction()
        sys.exit(0)
    if len(sys.argv) < 2:
        print("Usage: python autopipinstall.py yourscript.py [args...]")
        print("Or:    python autopipinstall.py --show-alias")
        sys.exit(1)
    script_path = sys.argv[1]
    extra_args = sys.argv[2:]
    tried = set()
    while True:
        out, err, code = run_script(script_path, extra_args)
        sys.stdout.write(out)
        sys.stderr.write(err)
        match = re.search(r"ModuleNotFoundError: No module named '([^']+)'", err)
        if match:
            modname = match.group(1)
            if modname in tried:
                print(f"[autopipinstall] Already tried installing '{modname}', giving up.")
                sys.exit(1)
            pip_name = get_pip_name(modname)
            print(f"[autopipinstall] Installing missing module: {pip_name} (from import '{modname}')")
            pip_result = subprocess.run([sys.executable, "-m", "pip", "install", pip_name])
            if pip_result.returncode != 0:
                # If submodule, try base/top-level name
                if '.' in modname:
                    top_level = modname.split('.')[0]
                    if top_level not in tried:
                        print(f"[autopipinstall] Failed to install '{pip_name}'. Trying top-level module: '{top_level}'")
                        pip_result2 = subprocess.run([sys.executable, "-m", "pip", "install", top_level])
                        if pip_result2.returncode == 0:
                            print(f"[autopipinstall] Successfully installed '{top_level}'. Retrying...")
                            tried.add(top_level)
                            continue
                        else:
                            print(f"[autopipinstall] Still failed to install '{top_level}'.")
                # Print helpful message and exit
                print(f"[autopipinstall] Failed to install '{pip_name}'.")
                print(f"[autopipinstall] Please Google: 'pip install for {modname} python', or check on https://pypi.org/project/{modname}/")
                print("If you solve it, please contribute the correct mapping to this tool!")
                sys.exit(1)
            tried.add(modname)
            print("[autopipinstall] Retrying...")
        else:
            break

if __name__ == "__main__":
    main()
