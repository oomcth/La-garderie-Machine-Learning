from gender_detection import predict_gender
import audio_separator
import wavfile
def get_caracters_audios(path):
  return audio_separator.count_speakers(path)
  

def get_genders_amounts(files):
  k = sum([predict_gender(file) for file in files])
  dict = {
    "M": k,
    "F": len(files) - k
  }
  
  return dict

def count_speaker(audio_path):
  try:
    return get_genders_amounts(get_caracters_audios(audio_path))
  except:
    return {
      "M": 1,
      "F":0
    }