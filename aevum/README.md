# Aevum – Premium Capstone-Level Student Management System

Aevum is a Django-based student productivity and management platform designed for capstone submission, phone-based development, browser-based editing, and public sharing.

## What Aevum includes

- Premium landing page and dashboard UI
- Student registration, login, logout, admin panel
- Profile management with GitHub configuration
- Smart notes with Markdown, file attachments, tags, pinning, and public sharing
- Kanban task board with To Do / Doing / Done workflow
- Event calendar module
- Code Vault for source-code snippets and code-file uploads
- Direct GitHub upload for code snippets from inside Aevum
- Focus timer and study-session logging
- Search across notes, tasks, events, and code snippets
- Public portfolio-style profile page for external viewers
- REST API endpoints for future React/mobile integration
- SQLite database for simple setup
- WhiteNoise static-file handling for deployment

---

# PART 1 – VERY IMPORTANT BEFORE YOU START

If you are using only a phone, the easiest method is:

1. Create a GitHub account.
2. Upload this Aevum project to GitHub.
3. Open the repository in GitHub Codespaces from your phone browser.
4. Run the setup commands exactly as written.
5. Make port 8000 public.
6. Share the public URL with your teacher/external checker.

If you need a more permanent public link, use PythonAnywhere after testing in Codespaces.

---

# PART 2 – EXACT FOLDER STRUCTURE

After extracting the ZIP, the project contains:

```text
Aevum/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                # generated after migrate
├── aevum/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hub/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── github_api.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── api/
│   ├── __init__.py
│   ├── apps.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── templates/
├── static/
└── media/
```

---

# PART 3 – GITHUB UPLOAD FROM PHONE (NO TERMUX)

## Step 1: Create a new GitHub repository

1. Open **https://github.com**.
2. Sign in.
3. Tap the **+** button.
4. Choose **New repository**.
5. Repository name: `aevum`
6. Set it to **Public** if your teacher needs to see the code.
7. Tap **Create repository**.

## Step 2: Upload project files from phone

### Option A – easiest way

If your phone browser supports desktop upload nicely:

1. Open the new repository.
2. Tap **Add file**.
3. Tap **Upload files**.
4. Extract the ZIP on your phone first.
5. Upload the extracted files and folders.
6. Scroll down.
7. Commit message: `Initial Aevum upload`
8. Tap **Commit changes**.

### Option B – if full folder upload is difficult on phone

Use one of these phone apps:

- Acode
- Spck Editor
- GitHub mobile + browser
- Files app + Chrome desktop mode

If folder upload fails, upload in smaller groups.

---

# PART 4 – OPENING AEVUM IN GITHUB CODESPACES FROM PHONE

## Step 1: Open Codespaces

1. Open your GitHub repository.
2. Tap the green **Code** button.
3. Tap **Codespaces**.
4. Tap **Create codespace on main**.
5. Wait until the online VS Code editor opens.

If your phone screen is small:

- Use Chrome
- Turn on **Desktop site**
- Rotate phone to landscape mode if needed
- Use OTG keyboard if available

## Step 2: Open terminal inside Codespaces

In the Codespaces window:

1. Tap the menu
2. Choose **Terminal**
3. Open **New Terminal**

You should now see a terminal prompt.

---

# PART 5 – EXACT COMMANDS TO RUN IN CODESPACES

Copy and run these one by one.

## Command 1 – install packages

```bash
pip install -r requirements.txt
```

## Command 2 – create migrations

```bash
python manage.py makemigrations hub
```

## Command 3 – apply migrations

```bash
python manage.py migrate
```

## Command 4 – create admin account

```bash
python manage.py createsuperuser
```

When prompted, type:

- Username: `admin`
- Email: your email
- Password: choose a strong password

Example password:

```text
Admin@12345
```

## Command 5 – collect static files

```bash
python manage.py collectstatic --noinput
```

## Command 6 – start the server

```bash
python manage.py runserver 0.0.0.0:8000
```

Important:

- Do not close the terminal while the server is running.
- Keep the Codespace active during demo.

---

# PART 6 – HOW TO OPEN THE APP IN BROWSER

After starting the server:

1. Look for a popup saying port 8000 is available.
2. Tap **Open in Browser** if shown.
3. If no popup appears, open the **PORTS** panel.
4. Find port **8000**.
5. Tap the globe/link icon.
6. Open the generated link.

The app will open in a browser tab.

---

# PART 7 – HOW TO SHARE THE LINK WITH EXTERNAL CHECKER

## Codespaces temporary sharing link

By default, Codespaces links are not public.
You must make port 8000 public.

### Exact steps

1. Open the **PORTS** panel in Codespaces.
2. Find port **8000**.
3. Tap or right-click it.
4. Choose **Port Visibility**.
5. Select **Public**.
6. Copy the generated URL.
7. Send that URL to your checker.

### Very important notes

- This link works only while Codespaces is running.
- If Codespaces stops, the link may stop.
- Sometimes the link changes after restart.
- Best for quick demo, viva, or temporary evaluation.

## Permanent sharing option – PythonAnywhere

Use PythonAnywhere if you need a more stable public link.

The final public link will look like:

```text
https://yourusername.pythonanywhere.com
```

---

# PART 8 – LOGIN AND USER FLOW SO YOU DO NOT GET ERRORS

Aevum supports two main account types:

## 1. Normal student user

Student users are created from:

```text
/register/
```

They can:

- log in
- create notes
- create tasks
- create events
- upload code files
- publish code snippets to GitHub
- log focus sessions
- generate public share links

## 2. Admin user

Admin user is created by:

```bash
python manage.py createsuperuser
```

Admin logs in at:

```text
/admin/
```

Admin can inspect all database objects.

---

# PART 9 – FIRST THINGS TO DO AFTER LOGIN

After you create a student account and log in:

## Step 1 – open profile settings

Go to:

```text
/profile/
```

Fill these fields:

- full name
- course
- year level
- bio
- portfolio headline
- GitHub username
- GitHub repo
- GitHub branch
- GitHub token

## Step 2 – save profile

This is important before testing GitHub upload.

---

# PART 10 – HOW GITHUB CODE UPLOAD WORKS INSIDE AEVUM

Aevum allows student code snippets to be uploaded directly to GitHub.

## Before this works, you MUST do all of the following:

1. Create a GitHub repository.
2. Create a GitHub Personal Access Token.
3. Save the token in Aevum Profile Settings.
4. Save your GitHub username.
5. Save the repository name.
6. Save the correct branch name.

## How to create a GitHub Personal Access Token

1. Open GitHub.
2. Go to **Settings**.
3. Go to **Developer settings**.
4. Go to **Personal access tokens**.
5. Choose **Tokens (classic)** or fine-grained token if you know how.
6. Tap **Generate new token**.
7. Give it a note like `Aevum upload token`.
8. Select repo/content write permission.
9. Generate token.
10. Copy the token immediately.

## Add the token to Aevum

Open:

```text
/profile/
```

Fill:

- GitHub username
- GitHub repo
- GitHub branch
- GitHub token

Then click **Save Profile**.

## Upload a code file to GitHub from Aevum

1. Login.
2. Go to **Code Vault**.
3. Create a snippet.
4. Either paste code in the content box OR upload a code file.
5. Open the saved snippet.
6. Tap **Upload to GitHub**.

If everything is correct, Aevum will:

- create a file in your GitHub repository
- save the GitHub link
- show a success message

If not configured, Aevum will show a friendly error instead of crashing.

---

# PART 11 – SUPPORTED CODE FILE TYPES

These file types are accepted:

- `.py`
- `.js`
- `.html`
- `.css`
- `.java`
- `.cpp`
- `.c`
- `.php`
- `.txt`
- `.sql`
- `.json`
- `.md`

---

# PART 12 – HOW TO CREATE PUBLIC SHARE LINKS

Aevum can generate public links for:

- profile portfolio page
- note page
- code snippet page

## Share your public profile

1. Login.
2. Open **Share** in navigation.
3. A public link will be generated.
4. Copy that link.
5. Send it to your teacher/external checker.

## Share a note

1. Open a note.
2. Tap **Share**.
3. Copy the generated link.

## Share a code snippet

1. Open a snippet.
2. Tap **Share**.
3. Copy the generated link.

These pages open without login.

---

# PART 13 – REST API ENDPOINTS

Aevum includes API endpoints at:

```text
/api/
```

Available endpoints:

- `/api/tags/`
- `/api/notes/`
- `/api/tasks/`
- `/api/events/`
- `/api/snippets/`
- `/api/stats/`

These are useful for future React integration.

---

# PART 14 – DETAILED TEST DEMO CHECKLIST FOR CAPSTONE

Before giving the project to checker, do this exact demo:

## Demo 1 – landing page

Open the home page.
Show:

- premium UI
- register button
- login button
- feature cards

## Demo 2 – student registration

Create a student account.
Example:

- Username: `evaluator`
- Password: `Demo@12345`

## Demo 3 – dashboard

Show:

- chart
- stats cards
- recent notes
- recent snippets
- activity heatmap

## Demo 4 – notes module

Create a tag.
Create a note.
Pin it.
Mark it public if needed.
Attach a file if needed.
Open the note detail page.

## Demo 5 – task board

Create a task.
Move it from To Do to Doing to Done.

## Demo 6 – events

Create an event.
Show the event in the event list/calendar page.

## Demo 7 – code vault

Create a code snippet.
Paste code or upload a `.py` file.
Open the snippet detail page.
If GitHub is configured, tap **Upload to GitHub**.

## Demo 8 – focus timer

Open focus page.
Start timer.
Log a focus session.

## Demo 9 – search

Search for note titles, event titles, or snippet content.

## Demo 10 – public sharing

Generate a public profile link.
Open it in incognito mode.
Show it works without login.

## Demo 11 – admin panel

Login at `/admin/` using superuser.
Show all models.

---

# PART 15 – VERY IMPORTANT SETTINGS FOR DEPLOYMENT

Current project supports environment variables:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`

If hosting on Codespaces for demo, you can keep local defaults.
If deploying publicly, set them properly.

Example:

```bash
export DEBUG=False
export ALLOWED_HOSTS=yourusername.pythonanywhere.com,.github.dev
```

---

# PART 16 – COMMON ERRORS AND EXACT FIXES

## Error 1 – `ModuleNotFoundError: No module named django`

Fix:

```bash
pip install -r requirements.txt
```

## Error 2 – `No such table` database error

Fix:

```bash
python manage.py makemigrations hub
python manage.py migrate
```

## Error 3 – static CSS not loading

Fix:

```bash
python manage.py collectstatic --noinput
```

## Error 4 – login page opens but styling is missing

Fix:

- make sure `collectstatic` ran
- refresh browser
- restart server

## Error 5 – GitHub upload fails

Check all of these:

- token is correct
- repo name is correct
- username is correct
- branch name is correct
- repository exists
- token has write permission

## Error 6 – public link does not open for teacher

If using Codespaces:

- make sure port 8000 is **Public**
- keep Codespaces running
- do not close the server terminal

## Error 7 – admin page not accessible

Make sure you created superuser:

```bash
python manage.py createsuperuser
```

---

# PART 17 – PYTHONANYWHERE DEPLOYMENT FOR MORE STABLE EXTERNAL LINK

If you want a more stable public link:

## Step 1
Create account on:

```text
https://www.pythonanywhere.com/
```

## Step 2
Open Bash console there.

## Step 3
Clone your repo:

```bash
git clone https://github.com/YOUR-USERNAME/aevum.git
cd aevum
pip3.10 install --user -r requirements.txt
python3.10 manage.py makemigrations hub
python3.10 manage.py migrate
python3.10 manage.py collectstatic --noinput
python3.10 manage.py createsuperuser
```

## Step 4
Create web app.

## Step 5
Set WSGI file to point to your project.

## Step 6
Reload app.

Now you can share your public domain.

---

# PART 18 – SUGGESTED CAPSTONE SUBMISSION ITEMS

Prepare these:

1. GitHub repository link
2. Live public link
3. Admin login
4. Evaluator login
5. Screenshots
6. PDF capstone report
7. ZIP backup
8. ER diagram image
9. API screenshots
10. Public share screenshot

---

# PART 19 – SUGGESTED EVALUATOR ACCOUNTS

## Admin

- username: `admin`
- password: your own secure password

## Evaluator test account

- username: `evaluator`
- password: `Demo@12345`

Create evaluator using register page.

---

# PART 20 – FINAL SAFE COMMAND LIST FOR PHONE USER

Run these in this exact order inside Codespaces:

```bash
pip install -r requirements.txt
python manage.py makemigrations hub
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
```

Then:

1. open PORTS panel
2. make port 8000 public
3. copy the public URL
4. share the URL

---

# PART 21 – WHAT TO SAY IN YOUR DEMO

You can say:

> Aevum is a premium student management and productivity platform developed using Django, SQLite, Bootstrap 5, JavaScript, and Django REST Framework. It supports student authentication, smart notes, Kanban task management, code-file upload, direct GitHub publishing, event planning, public portfolio sharing, and REST APIs for future expansion.

---

# PART 22 – FINAL REMINDER

If you are on phone only, your safest flow is:

- GitHub for storing code
- Codespaces for running code
- PythonAnywhere for permanent public link

This avoids Termux and avoids local setup problems.
