
import sys
import numpy as np
import string

from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
from keras_self_attention import SeqSelfAttention

LAYER_COUNT = 2
HIDDEN_LAYERS_DIM = 512

FORWARDS_MODEL  = "2_layer_1/1-gpu_BS-256_2-512_dp0.20_60S_epoch03-loss1.2074-val-loss1.3678_weights"
BACKWARDS_MODEL= "2_layer_2/1-gpu_BS-256_2-512_dp0.20_60S_epoch03-loss1.3356-val-loss1.4208_weights"

#FORWARDS_MODEL = "Train 1/1-gpu_BS-512_4-512_dp0.20_60S_epoch01-loss1.6195-val-loss1.2517_weights"
#BACKWARDS_MODEL = "Train 2/1-gpu_BS-512_4-512_dp0.20_60S_epoch01-loss2.2194-val-loss1.6785_weights"

#FORWARDS_MODEL = "Attention_4_layer_train_1/1-gpu_BS-256_4-512_dp0.20_60S_epoch01-loss3.0447-val-loss3.0643_weights"
#BACKWARDS_MODEL= "Attention_4_layer_train_2/1-gpu_BS-256_4-512_dp0.20_60S_epoch01-loss3.1233-val-loss3.0936_weights"

#FORWARDS_MODEL = "6 layer train 1/1-gpu_BS-256_6-512_dp0.20_60S_epoch01-loss3.0321-val-loss3.0518_weights"
#BACKWARDS_MODEL = "6 layer train 2/1-gpu_BS-256_6-512_dp0.20_60S_epoch01-loss3.0899-val-loss3.0935_weights"


OLD_MODEL= False


ATTENTION = False
SEED = "GOOD"
reci = []
NUMBER_OF_GENS = 15

# generic vocabulary
characters = list(string.printable)
characters.remove('\x0b')
characters.remove('\x0c')

VOCABULARY_SIZE = len(characters)
characters_to_ix = {c:i for i,c in enumerate(characters)}

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
    if (i != (LAYER_COUNT - 1) and ATTENTION):
        test_backwards.add(SeqSelfAttention(attention_activation='sigmoid'))
    test_forewards.add(
        LSTM(
            HIDDEN_LAYERS_DIM,
            return_sequences=True if (i != (LAYER_COUNT - 1)) else False,
            batch_input_shape=(1, 1, VOCABULARY_SIZE),
            stateful=True
        )
    )
    if (i != (LAYER_COUNT - 1) and ATTENTION):
        test_forewards.add(SeqSelfAttention(attention_activation='sigmoid'))

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

def to_text(text):
    noviText =[]
#    text.
    for i in range(len(text)):
        if (text[i] == "\n"):
            noviText.append(' ')
            break
        else :
            noviText.append(text[i])

    return noviText

def print_text(text):
    for i in range(len(text)):
        sys.stdout.write(text[i])


def combine_text_new(backwards_model, forewards_model, seed="HELLO WORLD", count=200):
    seed += " "
    seed = seed[::-1]
    seed = seed.upper()

    backwards = generate_text(backwards_model, seed, count)
    backwards = to_text(backwards)

    #print("BACKWARDS : ")

    #print(backwards)

    backwards.reverse()

    seed = seed[::-1]
    backwards.append(" ")
    for i in range(len(seed)):
        backwards.append(seed[i])

    newSeed = ''.join(backwards)
    newSeed.strip()
    newSeed += " "
    #print("NEW SEED IS : " + newSeed)

    reci.clear()


    # print("\nSLEDECI DEO \n")

    forewards = generate_text(forewards_model, newSeed, count)

    #print(forewards)
    # forewards = to_text(forewards)

    newString = ''.join(forewards)
    #print(newString)

    print_text(newSeed + newString)

    reci.clear()


def combine_text(backwards_model, forewards_model, seed="HELLO WORLD", count=200):
    seed+=" "
    seed = seed.upper()

    forewards = generate_text(forewards_model, seed, count)
    forewards = to_text(forewards)

    secondText = seed+ " " + ''.join(forewards)
    secondText+=" "


  #  print("Forewards je : " + secondText)


    forewards.reverse()

    #seed = seed[::-1]
    newSeed = secondText[::-1]
    newSeed.strip()
   # print("New seed je : " + newSeed)

    reci.clear()

    backwards = generate_text(backwards_model, newSeed, count)

  #  print("BACKWARDS : ")
  #  print(backwards)

    backwards.reverse()


    backwards = to_text(backwards)
    firstText = ''.join(backwards)

   # print("First text je : " + firstText)

    #print("PRVO GENERISANO : \n")
    #print(secondText)
    #print("DRUGO GENERISANO : \n")
    #print(firstText)
    #print("NIZ : \n")
    #print(backwards)
    print(firstText + secondText)


    reci.clear()

def generate_text(model, seed="I am", count=140):
    """Generate characters from a given seed"""
    model.reset_states()
   # print("\n U GENERATE TEXT, SEED JE : \n")
   # print(seed)
    for s in seed[:-1]:
        next_char = predict_next_char(model, s)
    current_char = seed[-1]


    for i in range(count - len(seed)):
        next_char = predict_next_char(model, current_char, diversity=0.5)
        current_char = next_char
        reci.append(next_char)

    return reci


#print("Unesite vrednost :")

seeds = [

"Generating",
"Teaching",
"Meme",
"Science",
"Computer",
"Love",
"Life",
"Sad",
"play games",
"school is boring"

]

#SEED = input()


for s in seeds :
    SEED = s
    for i in range(NUMBER_OF_GENS):
        print("\nNova iteracija :\n")
        if(OLD_MODEL) :
            combine_text(
                test_backwards,
                test_forewards,
                seed=SEED
            )
        else :
            combine_text_new(
                test_backwards,
                test_forewards,
                seed=SEED
            )