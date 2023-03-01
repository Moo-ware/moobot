import discord
import openai
import owoify
import json
from discord.ext import commands

f = open('apikey.json')
data = json.load(f)
openaikey = data.get('openaitoken')

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'owoify', aliases = ['owo'])
    async def owo(self, ctx, *, text = None):
        if text is not None:
            await ctx.send(owoify.owoify(text))
            
        else:
            channel = ctx.channel
            messages = [message async for message in channel.history(limit=2)]
            msg = messages[1].content
            
            if (msg[:1] + msg[-1:]) == '<>':
                pass
            else:   
                await ctx.send(owoify.owoify(messages[1].content))


    @commands.command(name = 'askgpt', aliases = ['ask'])
    async def askgpt(self, ctx, temp, *, body = None):
        if body is not None:
            openai.api_key = f"{openaikey}"
            response = openai.Completion.create(
                model="text-davinci-003", 
                prompt="{}".format(body), 
                temperature= float(temp), 
                max_tokens=1000)

            responseFormat = response.choices[0].text
            
            await ctx.send('```\n{}```'.format(responseFormat))
        else:
            await ctx.send('Please provide information')


async def setup(bot):
    await bot.add_cog(fun(bot))
    