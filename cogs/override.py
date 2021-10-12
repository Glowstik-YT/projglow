import nextcord
from nextcord.ext import commands
from global_functions import BOT_USER_ID


class BanConfirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.green, custom_id="yes"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()


class Override(commands.Cog):
    def __init__(self, client):
        self.client = client

        @commands.command()
        @commands.has_permissions(kick_members=True)
        async def modban(self, ctx, member: nextcord.Member = None, *, reason=None):
            if member == None:
                embed1 = nextcord.Embed(
                    title="Ban Error", description="Member to ban - Not Found"
                )
                return await ctx.send(embed=embed1)
            if member.id == ctx.author.id:
                embed69 = nextcord.Embed(
                    title="Ban Error",
                    description="Can not ban yourself, trust me I woulda ages ago <:hehe:796743161208504320>",
                )
                return await ctx.send(embed=embed69)
            elif ctx.author.top_role.position < member.top_role.position:
                em3 = nextcord.Embed(
                    title="Ban Error",
                    description="Member **higher** than you in the role heirarchy - Invalid Permission",
                )
                return await ctx.send(embed=em3)
            elif ctx.author.top_role.position == member.top_role.position:
                em3 = nextcord.Embed(
                    title="Ban Error",
                    description="Member has same role as you in the role heirarchy - Invalid Permission",
                )
                return await ctx.send(embed=em3)
            em = nextcord.Embed(
                title="Are you sure?",
                description="This is a very risky command only to be used in important situations such as, `NSFW or NSFLPosting` or `Raid on the Server`. Only use this command if no admin is online or responding. **If this command is used for the wrong purpose you may risk getting demoted if not banned from the staff team.**",
            )
            view = BanConfirm()
            ctx.author.send(embed=em, view=view)


def setup(client):
    client.add_cog(Override(client))
