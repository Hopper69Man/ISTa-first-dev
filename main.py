#Библиотеки
import sounddevice as sd
import vosk
import json
import queue

import modules 

modules.info.mic_info()
model            = vosk.Model(modules.info.vosk_path) 
q                = queue.Queue()
answer           = ""                     #расшифрованнй запрос

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

def voice_listen():

    global names 
    global answer

    with sd.RawInputStream(callback=q_callback, channels=1, samplerate=modules.info.samplerate, device=modules.info.microphone_index, dtype='int16'):
        rec = vosk.KaldiRecognizer(model, modules.info.samplerate)
        sd.sleep(-1)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())["text"]
                if res:
                    print(f"Фраза целиком: {res}")

                    if modules.info._is_voice_input_ == True:
                        print("Передача комманды в гс управление")
                        modules.os_interaction.voice_input(res)
                        
                    if modules.info._is_name_call_ == True:
                        modules.cmd.command(res)

            else:
                res = json.loads(rec.PartialResult())["partial"]

                #if res:
                #    print(f"Поток: {res}")

                if any(word in res for word in modules.info.names):
                    if modules.info._is_name_call_ == False:
                        modules.info._is_name_call_ = True
                        print("зафиксированно обращение")
                        modules.sound.start()
                else:
                    modules.info._is_name_call_ = False

if __name__ == "__main__":
    voice_listen()