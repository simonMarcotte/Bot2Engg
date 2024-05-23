# BOT2ENGG Discord Bot

This is a discord bot, previously used in B2E in 2023.

Terraform is used to provision a Google Cloud VM, and then the `deploy_bot.py` script interacts with it to update, start, and stop the bot remotely.

### Usage

To use shell scripts, please make sure the `deploy_bot.py` script is an executable. This can be done on linux with `chmod +x <file_name>`

`sh run_all.sh` will clean up old files, transfer in new ones with scp, and then download new requirements into the .venv. Make sure the .venv is set up, and make sure pip is installed on the VM before running this script.
After setting the environment, the bot will be run in the background with `nohup`

`sh stop_all.sh` will remove all instances of the filename of the bot. If something goes wrong here, and the bot fails to terminate, use `ps ax | grep <filename> | grep -v grep` to find the PIDs of the active instances. Kill them with `kill -9 <PID>`

## Features

Once the bot is running, please use `?info` to see a list of avaiable commands.

The current list is as follows:
- ?guess (num1) (num2), where num1 is lower than num2, and they are space-separated.
  - With this command, you can play a guessing game. Use the command a try it out!
- ?gpa (Course Units) (Letter Grade), (Course Units 2) (Letter Grade 2), ...
  - Calculates your GPA with as many course as you like (ex formatting: '?gpa 3.5 A+, 4.0 B+, 3.8 C+' etc)
- ?joined @user
  - Find out when a user joined the server! Please be mindful of pinging them...
- ?countforus
  - toggles on or off. If on, I will count one extra number after you
- ?eightball (your question here)
  - I am all knowing. I will answer every question you provide to me