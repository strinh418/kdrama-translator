import speech_recognition as sr

r = sr.Recognizer()

with sr.AudioFile('2p_convo_1.wav') as source:
    audio_text = r.record(source)

    try:

        text = r.recognize_google(audio_text, language='ko-KR')
        print('Converting audio transcripts into text ...')
        with open('transcript.txt', mode='w', encoding='utf-8') as file_object:
            print(text, file=file_object)
    except:
        print('Sorry... run again...')
