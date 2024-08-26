# Set up development environment
## 1. Installations
### 1.1 Install a package manager
For macOS, run the command below:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
For Windows users, please follow the instruction on this link: https://chocolatey.org/install
### 1.2 Install Python 3.11.0
```bash
# macOS
brew install python@3.11

# Windows OS
choco install python --version=3.11
```

## 2. Create virtual environment
### 2.1 Find Python3.11
First run this command below to find the path to your Python3.11.0
```bash
# macOS
brew info python@3.11 

# Windows OS
where python
```
For macOS, it will return a path similar to this: `Then run this command below to find the path to your Python3.11.0
```bash
# macOS
brew info python@3.11 

# Windows OS
where python
```
For macOS, it will return a path similar to this: `/usr/local/Cellar/python@3.11/3.11.x/bin/python3`.

For Windows OS, it will return a list of all Python installation, copy the path that includes `Python311`. And the path might look similar to this: `C:\Python311\python.exe`.
### 2.2 Create the virtual environment
First, go to your local repository. Assuming you are already in the root folder, run the following command:
```bash
git pull origin master
cd src/function-app/
```
```bash
# macOS
/usr/local/Cellar/python@3.11/3.11.x/bin/python3 -m venv .venv

# Windows OS
C:\Python311\python.exe -m venv .venv
```
### 2.3 Activate the environment and install the neccessary libraries
```bash
# macOS
source .venv/bin/activate

# Windows OS
.venv\Srcipts\activate
```
```bash
pip install -r requirements.txt
```

## 3. Install Azure Core Tools
```bash
# macOS
brew tap azure/functions
brew install azure-functions-core-tools

# Windows OS
choco install azure-functions-core-tools
```

## 4. Install VSCode Extension
1. Open Visual Studio Code
2. Go the the Extensions tab (Ctrl or Cmd + Shift + X)
3. Search for `Azure Functions`
4. Choose the extension provided by Microsoft