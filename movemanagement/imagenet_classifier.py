import tensorflow as tf
from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np
import time

def load_labels(path): # Read the labels from the text file as a Python list.
    with open(path, 'r') as f:
      return [line.strip() for i, line in enumerate(f.readlines())]

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
    set_input_tensor(interpreter, image)

    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

    ordered = np.argpartition(-output, 1)
    return [(i, output[i]) for i in ordered[:top_k]][0]

IMAGE_SHAPE = (224, 224)

data_folder = "/home/pi/roboproject/TFLiteMobileNet/"

captured_image_folder = "/home/pi/roboproject/"

model_path = data_folder + "mobilenet_v1_1.0_224_quant.tflite"
label_path = data_folder + "labels_mobilenet_quant_v1_224.txt"

def classicyImage():
    interpreter = Interpreter(model_path)
    print("Model Loaded Successfully.")
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    print("Image Shape (", width, ",", height, ")")
    # Load an image to be classified.
    #grace_hopper = tf.keras.utils.get_file('image.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg')
    image_to_analyze = Image.open(captured_image_folder + 'image.jpg').resize(IMAGE_SHAPE)
    # Classify the image.
    time1 = time.time()
    label_id, prob = classify_image(interpreter, image_to_analyze)
    time2 = time.time()
    classification_time = np.round(time2-time1, 3)
    print("Classificaiton Time =", classification_time, "seconds.")
    # Read class labels.
    labels = load_labels(label_path)
    # Return the classification label of the image.
    classification_label = labels[label_id]
    classification_prob = np.round(prob*100, 2)
    print("Image Label is :", classification_label, ", with Accuracy :", classification_prob, "%.")
    return (classification_label,classification_prob)