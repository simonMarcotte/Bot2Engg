#!/usr/bin/python3
import subprocess
import argparse
import time

class BotUpdate:
    
    def __init__(self):
        with open('project.txt') as f:
            self.PROJECT = f.readline()

        self.local_bot_script_path = 'bot2engg.py'
        self.local_app_key_path = 'token.txt'
        self.local_req_path = 'requirements.txt'
        self.remote_path = '~/'
        self.base_ssh_command = f'gcloud compute ssh --zone "us-west1-a" "discord-bot-vm" --tunnel-through-iap --project {self.PROJECT} --command'
        self.scp_commands = [
                f'gcloud compute scp {self.local_bot_script_path} discord-bot-vm:{self.remote_path}{self.local_bot_script_path} --tunnel-through-iap --zone "us-west1-a" --project {self.PROJECT}',
                f'gcloud compute scp {self.local_app_key_path} discord-bot-vm:{self.remote_path}{self.local_app_key_path} --tunnel-through-iap --zone "us-west1-a" --project {self.PROJECT}',
                f'gcloud compute scp {self.local_req_path} discord-bot-vm:{self.remote_path}{self.local_req_path} --tunnel-through-iap --zone "us-west1-a" --project {self.PROJECT}'
            ]
        self.create_venv = 'python3 -m venv .venv'
        self.load_venv = 'source .venv/bin/activate && pip install -r requirements.txt'
        self.run_bot_command = f'source .venv/bin/activate && nohup python3 {self.remote_path}bot2engg.py > my.log 2>&1 &'
        self.stop_bot_command = "ps ax | grep bot2engg.py | grep -v grep | awk '{print $1}' | xargs -r kill -9"
        self.cleanup = 'rm ~/*'
        self.process = None

    def start_shell_session(self):
        self.process = subprocess.Popen(
            f"{self.base_ssh_command} 'bash -l'",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

    def run_command(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

    def close_shell_session(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait()

    def transfer_files(self):
        print("Cleaning Old Files...")
        self.run_command(self.cleanup)
        time.sleep(0.5)
        print("Transferring files...")
        combined_scp_command = " && ".join(self.scp_commands)
        subprocess.run(combined_scp_command, shell=True)

    def setup_venv(self):
        print("Setting up and activating virtual environment, and installing requirements...")
        self.run_command(self.create_venv)
        self.run_command(self.load_venv) 

    def run_bot(self):
        print("Starting bot on VM...")
        self.run_command(self.run_bot_command)

    def stop_bot(self):
        # if something fails, try: ps ax | grep bot, then kil -9 PID
        print("Stopping bot on VM...")
        self.run_command(self.stop_bot_command)

def main():
    parser = argparse.ArgumentParser(description="Manage the Discord bot on GCP VM")
    parser.add_argument('--action', choices=['transfer', 'setup', 'run', 'stop'], required=True, help="Action to perform on the bot")

    args = parser.parse_args()
    bot_update = BotUpdate()
    bot_update.start_shell_session()

    if args.action == 'transfer':
        bot_update.transfer_files()
    elif args.action == 'setup':
        bot_update.setup_venv()
    elif args.action == 'run':
        bot_update.run_bot()
    elif args.action == 'stop':
        bot_update.stop_bot()

    bot_update.close_shell_session()

if __name__ == "__main__":
    main()