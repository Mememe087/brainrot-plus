import stable_whisper
from google.cloud import texttospeech
import re
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./verdant-wares-411806-e3a79bc85c36.json"
# Instantiates a client
client = texttospeech.TextToSpeechClient()
model = stable_whisper.load_model('base')

def generate_audio(script, output_file = None):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=script)
    # Build the voice request, select the language code ("en-US") 
    # ****** the NAME
    # and the ssml voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-C',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MULAW)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    output_bytes = response.audio_content
    
    if output_file:
        with open(output_file, 'wb') as f:
            f.write(output_bytes)
            f.close()

    return output_bytes

def generate_audio_timestamps(input_audio, script, emphasis_words):
    
    """
    :param input_audio: bytes object of the audio
    :param script: script corresponding to the audio, without linebreaks
    :param emphasis_words: array of words that should be emphasised, all lowercase
    """

    result = model.align(input_audio, script, language='en')
    emphasis_it = 0
    durations = []
    for segment in result.segments:
        segment_info = {}
        segment_info['text'] = segment.text
        segment_info['start'] = segment.start
        segment_info['end'] = segment.end
        segment_info['words'] = []

        for i in range(len(segment.words)):
            word = {}
            word_obj = segment.words[i]
            word['word'] = word_obj.word
            word['start'] = word_obj.start - segment_info['start']
            word['end'] = word_obj.end - segment_info['start']
            word['highlighted'] = False
            if emphasis_it != len(emphasis_words):
                if re.sub('[^A-Za-z0-9]+', '', word.word).lower() == emphasis_words[emphasis_it]:
                    word['highlighted'] = True
                    emphasis_it += 1
            segment_info['words'].append(word)
            
        durations.append(segment_info)

    return durations