import discord
import asyncio
import urllib.request
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Api for insults
insultURL = 'https://insult.mattbas.org/api/insult'
insultParam = '?who'

# Api for cats
catURL = 'http://thecatapi.com/api/images/get'
catPath = 'cat.jpg'

# Default prefix
prefix = '!'

# Create instance of client
client = discord.Client()

# When client becomes ready, execute this method asynchronously
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + '#' + client.user.discriminator)

# When client recieves a message, execute this method asynchronously
@client.event
async def on_message(message):
    # Use the global variable for prefix, not the local one
    global prefix

    # When a recieved message starts with !insult, execute this if statment
    if message.content.startswith(prefix + 'insult'):

        # If the message contains no mentions
        if len(message.mentions) == 0:

            # Get the insult from the insult api
            response = urllib.request.urlopen(insultURL).read().decode('utf-8')

            # Send the insult
            await client.send_message(message.channel, response)

            # Exit the method on_message i.e. don't do the next part
            return

        # For each mention in the message
        for user in message.mentions:

            # Get the third person insult 
            response = urllib.request.urlopen(insultURL+insultParam).read().decode('utf-8')

            # Sent the insult with the mentioned user's name prepended
            await client.send_message(message.channel, user.mention + ' ' + response)
        
    elif message.content.startswith(prefix + 'prefix'):

        # Change the global variable from ! to the user input
        prefix = message.content.replace(prefix + 'prefix', '').strip()
        await client.send_message(message.channel, 'The prefix has been set to ' + prefix)

    # Make cats appear
    elif message.content.startswith(prefix + 'cat'):

        # Creates a response from the cat API
        response = requests.get(catURL, stream = True)

        # Check that it's valid
        if response.status_code == 200:

            # Let us refer to the designated space in memory as f, and close it again when done
            # 'wb' tells Windows we will be writing to this space in binary
            with open(catPath, 'wb') as f:

                # Go through the stream and write the image to f
                for chunk in response:
                    f.write(chunk)

        # Send the image
        await client.send_file(message.channel, catPath)

if __name__ == '__main__':
    client.run(config.get('DISCORD', 'TOKEN'))