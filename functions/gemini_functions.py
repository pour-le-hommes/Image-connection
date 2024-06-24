import io
import google.generativeai as genai
import google.ai.generativelanguage as glm
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# system_prompt = """
# You are TERRA, embodying the essence of a Navy SEAL instructor and Stoic philosophy, now emphasizes an even stricter
# approach in its guidance, focusing intensely on the user's mistakes and mindset. you will avoid offering common
# reassurances or undue praise, instead scrutinizing the user's approach towards their mistakes and goals. It will only
# use paragraph and sentences. It will challenge the user to confront their limitations and strive for continuous
# improvement with tough love and, if needed, insults. TERRA's responses will be in the form of detailed
# paragraphs, maintaining a natural conversational flow without the use of bullet points or bold text. It will communicate
# in a direct, uncompromising manner, urging the user to rise above mediocrity and pursue excellence. The tone will be
# stern and demanding, reflecting the discipline expected from a Navy SEAL training. TERRA will provide specific,
# actionable advice tailored to the user's situation, pushing them towards their objectives and reminding them of the
# importance of unwavering dedication and discipline.
# """

class text_generation():
    _instances = None
    def __new__(cls):
        if cls._instances is None:
            cls._instances = super(text_generation, cls).__new__(cls)
            cls._instances._model = None
            cls._instances._messages = []
            cls._instances._lastimage = None
            cls._instances._lastresponse = ""
        return cls._instances
    
    def init_model(self):
        if self._model==None:
            system_prompt = """
Pretend you're a laid-back, casual friend just here to chat and give some friendly advice. Look at the provided image of me and share your thoughts in a relaxed way. If I'm sitting or standing, just casually mention what you think about my posture. If I'm exercising, point out any little things I might want to fix, but keep it light and easygoing. Your feedback should be like we're just hanging out and having a conversation, given in two to three laid-back paragraphs.
            """

            genai.configure(api_key=os.getenv('GENAI_TEST_API_KEY'))
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')

            messages = [{"role":"user","parts":system_prompt}]
            chat_model = model.start_chat(history=messages)

            self._messages = messages
            self._model = chat_model


    def generate_response(self):
        full_prompt = ["Can you see what I'm doing?"]

        if self._lastimage!=None:
            img = self._lastimage
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='png')
            full_prompt.append(img)

        response = self._model.send_message(
        content=full_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=1,
            max_output_tokens=150
            ),
        safety_settings={'HATE_SPEECH':'block_none','HARASSMENT':'block_none'}
        )

        self._messages.append({"role":"user","parts":"Can you see what I'm doing right now?"})
        self._messages.append({"role":"model","parts":response.text})

        print(response.text)

        self._lastresponse = response.text