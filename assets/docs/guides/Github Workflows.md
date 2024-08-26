# Github Workflow Guide
## 1/ Preparation
### 1.1 Cloning the Repository to Local
1. Open your **terminal** (macOS) or **command prompt** (Windows OS).
2. Navigate to the directory where you want to clone your project using the `cd` command.
	**Example**: 
	``` bash 
	cd Documents/Github/
	```
3. Run the following command:
	``` bash
	git clone https://github.com/AlanDataPortfolio/ey-azure-fn-pipeline.git
	```
4. Change into the cloned directory:
	```bash
	cd ey-azure-fn-pipeline
	```
### 1.2 Adding a remote repository
1. Add the remote origin using:
	```bash
	git remote add origin https://github.com/AlanDataPortfolio/ey-azure-fn-pipeline.git
	```
## 2. Workflows
### 2.1 Find an issue
Go to the **Issues** tab on Github and browse an issue that has been assigned to you. Note that each issue will have a unique number associated with it (e.g., 4). This number will be used for naming your development branch and commit messages.
### 2.2 Create a branch
1. It is a good practice to always pull from the **master** branch before creating a new branch to avoid merge conflicts later on.
	```bash
	git pull origin master
	```
2. Create a new branch with the format `ticket-<issue-number>`. For example, if your issue number is 4, you would run:
	```bash
	git checkout -b ticket-4
	```
### 2.3 Making changes
1. Make the neccessary changes to the files in your local repository.
2. Add the changes to the staging area.
	```bash
	git add .
	```
3. Commit the changes with a descriptive message with the format `#<issue-number: <desc>`
	```bash
	git commit -m "#<4: Added Github Workflows Guide"
	```
4. Push the changes to the remote branch.
	```bash
	git push origin ticket-4
	```
5. Once the changes are pushed, you can create a Pull Request (PR) on GitHub to merge your branch into the `master` branch.
