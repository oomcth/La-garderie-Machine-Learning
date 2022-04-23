#%%
#from sklearn import cluster
import numpy as np
from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
import matplotlib.pyplot as plt

#%%
wav_name = lambda t : "db/wav/*.wav".replace("*", t)
rttm_name = lambda t : "db/rttm/*.rttm".replace("*", t)
npy_name = lambda t : "db/npy/*.npy".replace("*", t)  

def get_array(file_name):
    """
    
    """
    wav_fpath = Path(file_name)
    wav = preprocess_wav(wav_fpath)
    encoder = VoiceEncoder("cpu")
    _, array, wav_split = encoder.embed_utterance(wav, return_partials=True, rate=16)
    return array, wav_split

#%%
from spectralcluster import SpectralClusterer
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.metrics import silhouette_score

def get_best_cluster(vectors, max_size):
    silh = []
    for k in range(2, max_size):
        kmeans = SpectralClustering(k)
        kmeans.fit(vectors)
        cluster_labels = kmeans.labels_
        

    return i + 1

def get_output_label(array):
    clusterer = SpectralClusterer(
    min_clusters=1,
    max_clusters=5,
    p_percentile=0.95,
    gaussian_blur_sigma=1)
    labels = clusterer.predict(array)
    return labels

#%%
def getextracts(label, tab):
    """
    param - label : the labelled value of the corresponding voice at each time
    param - tab : the different timestamp corresponding to the label
    return - the timestamp [start, end[ of the largest extract linked to each voice
    """
    values = [[] for _ in range(max(label) + 1)]
    start = 0
    for i, time in enumerate(tab):
        if i > 0 and label[i] != label[i-1]:
            values[label[i-1]].append(tuple([tab[start], time]))
            start = i
        if i == len(tab) - 1:
            values[label[i]].append(tuple([tab[start], time]))
    return([max(v, key=lambda t : t[1] - t[0]) for v in values])



# %%
import wavfile
def split(fichier,L):  
  #L contient les times codes où couper
  # read the file and get the sample rate and data
  data, rate, _ = wavfile.read(fichier) 
  split = 0
  noms =[]
  for i in range(len(L)):
    # get the frame to split at
    ba, bb = int(L[i][0]), int(L[i][1])
    l = (ba + bb) / 2
    split = data[max(ba, int(l - 5 * rate)):min(bb, int(l + 5 * rate))]
    wavfile.write(f"temp/{i}{fichier}",split, rate)
    noms.append(f"temp/{i}{fichier}")
  return noms
# Envoi les fonctions dans l'environnement, on les récupèrera avec nom​

#%%
def create_audio_files(filename) :
    ar, wav_split= get_array(filename)
    timestamps = [(s.start+s.stop)/2 for s in wav_split]
    labels = get_output_label(ar)
    extracts = getextracts(labels, timestamps)
    noms = split(filename, extracts)
    print(noms)
# %%
def count_speakers(audio_path):
    ar, wav_split= get_array(audio_path)
    timestamps = [(s.start+s.stop)/2 for s in wav_split]
    labels = get_output_label(ar)
    extracts = getextracts(labels, timestamps)
    noms = split(audio_path, extracts)
    print(noms)