from datetime import datetime

studyhrs = {
    "monday":["17:00-20:00","21:30-22:30"],
    "tuesday":["16:00-18:00","21:00-22:00"],
    "wednesday":["15:30-18:30","20:00-22:00"],
    "thursday":["16:00-18:00", "19:30-22:30"],
    "friday":["16:00-17:00","19:00-20:00"],#chill day
    "saturday":["10:00-14:00", "16:00-19:00"],
    "sunday":["10:00-16:00"]}

def current_state(): #give it time, if no it uses current
    now = datetime.time()
    day = now.strftime("%A").lower() #gets day as lowercase string
    time = now.strftime("%H:%M") #gets time as string in hourns and mins
    for window in studyhrs.get(day,[]):
        start,end = window.split("-") #getsday seperates to start and end
        if start <= time < end: #if in study time 
            return window
        return None
def study_end():#checks if study hours ended
    now = datetime.time()
    window = current_state(now)
    if window:
        return window.split("-")[1]
    return None



