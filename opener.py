from os import listdir
from os.path import isfile, join


def get_data():

    onlyfiles = [f for f in listdir("./LibriSpeech") if isfile(join("LibriSpeech", f))]
    for id, filename in enumerate(onlyfiles):
        if filename == "SPEAKERS.TXT":
            onlyfiles = onlyfiles[0:id] + onlyfiles[id+1:len(onlyfiles)]
            break
    nfiles = len(onlyfiles)

    def get_id_from_line(i, lines):
        numbers = lines[i][0:4]
        if numbers[2] == " ":
            numbers = numbers[0:2]
        elif numbers[3] == " ":
            numbers = numbers[0:3]
        return int(numbers)

    with open('./LibriSpeech/SPEAKERS.TXT') as f:
        lines = [line.rstrip('\n') for line in f]
        n = len(lines)
        k = 0
        ids = []
        genders = []
        for name in onlyfiles[0:nfiles]:
            i = 0
            doc_id = ""
            while True:  
                caracter = name[i]
                if caracter != '-':
                    doc_id += caracter
                    i += 1
                else:
                    break
            ids.append(int(doc_id))
            for i in range(k, n):
                if get_id_from_line(i, lines):
                    genders.append(lines[i][7])
                    k = i+1
                    break
        data = [[ids[i], genders[i], "./LibriSpeech/" + onlyfiles[i]] for i in range(nfiles)]
        return data