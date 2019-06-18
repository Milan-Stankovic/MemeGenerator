
import sys
import numpy as np
import string

from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation

LAYER_COUNT = 4
HIDDEN_LAYERS_DIM = 512
BACKWARDS_MODEL = "train1.w"
FORWARDS_MODEL = "train2.w"

SEED = " SUNDAY"
reci = []

# generic vocabulary
characters = list(string.printable)
characters.remove('\x0b')
characters.remove('\x0c')

VOCABULARY_SIZE = len(characters)
characters_to_ix = {c:i for i,c in enumerate(characters)}
print("vocabulary len = %d" % VOCABULARY_SIZE)
print(characters)

test_backwards = Sequential()
test_forewards = Sequential()
for i in range(LAYER_COUNT):
    test_backwards.add(
            LSTM(
                HIDDEN_LAYERS_DIM,
                return_sequences=True if (i!=(LAYER_COUNT-1)) else False,
                batch_input_shape=(1, 1, VOCABULARY_SIZE),
                stateful=True
            )
        )
    test_forewards.add(
        LSTM(
            HIDDEN_LAYERS_DIM,
            return_sequences=True if (i != (LAYER_COUNT - 1)) else False,
            batch_input_shape=(1, 1, VOCABULARY_SIZE),
            stateful=True
        )
    )
test_backwards.add(Dense(VOCABULARY_SIZE))
test_backwards.add(Activation('softmax'))
test_backwards.compile(loss='categorical_crossentropy', optimizer="adam")

test_backwards.load_weights(
    BACKWARDS_MODEL
)

test_forewards.add(Dense(VOCABULARY_SIZE))
test_forewards.add(Activation('softmax'))
test_forewards.compile(loss='categorical_crossentropy', optimizer="adam")

test_forewards.load_weights(
    FORWARDS_MODEL
)


def sample(preds, temperature=1.0):
    """Helper function to sample an index from a probability array"""
    # from fchollet/keras
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def predict_next_char(model, current_char, diversity=1.0):
    """Predict the next character from the current one"""
    x = np.zeros((1, 1, VOCABULARY_SIZE))
    x[:, :, characters_to_ix[current_char]] = 1
    y = model.predict(x, batch_size=1)
    next_char_ix = sample(y[0, :], temperature=diversity)
    next_char = characters[next_char_ix]
    return next_char

def combine_text(backwards_model, forewards_model, seed="I am", count=140):
    backwards = generate_text(backwards_model, seed, count)

    backwards.reverse()
    reci.clear()

    forewards = generate_text(forewards_model, seed, count)

    reci.clear()

def generate_text(model, seed="I am", count=140):
    """Generate characters from a given seed"""
    model.reset_states()
    for s in seed[:-1]:
        next_char = predict_next_char(model, s)
    current_char = seed[-1]

    #sys.stdout.write(seed[::-1])

    sys.stdout.write(seed)

    for i in range(count - len(seed)):
        next_char = predict_next_char(model, current_char, diversity=0.5)
        current_char = next_char
        reci.append(next_char)
        #sys.stdout.write(next_char)
    #reci.reverse()

    return reci
    #for i in range(len(reci)):
     #   sys.stdout.write(reci[i])
      #  if(reci[i]=="\n") :
       #     break

    #reci.clear()


for i in range(5):
    print("\nNOVI : \n")
    combine_text(
        test_backwards,
        test_forewards,
        seed=SEED
    )