import asyncio

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from bilibili_api import live, Credential, Danmaku
import configparser


def load_conf(path):
    conf = configparser.ConfigParser(interpolation=None)
    conf.read(path)
    return conf


def load_cred(configParser):
    cred = configParser.items("Credential")
    SESSDATA, buvid3, bili_jct = [i[1] for i in cred]
    cred = Credential(sessdata=SESSDATA, bili_jct=bili_jct, buvid3=buvid3)
    return cred


def load_room(configParser):
    room = configParser.items("Room")
    return int(room[0][1])


def setup(path):
    config = load_conf(path)
    cred = load_cred(config)
    room_id = load_room(config)
    
    return [room_id, cred]


async def live_chat(room_id, cred):
    danmaku = live.LiveDanmaku(room_id, credential=cred)

    @danmaku.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕
        print(f"{event['data']['info'][2][1]}: {event['data']['info'][1]}")

    try:
        await danmaku.connect()
    except asyncio.CancelledError:
        print("Background task cancelled.")


async def shell(room_id, cred):
    session = PromptSession(">>> ")
    room = live.LiveRoom(room_id, credential=cred)
    while True:
        try:
            result = await session.prompt_async()
            if result != "":
                await room.send_danmaku(Danmaku(result))
        except (EOFError, KeyboardInterrupt):
            return


async def main():
    room_id, cred = setup('conf.ini')
    with patch_stdout():
        background_task = asyncio.create_task(
            live_chat(room_id=room_id, cred=cred))
        try:
            await shell(room_id=room_id, cred=cred)
        finally:
            background_task.cancel()
        print("Quitting program")

if __name__ == "__main__":
    try:
        from asyncio import run
    except ImportError:
        asyncio.run_until_complete(main())
    else:
        asyncio.run(main())
