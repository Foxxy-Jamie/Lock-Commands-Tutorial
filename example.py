import asyncio
import aiosqlite
import nextcord
from nextcord.ext import commands

#! THIS DOES NOT START YOUR BOT. THIS IS A COG FILE
# DO NOT PUT locked() CHECK ON MODERATION COMMANDS. 

#To use in other Cog Files do:
from COG_FOLDER_NAME.FILENAME import locked
#If needing Help Join Hatake Blustone Here: https://discord.gg/tJjs7yfY4R


#Checks to see if the Bot is Locked to a Channel
def locked():
    async def check_locks(ctx):
        async with aiosqlite.connect('main.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT channel FROM bot_lock WHERE guild = ?", (ctx.guild.id,))
                check1 = await cursor.fetchone()
                if check1 == None:
                    return True
                elif check1[0] != ctx.channel.id:
                    return False
                else:
                    return True
    return commands.check(check_locks)

class COG_NAME_HERE(commands.Cog):
    """Cog Description Here"""
    def __init__(self,bot):
        self.bot = bot
    
#! REMEMBER TO CHANGE "main.db" TO YOUR DATABASE NAME

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'COG_NAME_HERE cog has been loaded')
        setattr(self.bot, "db", await aiosqlite.connect("main.db"))
        await asyncio.sleep(3)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS bot_lock(channel INTEGER, guild INTEGER)")
        print('-------------------------')

#* This is to lock the bot to the Channel!

    @commands.command()
    async def lockbot(self, ctx):
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM bot_lock WHERE guild = ?", (ctx.guild.id,))
            check1 = await cursor.fetchone()
            if check1 is None:
                await cursor.execute("INSERT INTO bot_lock VALUES (?, ?)", (ctx.channel.id, ctx.guild.id,))
                await ctx.reply("I have been locked to this channel")
                await self.client.db.commit()
                return
            else:
                return await ctx.reply("I am Already Locked")
    
    @commands.command()
    async def unlockbot(self, ctx):
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM bot_lock WHERE guild = ?", (ctx.guild.id,))
            check1 = await cursor.fetchone()
            if check1 is None:
                return ctx.reply("I was never locked :confused:")
            else:
                await cursor.execute("DELETE FROM bot_lock WHERE guild = ?", (ctx.guild.id,))
                await ctx.reply("I have been allowed to roam free once again")
                await self.client.db.commit()
                return

#* The Locked Check will connect to your database where it will return true or false
#* If the return is False it will start the CheckFailure Error. 

    @commands.command()
    @locked()
    async def testloc(self, ctx):
        await ctx.send("OOP I did something")

#! REMEMBER TO CHANGE THE <COG_NAME_HERE> AT THE BOTTOM AND TOP OF THE PAGE

def setup(bot):
    bot.add_cog(COG_NAME_HERE(bot))     
