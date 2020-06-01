from vggish_input import waveform_to_examples, wavfile_to_examples
import numpy as np
import tensorflow as tf
from keras.models import load_model
import vggish_params
from pathlib import Path
import ubicoustics
import wget
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import os
import flusense_labels as fl

###########################
# Download model, if it doesn't exist
###########################
MODEL_URL = "https://www.dropbox.com/s/cq1d7uqg0l28211/example_model.hdf5?dl=1"
MODEL_PATH = "models/example_model.hdf5"
print("=====")
print("Checking model... ")
print("=====")
model_filename = "models/example_model.hdf5"
ubicoustics_model = Path(model_filename)
if (not ubicoustics_model.is_file()):
    print("Downloading example_model.hdf5 [867MB]: ")
    wget.download(MODEL_URL, MODEL_PATH)

###########################
# Load Model
###########################
context = ubicoustics.everything
context_mapping = ubicoustics.context_mapping
trained_model = model_filename
other = True
selected_context = 'everything'

print("Using deep learning model: %s" % (trained_model))
model = load_model(trained_model)
context = context_mapping[selected_context]
graph = tf.get_default_graph()

# model.summary()

label = dict()
for k in range(len(context)):
    label[k] = context[k]

###########################
# Read Wavfile and Make Predictions
###########################

# x = wavfile_to_examples(selected_file)

rank = []

# Setup up file iteration of all segmented .wav files
for entry in os.scandir('../flusense_segmented/'):
    print("File: ", entry.path)
    # cough sample statistics
    if 'cough' in entry.path:
        try:
            x = wavfile_to_examples(entry.path)
        except ValueError as e:
            print("Error!", e, " in file", entry.path)

        row = 'cough'
        if x.shape[0] != 0:
            with graph.as_default():
                x = x.reshape(len(x), 96, 64, 1)

                # # Plot Mel Spectrum
                # melspec = np.transpose(x[1, :, :, :].reshape(96, 64))[::-1, :]
                # plt.imshow(melspec, origin='lower')
                # plt.title('Mel-spectrum of Audio Snippet with Coughs')
                # plt.xlabel('10ms Frames')
                # plt.ylabel('frequency band index')
                # plt.show()

                predictions = model.predict(x)

                for k in range(len(predictions)):
                    prediction = predictions[k]
                    rank.append(np.argsort(predictions)[0][8])
                    m = np.argmax(prediction)
                    fl.conf_mat[row][label[m]] += 1
                    print("Prediction: %s (%0.2f)" % (ubicoustics.to_human_labels[label[m]], prediction[m]))
        continue

    for i in range(1, len(fl.f_labels)):
        if fl.f_labels[i] in entry.path:
            try:
                x = wavfile_to_examples(entry.path)
            except ValueError as e:
                print("Error!", e, " in file", entry.path)

            row = fl.f_labels[i]
            if x.shape[0] != 0:

                with graph.as_default():
                    x = x.reshape(len(x), 96, 64, 1)
                    #print(np.shape(x))

                    predictions = model.predict(x)

                    for k in range(len(predictions)):
                        prediction = predictions[k]
                        m = np.argmax(prediction)
                        fl.conf_mat[row][label[m]] += 1
                        #print("Prediction: %s (%0.2f)" % (ubicoustics.to_human_labels[label[m]], prediction[m]))
            break

# Print confusion matrix & cough samples prediction rankings
print(fl.conf_mat)
print(rank)

