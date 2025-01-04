import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")
client = OpenAI(
            base_url=os.getenv("llm_host"),
            api_key="lm studio"
        )




@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user}')


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
        
    # Check if the bot is mentioned
    if bot.user in message.mentions:
        # Remove the bot mention and get the actual message
        prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        try:
            # Get response from OpenAI
            response = client.chat.completions.create(
                model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
                messages=[
                    {"role": "system", "content": "You are a a discord bot that only responds in lymrics. This lymrics will always involve touching or licking someone known as " + message.author.name},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Send the response
            await message.reply(response.choices[0].message.content.strip(""))
        except Exception as e:
            print(e)
            await message.reply("Sorry, I encountered an error processing your request.")
    
    # Check if the message is from tanner04345
    if message.author.name == 'tanner04345':
        # Add handprint reaction
        await message.add_reaction('👋')
    
    # Process commands if any
    await bot.process_commands(message)


bot.run(os.getenv('DISCORD_TOKEN'))
