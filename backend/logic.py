from datetime import datetime #date and time
from studyyy import current_state, study_end #checks if its a study period rn, end

def smol_text(text):
    " ".join((text or"").split()) #removes unnecessary spaces

def format_notif(body):
    info = body.split("||") #macrodroid sends notifs seperated by ||
    if len(info)==3:
        app, sender, text = (p.strip() for p in info) #assigns variables, if there 3 parts
    elif len(info) ==2:
        app = None
        sender, text = info[0].strip(), info[1].strip() #if 2 parts assumes app missing
    else:
        app =None
        sender =None
        text = body.strip()#if one part assumes its text
drafts =[]
def draft(persona): #inputs persona.text 
    start = persona.find("How the owner texts (try sound like her)")
    end = persona.find("Rules")
    style =persona[start+len("How the owner texts (try sound like her)"):end].strip()
    #style = required part from persona.txt excluding extra space
    example = persona.find("Examples of how she texts")
    examples =persona[example:].strip()
    return("You write text messages on behalf of the owner,NOT talking to owner"
           "Text in the owners style, Output ONLY THE REPLY TEXT nothing else.\n"
           "How owner writes\n"+style+"\nExamples of how she writes"+examples)
manual =None
manual_day =None
def study_active(): #checks if study mode
    global manual 
    now = datetime.now()#date and time
    if manual is not None and manual_day ==now.date():
        return manual
    return current_state(now)is not None #checks its true else false
def study_till():
    return study_end(datetime.now) or "later" #if no info found it just says later
def change_study():
    global manual, manual_day
    now = datetime.now()
    manual = not study_active(now) #if true becomes false and vice versa
    manual_day=now.date()
    return manual
recent ={}
next_id = 1
def add_notifs(app,sender,text,drafter): 
    global recent,next_id
    now = datetime.now()
    if not text:
        return "emptyyyy NEXT" #no text =ignored
    if not study_active():
        return "not study time, reply yourself :p"
    key =(sender,text)
    recent ={k: t for k,t in recent.items()
             if (now-t).total_seconds()<60} #recnt keys, notifs from past min
    if key in recent:
        return "SPAMMM"
    recent[key]=now
    draft =drafter(sender,text,study_active(now))
    draft = " ".join((draft or None).split()) #splits at blanks, joins it properly handles
    #None, formats tldr
    drafts.append({"id":next_id,"app":app,"sender":sender, "incoming":text, "draft":draft})
    next_id += 1
    return "queued"
def get_reply():
    if drafts:
        return "draft" + drafts[0]["draft"]
    if study_active:
        return "idle:study"
    return "idle"
outbox =[]
def decide(decision):
    if decision not in ("approve","reject"):
        return "check the damn code"
    if not drafts:
        return"no draft"
    draft_n = drafts.pop(0) #removes first draft from list
    if decision =="approve":
        outbox.append(draft_n)
        return "approved"
    else:
        return "rejected"
def dictate(spoken, rewriter):
    if not drafts:
        return None
    draft_n =drafts[0]
    new_draft = rewriter(draft_n["sender"],draft_n["incoming"],spoken)
    draft_n["draft"]= " ".join(new_draft.split()) #formats text
    return draft_n["draft"]
def send():
    if not outbox:
        return None
    m = outbox.pop(0) #m is first in outbox
    return m["app"]+ "||"+m["sender"]+"||"+m["draft"] #returns draft in macrodroid format









