# AUTOMATIC JOB BOARD NOTIFICATIONS

## Setup Instructions:

### Set up the Code
1) Download this repository by pressing XXXXXXXXX
2) If you don't have Python, download the latest version of Python (https://www.python.org/downloads/)
3) If you haven't done so already, set up Docker locally by going to https://docs.docker.com/desktop/, clicking Install Docker Desktop at the bottom, and following the instructions on the website.
4) Sign in to Docker Desktop
5) FINALLY, cut and paste `.wslconfig` from here to your `C:\Users\{Your User}` folder (cutting is okay, we don't need it here!)
    - I found that starting up Docker through a command would allocate it 100% of my CPU usage. This limits Docker's resources and lets everything run normally :)

#

### How This Works

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

### Update your Preferences

Open the app/config file within the files you downloaded. You should see 5 files, titled `allow_list`, `block_list`, `email`, `job_boards`, and `jobs_seen`

1) In `allow_list.txt`, add words that you want to see in your job titles.
2) In `block_list.txt`, add words to be filtered out from jobs found by the `allow_list`


 `job_boards` - the jobs boards you want to be checked, with each job board on a new line.

 `allow_list` - any words that, if they appear in a job title, will have the job listing be sent to you, with each word on a new line.

 `block_list` - any words that, if they appear in a job title, will PREVENT the job listing from being sent to you, with each word on a new line.

 `jobs_seen` - a list of jobs that have already been sent, no need to change this!

 `email` - the email at which you want to receive notifications.

#


### Update your Email Information

In `email.txt`, you need to put in information so that the application can send you the notifications you want to receive
- Replace `email@test.com` with your email address.
- The second line will be your APPLICATION PASSWORD (this is different from normal password.) You can find it here https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237. 
- replace `aaaa bbbb cccc dddd` with the application password you generated.

#

### AUTOMATING THE PROGRAM ENTIRELY 

 This sets up the program to run automatically when you log into your computer.



#### Set Up Executable

We need to set up the automatic function to work with your machine specifically.

1) In the code you downloaded, right-click `window_scheduler.bat` and click `Edit`
2) Search for `Docker Desktop.exe` on your computer. 
3) Press Shift + Right-Click `Docker Desktop.exe`, and click `Copy as Path`.
4) Back in `window_scheduler.bat`, replace `DOCKER_LOCATION` with what you just copied (leaving the quotation marks)
5) repeat steps 2-4, but replace `APP_LOCATION` with the `job-alerts` folder (this project!)
6) save the file


#### Set Up Automation

 Windows:
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

 Mac:

    unknown lmk ty


### Feedback 
If you have any questions or feedback about this documentation, email me at `robert.gugliel@gmail.com` to help improve this process!