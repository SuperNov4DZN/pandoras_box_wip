import pyrebase, os, json, discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv(dotenv_path="secrets\.env")

read_env = os.getenv
_PATH_JSON_DB = 'data/simpleDB_DB.json'

# region Data base configurations
dbconfig = {
    "apiKey": read_env("BOT_apiKey"),
    "authDomain": read_env("BOT_authDomain"),
    "databaseURL": read_env("BOT_databaseURL"),
    "projectId": read_env("BOT_projectId"),
    "storageBucket": read_env("BOT_storageBucket"),
    "messagingSenderId": read_env("BOT_messagingSenderId"),
    "appId": read_env("BOT_appId"),
    "measurementId": read_env("BOT_measurementId")
}

firebase = pyrebase.initialize_app(dbconfig)

db = firebase.database()
# endregion


class ExtensionSimpleDB(commands.Cog, name="Simple DB"):
    def __init__(self, client):
        self.client = client

    @commands.command(name='idb', aliases=['db','insert'])
    async def command_insert(self, ctx, user: discord.User, role: discord.Role):
        message_author = ctx.message.author.mention # author

        if os.stat(_PATH_JSON_DB).st_size == 0: # if file is empty
            json_data = {}# init an empty json
        
        else:
            with open(_PATH_JSON_DB, 'r') as f: # attempt to open file
                try:
                    json_data = json.load(f)
                
                except json.decoder.JSONDecodeError: # badly formatted JSON file
                    raise ValueError(f'ExtensionSimpleDB.command_insert(): JSONDecodeError in {_PATH_JSON_DB}')
        
        uid = str(user.id)
        rid = str(role.id)

        if json_data.get(uid) is not None: # user exists
            # add role if it's not there yet
            if rid not in json_data[uid]['role_id']:
                json_data[uid]['role_id'].append(rid)

            if role.name not in json_data[uid]['role_name']:
                json_data[uid]['role_name'].append(role.name)

        else: # user doesn't exists
            # print('falls under the else')
            user_dict = {
                'user_name': user.name,
                'role_id': [rid],
                'role_name': [role.name]
            }

            json_data.update({uid: user_dict})
        
        # write to file
        with open(_PATH_JSON_DB, 'w') as f:
            f.seek(0)
            json.dump(json_data, f, indent=4)
            db.child("users").child(uid).set(json_data[uid])


def setup(client):
    client.add_cog(ExtensionSimpleDB(client))