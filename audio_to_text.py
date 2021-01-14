import speech_recognition as sr
from os import listdir, path
import difflib

r = sr.Recognizer()
samples = listdir('audio_samples')
for f in samples:
    sample = path.join('audio_samples', f)
    with sr.AudioFile(sample) as source:
        audio_text = r.record(source)
        try:
            text = r.recognize_google(audio_text, language='ko-KR')
            with open('recognize_google.txt', mode='a', encoding='utf-8') as file_object:
                print(text, file=file_object)
                print('', file=file_object)
        except Exception as e:
            print('There was a problem converting speech to text.')
            print(e)

""" Given a file name of the actual results and a file name for the expected results. Prints out the differences between the two."""
def check_diff_file(actual, expected, log=None, detailed=False):
    actual = open(actual, 'r', encoding='utf-8') 
    actual_lines = actual.readlines() 
    actual_lines = [line for line in actual_lines if line != '\n']

    expected = open(expected, 'r', encoding='utf-8')
    expected_lines = expected.readlines()
    expected_lines = [line for line in expected_lines if line != '\n']
    result = ''
    for i in range(min(len(actual_lines), len(expected_lines))):
        result += f'Line {i}:\n{actual_lines[i]} => {expected_lines[i]}\n'
        changes = check_diff(actual_lines[i], expected_lines[i])
        if detailed:
            if len(changes):
                for change in changes:
                    result += f'{change}\n'
            else:
                result += 'no differences\n'
        else:
            result += f'{len(changes)} differences\n'
        result += '\n'
    if log:
        with open('edits.txt', mode='w', encoding='utf-8') as file_object:
            print(result, file=file_object)
    else:
        print(result)

def check_diff(actual, expected):
    """ Given a string, ACTUAL, and a string, EXPECTED, return a list of the changes required to go from ACTUAL to EXPECTED."""
    deletes = []
    prev = ()
    changes = []
    i = 0
    for s in difflib.ndiff(actual, expected):
        if s[0] == ' ':
            if len(deletes):
                delete = deletes.pop(0)
                index = delete[0]
                item = delete[1][-1]
                changes.append(u'Delete "{}" from position {}'.format(item,index))
            i += 1
        elif s[0] == '-':
            deletes.append((i,s))
            i += 1
        elif s[0] == '+':
            if len(deletes):
                delete = deletes.pop(0)
                index = delete[0]
                item = delete[1][-1]
                changes.append(u'Substitute "{}" with "{}" at position {}'.format(s[-1], item, index))
            else:
                if prev:
                    changes.append(u'Add "{}" after "{}" at position {}'.format(s[-1], prev[1][-1], i-1))
                else:
                    changes.append(u'Add "{}" at the front\n'.format(s[-1]))
        prev = (i, s)
    for delete in deletes:
        index = delete[0]
        item = delete[1][-1]
        changes.append(u'Delete "{}" from position {}'.format(item,index))
    return changes

   
check_diff_file('recognize_google.txt', 'actual.txt', log='edits.txt', detailed=False)


        
