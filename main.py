import discord
import os
import requests
import json 
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

beer_words = [
    'cerveza',
    'birra',
    'beer',
    'caña',
    'pinta',
    'tercio',
    'mediana',
    'quinto',
    'trago',
    'frias'
]

beer_msg = [
    "¡Saliendo una cerveza bien fría! :beer:",
    "¡Hey! ¿Alguien pidió una birra? :beer:",
    "Se te ve cansado... toma esta cerveza, ¡la casa invita! :beer:",
    "Luego de un largo viaje a través del espacio siempre viene bien una buena cerveza, ¡Salud! :beer:",
    "Toma tu birra, Tigu te llevará a la zona de invitados :beer:"
]

beer_gif = [
    "https://tenor.com/view/beer-drink-gif-21009891",
    "https://tenor.com/view/beer-drink-gif-21009891",
    "https://tenor.com/view/go-to-sleep-friday-freedom-beer-bottoms-up-gif-14637245",
    "https://tenor.com/view/beer-german-celebrate-party-gif-5579802",
    "https://tenor.com/view/thirsty-homer-simpson-beer-gif-8852319",
    "https://tenor.com/view/gaffel-gaffel-k%C3%B6lsch-k%C3%B6lsch-k%C3%B6ln-k%C3%B6lle-gif-17284876",
    "https://tenor.com/view/girl-beer-water-mug-sexy-gif-5080287"
]

if "responding" not in db.keys():
    db["responding"] = True

# Obtener la Cita Motivacional
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    print(json_data)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

@client.event
async def on_ready():
    print("Hemos entrado como {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #variable para el contenido del mensaje
    msg = message.content

    # Comando para saludar
    if msg.startswith('$hola'):
        await message.channel.send("¡Hola!")

    # Comando para frase motivacional
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        # Enviar un mensaje con gif si el mensaje contiene alguna palabra de la lista beer_words
        if any(word in msg for word in beer_words):
            await message.channel.send(random.choice(beer_msg))
            await message.channel.send(random.choice(beer_gif))

    if msg.startswith("$resp"):
        value = msg.split("$resp ",1)[1]

        if value.lower() == "on":
            db["responding"] = True
            await message.channel.send(":white_check_mark: **Las respuestas automáticas están activadas.**")
        elif value.lower() == "off":
            db["responding"] = False
            await message.channel.send(":x: **Las respuestas automáticas están desactivadas.**")
        else:
            await message.channel.send(":warning:  Estás usando una sintáxis que no reconozco. \nEl comando `$resp` solo admite 2 parámetros: \n- `on` para activarlo \n- `off` para desactivarlo")

keep_alive()
client.run(os.environ['TOKEN'])
