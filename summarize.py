from pypdf import PdfReader
import asyncio
import re
import time
from EdgeGPT import Chatbot, ConversationStyle

conversationLimit = 5
conversationTimes = 0

pattern = r"\[\^\d\^\]"
initial_prompt = "Given the following text prompts, generate a summary of the text. The proceeding prompts will be a Management discussion and analysis for a given company."

async def handlePrompt(bot: Chatbot, prompt: str):
    global conversationTimes
    if conversationTimes >= conversationLimit:
        # reset conversation times
        conversationTimes = 1
        # reset conversation
        resp = await bot.reset()
        time.sleep(5)
    if conversationTimes == 0:
        # initial prompt
        resp = await bot.ask(initial_prompt, conversation_style=ConversationStyle.precise)
        conversationTimes += 1
        time.sleep(5)

    
    resp = await bot.ask(prompt, conversation_style=ConversationStyle.precise)
    time.sleep(5)
    errorMessage = resp.get("item", {}).get("result", {}).get("error")
    if errorMessage != None:
        raise Exception(resp.get("item", {}).get("result", {}).get("error"))
        return ""
    print(resp)
    raw_message = ""
    # find text equal to prompt, then grab the next message then return the text of that message
    for i, message in enumerate(resp.get("item", {}).get("messages", [])):
        if message.get("text", "") == prompt:
            raw_resp = resp.get("item", {}).get("messages", [])
            try:
                raw_message = raw_resp[i+1].get("text", "")
            except:
                # grab latest message
                raw_message = raw_resp[-1].get("text", "")
                if raw_message == "":
                    return ""
                # no message after prompt
                return ""
            break
    # clean message
    clean_message = re.sub(pattern, "", raw_message)
    return clean_message

async def main():

    bot = Chatbot(cookiePath='./cookies.json')
    # Open the PDF file in read-binary mode
    with open('docs/BRAG/q2Mda2022.pdf', 'rb') as pdf_file:
        
        # Create a PDF reader object
        pdf_reader = PdfReader(pdf_file)

        # Get the number of pages in the PDF file
        num_pages = len(pdf_reader.pages)

        # Loop through the pages in the PDF file
        for page_num in range(2, num_pages):

            # Skip the first two pages
            pdf_page = pdf_reader.pages[page_num]

            # Extract the text from the PDF page
            page_text = pdf_page.extract_text()

            # page text in 1950 chunks
            for i in range(0, len(page_text), 1950):
                # get the first 1900 characters of the text
                summarization_text = page_text[i:i+1950]

                clean_message = await handlePrompt(bot, summarization_text)

                print(clean_message)
                print("\n\n")
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())