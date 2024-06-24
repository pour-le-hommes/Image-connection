import pyttsx3

class tts():
    _instances = None

    def __new__(cls):
        if cls._instances==None:
            cls._instances = super(tts, cls).__new__(cls)
            cls._instances._model = None
            cls._instances._finished = True

        return cls._instances
    
    def init_model(self):
        if self._model==None:
            engine = pyttsx3.init()

            engine.setProperty('rate', 170)

            self._model = engine

    def tts(self, prompt:str):
        self._finished = False
        engine = self._model
        engine.say(prompt)
        engine.runAndWait()
        self._finished = True


# tts_model = tts()

# tts_model.init_model()

# tts_model.tts(prompt="Hello how are you")

# print("testing")