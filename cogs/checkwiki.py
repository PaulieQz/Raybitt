import nextcord
from nextcord.ext import commands
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from transformers.data.processors.utils import InputExample
import torch
from datetime import datetime, timedelta

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("fine_tuned_model")


class DumbassDetector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_cooldowns = {}  # Dictionary to store cooldown times for users

    async def is_hacking_question(self, sentence):
        inputs = tokenizer(sentence, return_tensors="pt")
        outputs = model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=1)
        prob_how_to_hack = predictions[0][1].item()
        return prob_how_to_hack > 0.7

    async def check_role(self, member):  # changed ctx to member for clarity
        found = False
        for role in member.roles:
            if role.name == "Level 1":
                return True
        return False


    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if user is on cooldown
        if message.author.id in self.user_cooldowns:
            cooldown_time = self.user_cooldowns[message.author.id]
            if datetime.now() < cooldown_time:
                return  # Exit early if the user is on cooldown

        role = await self.check_role(message.author)
        if role:
            return
        else:
            if message.author == self.bot.user:
                return
            if await self.is_hacking_question(message.content):
                response = ("Explore hacking the right way. Start here: "
                           "https://wiki.subhackers.org/en/getting-started/Offensive-Security-Reading-List")
                await message.channel.send(response)
                # Set a cooldown for this user
                self.user_cooldowns[message.author.id] = datetime.now() + timedelta(hours=1)
            else:
                return


def setup(bot):
    bot.add_cog(DumbassDetector(bot))
