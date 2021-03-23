from os import listdir
from os.path import isdir, join as join_path
from json import load as load_json

# file need to be moved to the backend folder for execution!!!!

counter = 0
with open('../backend/calls.txt', 'w') as f_calls:
    for dir_item in listdir('../backend/modules'):
        dir_path = join_path('../backend/modules', dir_item)
        if isdir(dir_path) and dir_item not in ['__pycache__']:
            with open(join_path(dir_path, 'metadata.json'), 'r') as f:
                metadata = load_json(f)
                for move in metadata['moves']:
                    for sentence in move["calls"]:
                        for word_num in range(len(sentence)):
                            counter = counter + 1
                            if word_num == len(sentence)-1:
                                f_calls.write(sentence[word_num])
                            else:
                                f_calls.write(sentence[word_num]+" ")
                        f_calls.write("\n")


print('complete')
print('a total of '+counter+' were saved to the calls.txt')