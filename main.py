from colorama import Fore, Style, init
from discord.ext import commands
import paramiko, discord, os
init()

class ssh_controller():
    def __init__(self, host, username, password):
        self.client   = paramiko.SSHClient()
        self.password = password
        self.username = username
        self.host     = host
        self.ssh      = 22

    def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname= self.host, username= self.username, password= self.password)

    def send_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return str(stdout.read()).split('b\'')[1].split("\\n'")[0].replace('\\n', '\n')

class discord_client():
    def __init__(self, prefix, token, host, username, password):
        self.client   = commands.Bot(command_prefix= prefix)
        self.password = password
        self.username = username
        self.token    = token
        self.host     = host

        self.ssh = ssh_controller(self.host, self.username, self.password)

        client = self.client
        client.remove_command("help")

        @client.event
        async def on_ready():
            os.system('cls' if os.name == 'nt' else 'clear')
            await self.client.change_presence(activity=discord.Game(name=">help | SSH Bot | Suicidal Security"))
            print(f"""
    
{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] SSH Bot was connected on {Fore.RED}{self.client.user.name}#{self.client.user.discriminator}""")
            self.ssh.connect()
            print(f'{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] SSH Bot Connected to  ({Fore.RED}{self.username}{Fore.WHITE}@{Fore.GREEN}{self.host}:NICETRYNIGGA{Fore.WHITE}{Fore.WHITE})')
            
        @client.command()
        async def ssh(ctx, *, command):
            await ctx.send(f'```{self.ssh.send_command(command)}```')
        
        client.run(self.token)

discord_client('BOT PREFIX', 'BOT TOKEN', 'SERVER IP(ssh server)', 'SERVER USERNAME', 'SERVER PASS')
