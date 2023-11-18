from config.config import SBER_API_KEY

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

MODEL = "gpt-3.5-turbo-1106"
MAX_SYMBOLS = 15000


system_prompt = '''Твоя задача выделить главную информацию из записи совещания. 
            Эта информация должна быть удобным сокращением текста, который содержится в тройных кавычках.
            Выдели несколько главных тезисов, которые обсуждались и перечисли их.
            Постарайся сохранить важные детали.'''

class Summarizer():
    def __init__(self, combined_text):
        self.texts = [text for (text, speaker) in combined_text]
        self.speakers = [speaker for (text, speaker) in combined_text]
        self.chat = GigaChat(credentials=SBER_API_KEY, verify_ssl_certs=False)        

    def summarize(self):
        # change later !!!
        summaries = self.get_summary()
        summary = ''
        for i, part in enumerate(summaries):
            summary += part + '\n'
        return summary

    def get_summary(self):
        texts = self.prepare_texts()
        result = []

        for text in texts:
            prompt = text
            try:
                response = self.get_completion(prompt)
            except:
                response = self.get_completion(prompt)
            result.append(response)
        return result

    def prepare_texts(self):
        curr_size = 0
        curr_text = ''
        text = []
        last_speaker = self.speakers[0]

        for i, line in enumerate(self.texts):
            line = '\n' + last_speaker + ': ' + line
            if len(line) + curr_size < MAX_SYMBOLS:
                curr_text += line
                curr_size += len(line)
            else:
                text.append(curr_text)
                curr_text = line
                curr_size = len(line)
        text.append(curr_text)
        return text

    def get_completion(self, prompt, model=MODEL):
        messages = [SystemMessage(content=system_prompt)]
        messages.append(HumanMessage(content=prompt))
        
        response = self.chat(messages)
        return response.content