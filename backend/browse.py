from urllib.parse import quote_plus #converts search to URL format
from playwright.sync_api import sync_playwright 

def browser(query,n =5): #returns 5 search results
    output = []
    with sync_playwright() as play: #sync playwright function, can be called as play
        browser = play.firefox.launch(headless=True) 
        #launches friefox in headless mode (not visible in bg)
        page = browser.new_page() #creates new tab
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}" 
        #searches url with query in right format
        page.goto(url,wait_until="domcontentloaded") #goes to search url
        try:
            page.locator("div.result").first.wait_for(timeout=5000)
             #locator searches for div with class result (aka links with result)
             # first() gets first result, wait waits for it to load
            for result in page.locator("div.result").all()[:n]: #loops through all results
                title = result.locator(".result_title") #finds title
                body = result.locator(".result__snippet") #finds description under title
                if not title or not body: #if no title or body, skip
                    continue
                title_t = title.inner_text() #gets text of title
                body_t = body.inner_text() #gets text of body
                link = title.locator("a").get_attribute("href") 
                #gets link from title
                output.append({"title":title_t,"body":body_t,"\nlink":link})
                return "\n".join(output) or "ERROR ERROR ERROR"
        except Exception as e:
            return f"Sumn is off: {e}"
        finally:
            browser.close() #wtv happens browser closes 
