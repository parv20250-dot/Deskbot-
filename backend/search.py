from ddgs import DDGS 

def search (query,n =5): #first five results
    searchy = DDGS()
    results = ddgs.text(query,max_results =n)#text search using query no of results
    output =[]
    for r in results:
        output.append(r["title"]+":"+r["body"])#adds search result to list
    return "\n".join(output) #joins list terms tg

