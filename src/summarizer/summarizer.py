import openai

MODEL = "gpt-3.5-turbo-1106"
MAX_SYMBOLS = 15000

openai.api_key = API_KEY


class Summarizer():
    def __init__(self, combined_text):
        self.texts = combined_text[:][0]
        self.speakers = combined_text[:][1]

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
            prompt = f"""
            Твоя задача выделить главную информацию из записи совещания. 
            Эта информация должна быть удобным сокращением текста, который содержится в тройных кавычках.
            Выдели несколько главных тезисов, которые обсуждались и перечисли их.
            Постарайся сохранить важные детали.
            Текст: ```{text}```
            """
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
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            # temperature =
        )
        return response.choices[0].message["content"]
