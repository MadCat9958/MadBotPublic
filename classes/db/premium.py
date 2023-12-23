from . import client

from typing import Optional

async def get_premium_user(user_id: int) -> Optional[dict]:
    db = client.premium
    coll = db.user
    return await coll.find_one({'user_id': str(user_id)})

async def give_premium(user_id: int, type: str) -> bool:
    """
    Gives premium for a user.

    Arguments:
    - `user_id` - ID of the user.
    - `type` - Type of the premium ('user' | 'server').
    """
    db = client.premium
    coll = db.user
    await coll.insert_one({'user_id': str(user_id), 'type': type})
    return True

async def take_premium(user_id: int) -> bool:
    """
    Takes premium from the user.

    Arguments:
    - `user_id` - ID of the user.
    """
    db = client.premium
    coll = db.user
    await coll.delete_one({'user_id': str(user_id)})
    return True

def get_premium_guids(user_id: int) -> Optional[dict]:
    """
    Gets all servers, where the user gave premium.

    Arguments:
    - `user_id` - ID of the user.
    """
    db = client.premium
    coll = db.guild
    return coll.find({'user_id': str(user_id)})

async def get_premium_guild_info(guild_id: int) -> Optional[dict]:
    """
    Gets info about premium server.

    Arguments:
    - `guild_id` - ID of the guild.
    """
    db = client.premium
    coll = db.guild
    return await coll.find_one({'guild_id': str(guild_id)})

async def take_guild_premium(guild_id: int) -> bool:
    """
    Takes premium from the guild.

    Arguments:
    - `guild_id` - ID of the guild.
    """
    try:
        db = client.premium
        coll = db.guild
        await coll.delete_one({'guild_id': str(guild_id)})
        return True
    except Exception as e:
        raise e