from typing import Any
import pandas as pd
import sklearn.model_selection
from resemblyzer import VoiceEncoder, preprocess_wav
from sklearn import svm

def predict_gender(filename):

    data = None

    try:
        data = pd.read_excel("./base.xlsx")
    except:
        raise("error csv does not exit")
    
    print(data.keys)
    X = data.iloc[:, 17:]
    y = data["nb_gender_M"]
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)

    clf = svm.SVC(kernel='linear', random_state=42)
    clf.fit(X_train, y_train)

    def predict(path):
        wav = preprocess_wav(path)
        encoder = VoiceEncoder()
        embed = encoder.embed_utterance(wav)
        feature = embed.reshape(-1, 1).T
        prediction = clf.predict(feature)
        return prediction[0]

    return predict(filename)


def score(n_max: Any):
    try:
        df = pd.read_excel("./movieclips/referential_movies_subtitles_with_gender.xlsx")
        df2 = df[df["nb_characters"] == 1]
        a = []
        k = 0
        for x in df2["sound_clip_id"]:
            a.append(predict_gender("./movieclips/{x}.wav"))
            k += 1
            if(k >= n_max):
                break
        b = df2['nb_gender_M'].tolist()
        return (sum([abs(1-abs(a[i]-b[i])) for i in range(k)])/k)
    except:
        return -1
