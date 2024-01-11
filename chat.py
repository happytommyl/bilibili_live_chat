""" connect to bilibili live room and send chat. """

import asyncio
import configparser
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from bilibili_api import live, Credential, Danmaku


def load_conf(path):
    """return a configparser for the configuration information from given path"""
    conf = configparser.ConfigParser(interpolation=None)
    conf.read(path)
    return conf


def load_cred(parser):
    """return the credential infomation to login the chat room. """
    credential = parser.items("Credential")
    sessdata, buvid3, bili_jct = [i[1] for i in credential]
    credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3)
    return credential


def load_room(parser):
    """return the room id. """
    room = parser.items("Room")
    return int(room[0][1])


def setup(path):
    """return the configuration information"""
    config = load_conf(path)
    credential = load_cred(config)
    room = load_room(config)

    return [room, credential]


async def live_chat(room_id, cred):
    """background process to display the live chat"""
    danmaku = live.LiveDanmaku(room_id, credential=cred)

    @danmaku.on('DANMU_MSG')
    async def on_danmaku(event):
        """print out the sender and the chat content"""
        print(f"{event['data']['info'][2][1]}: {event['data']['info'][1]}")

    try:
        await danmaku.connect()
    except asyncio.CancelledError:
        print("Background task cancelled.")


async def shell(room_id, cred):
    """a prompt session where you can type in and send chat."""
    session = PromptSession(">>> ")
    room = live.LiveRoom(room_id, credential=cred)
    while True:
        try:
            result = await session.prompt_async()
            if result.find("exit") == -1:
                exit()
            if result != "":
                await room.send_danmaku(Danmaku(result))
        except (EOFError, KeyboardInterrupt):
            return


async def main(room_id, cred):
    """entry point"""
    with patch_stdout():
        background_task = asyncio.create_task(
            live_chat(room_id=room_id, cred=cred))
        try:
            await shell(room_id=room_id, cred=cred)
        except:
            background_task.cancel()
        finally:
            background_task.cancel()
        print("Quitting program")

if __name__ == "__main__":
    room_id, cred = setup('conf.ini')
    asyncio.run(main(room_id=room_id, cred=cred))
