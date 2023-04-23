import openai
import config
from drive_api import update_personality, remember_personality, gdrive, persona

history = {}

def new_user(username):
    if(history.get(username) == None ):

        per = remember_personality(username,'Your Role')

        history[username] = [{"role": "system", "content": per}]
   

def generate_response(text, username, API_KEY = config.api_key):
    openai.api_key = API_KEY

   
    history[username].append({"role": "user", "content": f"{text}"})


    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = history[username]
        )
        
    res = response['choices'][0]['message']['content']
    tkn = response['usage']['prompt_tokens']
    if(tkn > 2000):
        del history[username][1]
    if(len(history[username])>5):
        del history[username][2], history[username][1]
    #print("Left : ", res, "\n")
    history[username].append({"role": "assistant", "content": f"{res}"})


    return res

def delete_hist(username):
    if(len(history[username])>1):
        del history[username][1:]

def delete_last(username):
    if(len(history[username])>2):
        del history[username][-2], history[username][-1]

def set_new_personality(username, new_personality):

    if(history.get(username) == None ):

        for i in persona:
            if(new_personality == i['name'] or new_personality == i['spelling']):
                history[username] = [{"role": "system", "content": f"{i['act']}"}]
                update_personality(username,f"{i['act']}")
                break
    else:

        for i in persona:
            if(new_personality == i['name'] or new_personality == i['spelling']):
                history[username][0] = {"role": "system", "content": f"{i['act']}"}
                update_personality(username,f"{i['act']}")
                break

        delete_hist(username)



