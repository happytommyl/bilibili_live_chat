import os
os.environ['NO_PROXY'] = '*'
def main():
    import chat
    import asyncio
    room_id, cred = chat.setup('conf.ini')
    asyncio.run(chat.main(room_id=room_id, cred=cred))

# def get_conf():
#     import json
#     with open(r"C:\Users\happy\AppData\Local\xfangfang\wiliwili\wiliwili_config.json") as f:
#         data = json.load(f)
    
#     cookie = data["cookie"]
#     sessdata = cookie["SESSDATA"]
#     buvid3 = cookie["buvid3"]
#     bili_jct = cookie["bili_jct"]
#     DedeUserID = cookie["DedeUserID"]
#     credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3, dedeuserid=DedeUserID)



if __name__ == "__main__":
    
    main()
