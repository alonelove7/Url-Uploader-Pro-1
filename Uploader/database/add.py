
        


from pyrogram import Client
from Uploader.database.database import db, Database
from pyrogram.types import Message



async def add_user_to_database(uid, fname, lname):
    try:
        userDetails = {
            "_id": uid,
            "name": f"{fname} {lname}",
        }
        Database.tellybots.users.insert_one(userDetails)
        print(f"New user added id={uid}\n{fname} {lname} \n")
    except DuplicateKeyError:
        print(f"Duplicate Entry Found for id={uid}\n{fname} {lname} \n")
    return
