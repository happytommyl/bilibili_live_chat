def main():
    import chat
    import asyncio
    room_id, cred = chat.setup('conf.ini')
    asyncio.run(chat.main(room_id=room_id, cred=cred))



if __name__ == "__main__":
    main()
