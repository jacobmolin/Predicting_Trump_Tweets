# Learn from a part of the data set (or a specific year) and predict a Trump tweet

from cleanup import cleanup
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils

data = pd.read_csv('data/tweets_11-06-2020.csv')
# print(data.head(10), '\n')

user_year = '2016'
df = data[(data["date"] >= user_year + '-01-01 00:00:00') &
          (data["date"] <= user_year + '-12-31 23:59:59')]

# print('len(df):')
print('length df:', len(df))

text = cleanup(df)
# print(text)
# print(len(text.split(' ')))

# Creating word mapping
words = text.split()
words = sorted(list(set(words)))
# print('unique words:', len(words))
# print(words)

# maps words to numbers
n_to_word = {n: word for n, word in enumerate(words)}
word_to_n = {word: n for n, word in enumerate(words)}

# print('n_to_word: ', n_to_word)
# print('word_to_n: ', word_to_n)

# #Data pre-processing
X_train = []
Y_target = []
text_list = text.split()
length = len(text_list)
# print(text.split())
print('length text:', length)
seq_length = 10


for i in range(0, length-seq_length, 1):
    sequence = text_list[i:i + seq_length]
    label = text_list[i + seq_length]
    X_train.append([word_to_n[word] for word in sequence])
    Y_target.append(word_to_n[label])


# print(X_train)
print('len(X_train):', len(X_train))

# We need to transform the array Y into a one-hot encoded format.
X_modified = np.reshape(X_train, (len(X_train), seq_length, 1))
X_modified = X_modified / float(len(words))
Y_modified = np_utils.to_categorical(Y_target)

# print('X_modified:', X_modified)
# print('Y_modified:', np.amax(Y_modified[0]))

import tensorflow as tf
config = tf.compat.v1.ConfigProto(gpu_options = 
                         tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
# device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)


model = Sequential()

model.add(LSTM(400, input_shape=(
    X_modified.shape[1], X_modified.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(400, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(400))
model.add(Dropout(0.2))
model.add(Dense(Y_modified.shape[1], activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(X_modified, Y_modified, epochs=1, batch_size=50)

model.save_weights('models/text_generator_400_0.2_400_0.2_400_0.2_100_1.h5')

model.load_weights('models/text_generator_400_0.2_400_0.2_400_0.2_100_1.h5')


# string_mapped = X_train[99]
# full_string = [n_to_char[value] for value in string_mapped]
# # generating characters
# for i in range(400):
#     x = np.reshape(string_mapped, (1, len(string_mapped), 1))
#     x = x / float(len(characters))

#     pred_index = np.argmax(model.predict(x, verbose=0))
#     seq = [n_to_char[value] for value in string_mapped]
#     full_string.append(n_to_char[pred_index])

#     string_mapped.append(pred_index)
#     string_mapped = string_mapped[1:len(string_mapped)]
#     # combining text
# txt = ""
# for char in full_string:
#     txt = txt+char
# txt


# print(words)
# print('len words:', len(words))


# # Summarize months, user_month is chosen by user.
# user_month = 1
# # timeInterval = 1 / user_month
# monthText = [user_month]

# # for i in range(user_month):
# #     if i < 10:
# #         df = data[(data["date"] >= user_year + '-0' + i + '-01 00:00:00') & (data["date"] <= user_year + '-0' + i + '-30 23:59:59')]

# #     else:
# #         df = data[(data["date"] >= user_year + '-' + i + '-01 00:00:00') & (data["date"] <= user_year +  '-' + i + '-30 23:59:59')]

# #     monthText[i] = ''.join(df["text"])
# #     monthText[i] = monthText[i].lower()

# # characters = sorted(list(set(text)))
# # n_to_char = {n:char for n, char in enumerate(characters)}
# # char_to_n = {char:n for n, char in enumerate(characters)}

# # #Data pre-processing
# X = []
# Y = []
# length = len(text)
# seq_length = 100

# for i in range(0, length-seq_length, 1):
#     sequence = text[i:i + seq_length]
#     label = text[i + seq_length]
#     X.append([char_to_n[char] for char in sequence])
#     Y.append(char_to_n[label])

# X_modified = np.reshape(X, (len(X), seq_length, 1))
# X_modified = X_modified / float(len(characters))
# Y_modified = np_utils.to_categorical(Y)


# # #A deeper model
# model = Sequential()
# model.add(LSTM(400, input_shape=(
#     X_modified.shape[1], X_modified.shape[2]), return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(400, return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(400))
# model.add(Dropout(0.2))
# model.add(Dense(Y_modified.shape[1], activation='softmax'))

# model.compile(loss='categorical_crossentropy', optimizer='adam')

# # Train model
# # model.fit(X_modified, Y_modified, epochs=10, batch_size=10)
# # model.save_weights('text_generator_400_0.2_400_0.2_400_0.2_100.h5')

# model.load_weights('/text_generator_400_0.2_400_0.2_400_0.2_100.h5')


# # Generating text
# string_mapped = X[99]
# full_string = [n_to_char[value] for value in string_mapped]
# # generating characters
# for i in range(400):
#     x = np.reshape(string_mapped, (1, len(string_mapped), 1))
#     x = x / float(len(characters))

#     pred_index = np.argmax(model.predict(x, verbose=0))
#     seq = [n_to_char[value] for value in string_mapped]
#     full_string.append(n_to_char[pred_index])

#     string_mapped.append(pred_index)
#     string_mapped = string_mapped[1:len(string_mapped)]


# # Combining text
# txt = ""
# for char in full_string:
#     txt = txt+char
# print(txt)
