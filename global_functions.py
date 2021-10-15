#This Code Is Under The MPL-2.0 License
import json

# CONTANTS
MAX_BEG_GAIN = 300
DAILY_AMT = 2000
PREFIX = ">"
MAX_WORK_GAIN = 2000
WEEKLY_AMT = 5000
BOT_USER_ID = "832712190590844968"
MEMBERCOUNT_CHANNEL = 864182952937127948  # membercount channel id here, default is the one in glow's server
UPDATE_CHANNEL = "update channel here"
ERROR_CHANNELS = ["error channel ids here"]
GUILDS = [
    {"server": 815976334907801601},
    {"server": 803080452968808468},
    {"server": 824640805884919849},
]

TOKEN = "token here"
# make sure to remove it before you push


hugs = [
    "https://i.pinimg.com/originals/f2/80/5f/f2805f274471676c96aff2bc9fbedd70.gif",
    "https://i.pinimg.com/originals/85/72/a1/8572a1d1ebaa45fae290e6760b59caac.gif",
    "http://25.media.tumblr.com/tumblr_ma7l17EWnk1rq65rlo1_500.gif",
    "https://i.imgur.com/r9aU2xv.gif?noredirect",
    "https://i.gifer.com/2QEa.gif",
    "https://25.media.tumblr.com/2a3ec53a742008eb61979af6b7148e8d/tumblr_mt1cllxlBr1s2tbc6o1_500.gif",
    "https://media3.giphy.com/media/sUIZWMnfd4Mb6/200.gif",
    "https://i.pinimg.com/originals/f9/e9/34/f9e934cddfd6fefe0079ab559ef32ab4.gif",
    "https://media3.giphy.com/media/wnsgren9NtITS/giphy.gif",
    "https://38.media.tumblr.com/b22e5793e257faf94cec24ba034d46cd/tumblr_nldku9v7ar1ttpgxko1_500.gif",
    "https://i2.wp.com/nileease.com/wp-content/uploads/2020/09/38ff71787d331e2c8c7326846e718c4b.gif?fit=498%2C314&ssl=1",
    "https://i.pinimg.com/originals/0c/bc/37/0cbc377124f2f91d76277160b5803372.gif",
    "https://78.media.tumblr.com/88b9b721e47c33272a3cafd0fdb916b5/tumblr_oqkfe3BbYM1vb10byo1_500.gif",
]

people_list = [
    "Glowstikk",
    "Chill",
    "Vibe",
    "a fellow beggar",
    "drunk boi",
    "the big man",
    "You from a parallel universe",
    "Elon",
    "Siri",
    "Creepy dude with a knife who is now prolly watching you and is bout to eat you tmmr :)",
    "Dream",
    "¯\_(ツ)_/¯",
    "you?",
    "I",
    "Discord",
    "Your Dad",
    "Your Mom",
    "Your family who is really unhappy with you because your let everyone down by becoming a redditor",
    "Your imaginary gf :rofl:",
    "the street",
]

ban_msg = [
    "flew to close to the radar and got banned",
    "messed up bad and got banned",
    "has been struck by the BAN HAMMER",
    "annoyed some staff and got banned",
    "wanted to see what would happen if you broke rules and got banned",
    "tried to dodge the ban hammer :rofl:",
    "was blown up by Creeper"
    "was killed by [Intentional Game Design]"
    "tried to swim in lava"
    "experienced kinetic energy"
]


kick_msg = [
    "got booted and got kicked?",
    "got kicked, imagine getting kicked...",
    "got kicked... I ran out of jokes",
]

work_list = ["Discord", "Microsoft", "Apple", "a Police Station", "Youtube", "Google"]

options = [
    "uber",
    "taxi",
    "doorstep",
    "locker",
    "grass",
    "couch",
    "house",
    "bush",
    "street",
    "lake",
]

choices = ["get no", "gained"]
# test

bank_memberships = [
    {
        "name": "Basic Membership - ``$100,000``",
        "description": "Store up to $100,000 in your bank",
    },
    {
        "name": "Silver Membership - ``$500,000``",
        "description": "Store up to $250,000 in your bank",
    },
    {
        "name": "Diamond Membership - ``$1,000,000``",
        "description": "Store up to $500,000 in your bank!",
    },
    {
        "name": "Magical Membership - ``$1,500,000``",
        "description": "Store up to $1,000,000 in your bank!",
    },
    {
        "name": "Epik Membership - ``$2,500,000``",
        "description": "Store up to $2,000,000 in your bank!",
    },
    {
        "name": "Glow Membership - ``$5,000,000``",
        "description": "Store up to $10,000,000 in your bank!",
    },
]

bank_membership_conversions = [
    {
        "name": "basic membership",
        "nickname": "basic",
        "price": 100_000,
        "amount": 100_000,
    },
    {
        "name": "silver membership",
        "nickname": "epic",
        "price": 500_000,
        "amount": 250_000,
    },
    {
        "name": "diamond membership",
        "nickname": "magical",
        "price": 1_000_000,
        "amount": 500_000,
    },
    {
        "name": "magical membership",
        "nickname": "diamond",
        "price": 1_500_000,
        "amount": 1_000_000,
    },
    {
        "name": "epik membership",
        "nickname": "silver",
        "price": 2_500_000,
        "amount": 2_000_000,
    },
    {
        "name": "glow membership",
        "nickname": "exotic",
        "price": 5_000_000,
        "amount": 10_000_000,
    },
]

responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
]


shop_display = [
    {"name": "Laptop", "price": "``$5,000``", "description": "Used for posting memes"},
    {"name": "Phone", "price": "``$1,000``", "description": "Bored? Well look at some memes!"},
    {"name": "Nothing", "price": "``$500,000``", "description": "It's literally nothing, why would you waste your money"},
    {"name": "Glow", "price": "``$100,000``", "description": "FLEX"},
]


shop_buy = [
    {"name": "laptop", "nickname": "lap", "price": 5_000, "sell": 2_500},
    {"name": "phone", "nickname": "cell", "price": 1_000, "sell": 500},
    {"name": "glow", "nickname": "glow", "price": 100_000, "sell": 10_000},
    {"name": "nothing", "nickname": "air", "price": 500_000, "sell": 250_000}
]


def fetch_data(fn):
    with open("json/" + str(fn), "r") as f:
        data = json.load(f)
    return data


def write_data(fn, data):
    with open("json/" + str(fn), "w") as f:
        json.dump(data, f, indent=4)
