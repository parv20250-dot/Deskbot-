import os
import secrets
import tempfile
from datetime import datetime
from dotenv import load_env #contains verification code and city deets REMOVED
from fastapi import Body,Depends,FastAPI,HTTPException,Security, UploadFile
from fastapi.security import APIKeyHeader 
from fastapi.responses import PlainTextResponse #text no JSON
from faster_whisper import WhisperModel #imports audio to text thingy
from pydantic import BaseModel 
from tools import ask
from logic import (drafts,outbox,draft, smol_text, format_notif, study_active,change_study,
                   add_notifs,get_reply,decide,dictate,send)
max_messages = 5
load_dotenv() #removed for privacy
Whisper = WhisperModel("models/tiny",device ="cpu", compute_type = "int8", cpu_threads =2)

if not DESKBOT_KEY:#removed 
    print("Warning no pin set",flush=True)
api_header =APIKeyHeader(name="X-Deskbot-Key", auto_error=False)
def require_key(key:str=Security(api_header)):
   if not(key and secrets.compare_digest(key,DESKBOT_KEY)):
         raise HTTPException(status_code=401,detail="bad or missing key")
server = FastAPI(dependencies=[Depends(require_key)]) #every input must pass key check
with open("persona.txt",encoding="utf-8") as persona:
    personality = persona.read()
    draft_system = draft(personality)
    history =[]
def input():
       now = datetime.now().strftime("%A %d %B %Y, %H:%M") #date and time
       system = personality+"\n Current date and time:"+now
       system += "The user lives in"+HOME_CITY #info has been removed
       return[{"role":"system","content":system}]+ history[-max_messages:]
   #prompt and last 5
def chat_reply(text):
     history.append({"role":"user","content":text}) #user text to history
     answer = ask(input())
     history.append({"role":"assistant","content":answer}) #ai reply
     return answer
def transcribe(upload):
     file_type = os.path.splitext(upload.filename or "")[1] #find fil typ
     with tempfile.NamedTemporaryFile(delete=False,suffix= file_type) as temp_fil:
         temp_fil.write(upload.file.read())
         path = temp_fil.name
     try:
          segments,_ = Whisper.transcribe(path,beam_size =1) #transcribes using whsiper
          return " ".join(s.text.strip() for s in segments).strip() 
     #returns output from whisper and joins em tg, keeps output simplr
     finally:
          os.remove(path) #delted audio file
def draft_reply(sender,incoming,until):
     prompt = (f"Someone texted you:{incoming}\n" f"You are studying till {until}"
              "Apologise AND ALSO reply to the text")#prompt for ai
     answer =ask([{"role":"system","content":draft_system},
                  {"role":"user","content":prompt}])
      #sends the ai instructions for personality and the prompt
     answer = smol_text(answer) #formats response
     return answer or f"sry studying till{until},ttyl"
def rewrite_reply(sender,incoming,spoken):
     prompt =(f"Someone texted you:{incoming}\n"
              f" You want to reply with this idea (CHECK IT FIRST):{spoken}\n"
              "Write a reply text in the owners text tone and personality USING IDEA")
     answer = ask([{"role":"system","content":draft_system},
                   {"role":"user", "content": prompt}],use_tools =False)
     #asks model for output, no tools used
     return smol_text(answer) or spoken #returns ai answer or if no output directly
#audio to text
class ChatRequest(BaseModel):
         text:str #reuqest must have str value
         @server.get("/")
         def home(): 
              return{"status": "Deskbot server running", "messages_stored": len(history),
                    "study_mode":study_active(),"drafts_waiting": len(drafts),
                    "outbox": len(outbox),} 
         #whenever som1 at home page writes server stats
         @server.post("/chat")
         def chat(req:ChatRequest):
              return {"reply":chat_reply(req.text)} #for normal chat rq retruns reply
         @server.post("/chat_text",response_class =PlainTextResponse)
         def chat_text (text:str =Body(...,media_type="text/plain")):
              print("Recieved text:"+text,flush = True)
              return chat_reply(text)
         @server.post("/reset") #clears convo history
         def reset():
              history.clear()
              return{"status":"history cleared"}
         @server.post("/voice")
         def voice(audio:UploadFile): #voice input or uploads to server
              heard = transcribe(audio) #transcribes audio
              return {"heard":heard, "reply": chat_reply(heard)
                      if heard else""} #if heard else returns empty string
         @server.post("/voice_text",response_class=PlainTextResponse)
         def voice_text(audio:UploadFile):
              heard =transcribe(audio)
              if not heard:
                   return "huh,say that again pls"
              return smol_text(chat_reply(heard)) #if heard returns formatted, nun heard return
         @server.post("/notification", response_class=PlainTextResponse)
         def notification(body:str=Body(...,media_type="text/plain")):
             app_name, sender, text = format_notif(body)
             print( f"Notification from {sender} ({app_name}): {text}",flush=True)
             return add_notifs(app_name, sender, text, draft_reply)
         #recieves notif,extracts app sender and text, creates a draft reply
         @server.get("/phone/outbox", response_class=PlainTextResponse)
         def phone_outbox(): 
              return send() #asks for reply,reply send phone ask info from
         #phone/outbox, it gets info
         @server.get("/device/poll",response_class=PlainTextResponse)
         def device_poll():
              return get_reply() #idle when nun,idle.study if study else shows text
         @server.post("device/decision,",response_class=PlainTextResponse)
         def device_decision(body:str =Body(...,media_type ="text/plain")):
              result=decide(body) 
              return result #allows for decision to be made send by esp,checks it acts on draft
         @server.post("device/dictate",response_class= PlainTextResponse)
         def device_dictate(audio:UploadFile):
            if not drafts:
                 return PlainTextResponse("nopending draft")
            spoken=transcribe(audio)
            if not spoken:
                 return PlainTextResponse("heard nothing")
            return dictate(spoken,rewrite_reply)
         #hold B on a draft to record audio and transcribe for a new draft
         @server.post("/device/study", response_class=PlainTextResponse)
         def device_study(body:str =Body("toggle",media_type="text/plain")):
              if study_active():
                   return "on"
              else:
                   return("off") #study, button a hold allows study mode on and off