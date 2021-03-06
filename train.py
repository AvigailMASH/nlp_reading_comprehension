import numpy as np
import matplotlib.pyplot as plt 
import os 
from os import path

if not path.exists('/content/drive/MyDrive/nlp/Saved_model'):
    Save_model = '/content/drive/MyDrive/nlp/Saved_model'
    os.mkdir(Save_model)

from keras import backend as K

from process_data import load_data, build_dict, vectorize, load_glove_weights
from net import Net

N = 30000
N_d = int(N * 0.1)
train_d, train_q, train_a = load_data('/content/drive/MyDrive/nlp/training3.txt', N, True)
dev_d, dev_q, dev_a = load_data('/content/drive/MyDrive/nlp/validation.txt', N_d, True)

num_train = len(train_d)
num_dev = len(dev_d)
print('n_train', num_train, ', num_dev', num_dev)

print('Build dictionary..')
word_dict = build_dict(train_d + train_q)
entity_markers = list(set([w for w in word_dict.keys()
                              if w.startswith('@entity')] + train_a))
entity_markers = ['<unk_entity>'] + entity_markers
entity_dict = {w: index for (index, w) in enumerate(entity_markers)}
print('Entity markers: %d' % len(entity_dict))
num_labels = len(entity_dict)

doc_maxlen = max(map(len, (d for d in train_d)))
query_maxlen = max(map(len, (q for q in train_q)))
print('doc_maxlen:', doc_maxlen, ', q_maxlen:', query_maxlen)

v_train_d, v_train_q, v_train_y, _ = vectorize(train_d, train_q, train_a, word_dict, entity_dict, doc_maxlen, query_maxlen)
v_dev_d, v_dev_q, v_dev_y, _       = vectorize(dev_d, dev_q, dev_a, word_dict, entity_dict, doc_maxlen, query_maxlen)
print('vectroized shape')
print(v_train_d.shape, v_train_q.shape, v_train_y.shape)
print(v_dev_d.shape, v_dev_q.shape, v_dev_y.shape)

vocab_size = max(word_dict.values()) + 1 
print('vocab_size:', vocab_size)
embd_size = 100
rnn_half_hidden_size = 64
glove_embd_w = load_glove_weights('/content/drive/MyDrive/nlp/glove.6B/', 100, vocab_size, word_dict)
model = Net(vocab_size, embd_size, rnn_half_hidden_size, glove_embd_w, doc_maxlen, query_maxlen, len(entity_dict))
print(model.summary())
history = model.fit([v_train_d, v_train_q], v_train_y,
            batch_size=32,
            epochs=15,
            validation_data=([v_dev_d, v_dev_q], v_dev_y)
        )

#print(history.history.keys())

train_loss = history.history['loss']
val_loss = history.history['val_loss']

train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

#print(train_loss)


fig = plt.figure()
plt.plot(train_loss)
plt.plot(val_loss)
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
save_fig_name = '/content/drive/MyDrive/nlp/Saved_model/figure_loss.png'
fig.savefig(save_fig_name)

fig = plt.figure()
plt.plot(train_acc)
plt.plot(val_acc)
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
save_fig_name = '/content/drive/MyDrive/nlp/Saved_model/figure_acc.png'
fig.savefig(save_fig_name)
