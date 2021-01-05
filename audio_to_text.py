import speech_recognition as sr
from os import listdir, path

r = sr.Recognizer()
samples = listdir('audio_samples')
try:
    with open('recognize_google.txt', mode='w') as file_object:
        print('', file=file_object)
except:
    print('There was a problem clearing the file.')
for f in samples:
    sample = path.join('audio_samples', f)
    with sr.AudioFile(sample) as source:
        audio_text = r.record(source)
        try:
            text = r.recognize_google(audio_text, language='ko-KR')
            with open('recognize_google.txt', mode='a', encoding='utf-8') as file_object:
                print(text, file=file_object)
                print('', file=file_object)
        except:
            print('There was a problem converting speech to text.')

""" Checks for differences in character, disregarding differences in whitespace. """
def check_diff_string(actual, expected):
    actual = actual.replace(' ', '')
    expected = expected.replace(' ', '')
    min_len = min(len(actual), len(expected))
    differences = 0
    for i in range(min_len):
        if actual[i] != expected[i]:
            differences += 1
    return differences




""" Given a file name of the actual results and a file name for the expected results. Prints out the differences between the two."""
def check_diff(actual, expected, log=None):
    actual = open(actual, 'r', encoding='utf-8') 
    actual_lines = actual.readlines() 

    expected = open(expected, 'r', encoding='utf-8')
    expected_lines = expected.readlines()
    result = ""
    min_len = min(len(actual_lines), len(expected_lines))
    for i in range(min_len):
        result += f'Differences on line {i+1}: {check_diff_string(actual_lines[i], expected_lines[i])}\n'
    if log:
        with open(log, mode='w') as file_object:
            print(result, file=file_object)
    else:
        print(result)

check_diff('recognize_google.txt', 'actual.txt')
            



        
