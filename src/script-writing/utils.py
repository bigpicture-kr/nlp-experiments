import re

def normalization(text):
    text = re.sub('[●○]', '', text)
    text = re.sub('!+', '!', text)
    text = re.sub('\?+', '?', text)
    text = re.sub('(\?!|!\?)+', '?!', text)
    text = re.sub('\.\.\.\.+', '...', text)
    return text
