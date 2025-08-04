# autopipinstall

**autopipinstall** is a Python command-line tool that automatically detects and installs missing Python packages when running scripts.  
It’s ideal for rapid prototyping, learning, and sharing scripts without manual pip install steps!

---

## 🚀 Features

- 🚚 **Runs any Python script** and auto-installs missing modules as soon as `ModuleNotFoundError` is encountered.
- 🔍 **Handles submodules:** If `import foo.bar` fails, tries to install both `foo.bar` and the top-level `foo`.
- 📦 **Includes a mapping** for popular package import names that don’t match PyPI names (e.g., `bs4` → `beautifulsoup4`).
- 🖥️ **CLI-friendly:** Just swap in place of your usual `python script.py` call.
- 🧰 **Shows how to alias** for even more convenience.

---

## 📦 Installation

### Install from source (development mode):

```bash
git clone https://github.com/yourusername/autopipinstall.git
cd autopipinstall
pip install -e .
