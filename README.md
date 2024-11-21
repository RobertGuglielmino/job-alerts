# AUTOMATIC JOB BOARD NOTIFICATIONS

## Setup Instructions:

The summary for how to set up the application:

1) [DOWNLOAD](#set-up-the-code) - Download the code, and Set Up Docker to run the code 
2) [PREFERENCES] - (#update-your-preferences) Set up your job preferences
3) [AUTOMATE] - (#automating-the-program-entirely) Set your computer to run the code when you log in

The rest is step by step details for accomplishing those things.

### 1. Set up the Code
1) Download this application using one of the following:
 
    If you don't use github regularly,
    - Press `Code`
    - Press `Download ZIP`
    - Unzip the code wherever you would like.

    Otherwise, `git clone https://github.com/RobertGuglielmino/job-alerts.git`
2) If you haven't done so already, set up Docker locally by going to https://docs.docker.com/desktop/, clicking Install Docker Desktop at the bottom, and following the instructions on the website.
3) Sign in to Docker Desktop
4) WINDOWS ONLY -  cut and paste `.wslconfig` from here to your `C:\Users\{Your User}` folder (cutting is okay, we don't need it here!)
    - This issue may exist on Mac but I don't have a test device yet
    - I found that starting up Docker through a command would allocate it 100% of my CPU usage. This limits Docker's resources and lets everything run normally :)

#

#### How This Works

This program works off of Allow Lists and Block Lists to target the exact job titles you are looking for.


Let's say our `allow_list` contains `Software` and `Cloud`, and `block_list` contains `Lead`. We have the following jobs that we COULD be interested in.
 ```
Software Engineer II
Lead Software Engineer
Cloud Engineer 
Electrical Engineer
 ```

 First, `ALLOW` will add `Cloud Engineer`, `Lead Software Engineer`, and `Software Engineer II` to the, and then `BLOCK` will remove `Lead Software Engineer` from the list.

#

### 2. Update your Preferences

Open the app/config file within the files you downloaded. You should see 5 files, titled `allow_list`, `block_list`, `email`, `job_boards`, and `jobs_seen`

1) In `allow_list.txt`, add words that you want to see in your job titles.
2) In `block_list.txt`, add words to be filtered out from jobs found by the `allow_list`

#

If you're curious, here is additional info on each of the files:

 `job_boards` - the jobs boards you want to be checked, with each job board on a new line.

 `allow_list` - any words that, if they appear in a job title, will have the job listing be sent to you, with each word on a new line.

 `block_list` - any words that, if they appear in a job title, will PREVENT the job listing from being sent to you, with each word on a new line.

 `jobs_seen` - a list of jobs that have already been sent, no need to change this!

 `email` - the email at which you want to receive notifications.

#


#### Update your Email Information

In `email.txt`, you need to put in information so that the application can send you the notifications you want to receive
- Replace `email@test.com` with your email address.
- The second line will be your APPLICATION PASSWORD (this is different from normal password.) You can find it here https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237. 
- replace `aaaa bbbb cccc dddd` with the application password you generated.

#


#### Add Job Boards to Watch

In `job_boards.txt`, add url links to the job boards you want to watch. Add each job link on a new line. The application also works if the job board lets you filter by location or department - filter first, copy the url, and put it in!

It should look like the following. 

```
https://www.talkiatry.com/jobs
https://discord.com/careers
https://motionrecruitment.com/tech-jobs?remote=true&keywords=software&start=0
```

#

### 3. AUTOMATING THE PROGRAM ENTIRELY 

 This sets up the program to run automatically when you log into your computer.

Click here if you use [Windows](#windows---set-up-automation)

Or click here for [Mac](#mac---set-up-automation)

#### Windows - Set Up Automation

 
We need to set up the automatic function to work with your machine specifically.

1) In the code you downloaded, right-click `window_scheduler.bat` and click `Edit`
2) Search for `Docker Desktop.exe` on your computer. 
3) Press Shift + Right-Click `Docker Desktop.exe`, and click `Copy as Path`.
4) Back in `window_scheduler.bat`, replace `DOCKER_LOCATION` with what you just copied (leaving the quotation marks)
5) repeat steps 2-4, but replace `APP_LOCATION` with the `job-alerts` folder (this project!)
6) save the file

After this, we can set the computer to run the machine as you log in.

 1) Press `Windows + S`
 2) Type `Task Scheduler`
 3) Open `Task Scheduler`
 4) On the right, click on `Create Basic Task...`
 5) In Name section, type `Automated Job Notifier`
 6) In Description section, type `Automated Job Notifier`
 7) For the trigger, have the task start `When I log on`
    - Enable Advanced Settings
    - Check box for "Delay task for", and select `1 minute` in the drop down
 8) For the action, click `Start a program`
    - Paste the program path for `window_scheduler.bat` (you can search `window_scheduler.bat` in the Browse window as well!)
 9) Click Next.
 10) Click Next, Again.

#### Mac - Set Up Automation

 1) Find and start `Automater.app`
 2) Select `Application`
 3) Click `Show Library` in the toolbar, if hidden
 4) Add `Run shell script` from Actions/Utilities
 5) Copy-Paste the contents of `mac_scheduler.sh` into the window.
 6) Save it as `job_board_tracker.app` somewhere on your device (desktop works!) 
 7) Go to `System Preferences` -> `General` -> `Login Items`
 8) Add `job_board_tracker.app`

#

We're done! Log out, log back in, and see if Docker starts up, and that you get an email!

### Feedback 
If you have any questions or feedback about this documentation, email me at `robert.gugliel@gmail.com` to help improve this process!