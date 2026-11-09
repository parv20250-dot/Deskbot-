import ollama
from browse import browser
from search import search
from weather import weather_res

MODEL ="gemma4:e2b"
def web_search(query):
    return (search(query))#defines query
def browse_search(query):
    return (browser(query))#defines what to do if search
def weather_info(city): #defines weather info for a city, if no info error
    try:
        return weather_res(city)
    except Exception as e:
        return "Search failed"+ str(e) 
tools ={"web_search":web_search,
        "browse_search":browse_search,
        "weather_info":weather_info}
def pick_tools(messages):
    last_text =""
    for m in reversed(messages): #message history, latest
        if isinstance(m,dict) and m.get("role")=="user": #if dictionary and by user
            last_text =m["content"]
            break #gets latest valid user text
        if "search" in last_text.lower().split(): #if word search in input browser tool
            return[browse_search,weather_info]
        else:
            return[web_search,weather_info] 
    #if no search mentioned specifically ai only gets search tool no browser
def ask(messages, use_tools = True):
    messages =list(messages)
    if use_tools:
        tools = pick_tools(messages)
    else:
        tools = None
    for r in range(3): #can search thrice
        reply = ollama.chat(
            model=MODEL,
            messages=messages,
            think=False,
            keep_alive= "30 m",
            options={"num_ctz":4096,"num_predict":200},
            tools = tools) #confugures ollama settings, no think, kept alive 30m no reloading
        #restricts responses to 200 tockens(words)
        messages.append(reply.message)
        if not reply.message.tool_calls:
            return reply.message.content or "" #no tools request = sends reply back
        for call in reply.message.tool_calls: #loops through calls
            name=call.funvtion.name
            arguments = call.function.argumentsprint("[tool]",name,arguments, flush= True)
        tool_func = tools.get(name)
        if tool_func:
            result = tool_func(**arguments) #calls tool requested with arguments
        else:
            result ="NO TOOL, STOP HALLUCINATING"+name #no tool means error
        print("[result]",str(result)[:400],flush=True)
        messages.append({"role":"tool", "tool_name":name, "content": str(result)+
                         "\nAnswer questions from given info, DO NOT JUST send links"})
        return ("ERROR. SUMN WENT WRONG")
        


    
    