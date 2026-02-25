import os
import asyncio
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

session_name = 'auto_session'

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    
    print("جاري الاتصال...")
    await client.connect()
    
    if not await client.is_user_authorized():
        print(f"إرسال كود لـ {phone}")
        await client.send_code_request(phone)
        code = input("أدخل الكود اللي وصلك: ")
        try:
            await client.sign_in(phone, code)
            print("تم تسجيل الدخول بنجاح!")
        except SessionPasswordNeededError:
            password = input("أدخل كلمة السر (2FA): ")
            await client.sign_in(password=password)
            print("تم مع 2FA!")
        except Exception as e:
            print("خطأ في التسجيل:", str(e))
            return
    else:
        print("متصل مسبقاً.")
    
    me = await client.get_me()
    print(f"مرحبا {me.first_name}! يوزر: @{me.username or 'لا يوجد'}")

asyncio.run(main())
