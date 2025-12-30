
# Kali Installation Steps

**PART 1 - Extract the Project (Kali)**
Download the zip file and place it on the Desktop.

1. Open terminal
```bash
cd ~/Dekstop
```

2. Extract the zip file
unzip securems_share.zip

3. Enter the project folder
cd securems_share

4. Confirm structure
ls -l

Check that these folders/files exist:
accounts/
auditlog/
booking/
core/
manage.py
requirements.txt
templates/
securems/

If they match, proceed. If not, stop and inform. 

**PART 2 - Install Python & Virtual Environment (Kali)**

1. Check Python version :
python3 --version

Must be 3.10 or higher

If missing, install : 
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

2. Create virtual environment
python3 -m venv env

3. Activate virtual environment
source env/bin/activate

You should see:
(env) kali@kali:~/Desktop/securems_share$


**PART 3 - Install Project Dependencies**
1. Upgrade pip
pip install --upgrade pip

2. Install requirements
pip install -r requirements.txt


**PART 4 — Environment Configuration (IMPORTANT)**
1. Create .env file
nano .env

2. Paste this (safe dev config):
DEBUG=True
SECRET_KEY=dev-secret-key-only
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.242.129

Change localhost with your IP address

Save with:
CTRL + O → ENTER → CTRL + X

**PART 5 — Database Setup (SQLite – Safe & Simple)**
python manage.py makemigrations
python manage.py migrate

**PART 6 — Create Admin Account**
python manage.py createsuperuser

Enter any username, email, and password.

**PART 7 — Run the Server**
python manage.py runserver

Open browser and visit:
http://127.0.0.1:8000
