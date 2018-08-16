# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os, sys, datetime, shutil

import numpy as np
import tensorflow as tf


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(
            file_reader, channels=3, name="png_reader")
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(
            tf.image.decode_gif(file_reader, name="gif_reader"))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
    else:
        image_reader = tf.image.decode_jpeg(
            file_reader, channels=3, name="jpeg_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)

    return result


def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label


if __name__ == "__main__":
    file_name = "tensorflow/examples/label_image/data/grace_hopper.jpg"
    model_file = \
        "tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb"
    label_file = "tensorflow/examples/label_image/data/imagenet_slim_labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = "input"
    output_layer = "InceptionV3/Predictions/Reshape_1"

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    parser.add_argument("--graph", help="graph/model to be executed")
    parser.add_argument("--labels", help="name of file containing labels")
    parser.add_argument("--input_height", type=int, help="input height")
    parser.add_argument("--input_width", type=int, help="input width")
    parser.add_argument("--input_mean", type=int, help="input mean")
    parser.add_argument("--input_std", type=int, help="input std")
    parser.add_argument("--input_layer", help="name of input layer")
    parser.add_argument("--output_layer", help="name of output layer")
    args = parser.parse_args()

    model_file = "../retrained_graph.pb"
    # need to loop through the files in the directory
    # file_name = args.image
    label_file = "../retrained_labels.txt"
    input_layer = "Placeholder"
    output_layer = "final_result"

    # python label_image.py \
    # --graph = / tmp / output_graph.pb
    # --labels = / tmp / output_labels.txt \
    # --input_layer = Placeholder \
    # --output_layer = final_result \
    # --input_height = 224
    # --input_width = 224 \
    # --image =$HOME / flower_photos / daisy / 21652746_cc379e0eea_m.jpg

log = open("ML_log.txt", "w+")

log.writelines("started processing at " + str(datetime.datetime.now()) + "\r\n")

print("started processing at " + str(datetime.datetime.now()) + "\r\n")

files_processed = 0

# load the model file
graph = load_graph(model_file)

print(os.getcwd())

os.chdir('../ML-Processing')

for f in os.listdir(os.getcwd()):

    print("into for files_processed")

    file_name, file_ext = os.path.splitext(f)
    # print(file_name)

    full_file_name = file_name + file_ext

    print(" the first letter of the file is " + file_name[0:1])
    # 2018-06-21-18-14-19-01-13_maybe_ball in frame=0.516
    # need to check the file starts with 2 (as in the timestamp) and is a .jpg
    if file_ext == '.jpg' and file_name[0:1] == '2':
        # print("into if statement")

        log.writelines("Processing file number " + str(files_processed) + "\r\n")
        log.writelines(full_file_name + "\r\n")
        log.writelines("Actually processing this file" + "\r\n")
        # load move file was here.

        t = read_tensor_from_image_file(
            full_file_name,
            input_height=input_height,
            input_width=input_width,
            input_mean=input_mean,
            input_std=input_std)

        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name)
        output_operation = graph.get_operation_by_name(output_name)

        with tf.Session(graph=graph) as sess:
            results = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: t
            })
        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]
        labels = load_labels(label_file)
        loop = 0
        for i in top_k:
            print(labels[i], results[i])
            # print(str(i))
            # print(str(len(top_k)))

            log.write(str(labels[i]) + "_" + str(results[i]) + "\r\n")

            if loop == 0:
                # the first loop contains the higest likelihood classification

                if results[i] >= 0.8:
                    # we should only classify things that we think are more than 50% meant to be something
                    # rename the file
                    os.rename(f, file_name + "_" + str(labels[i])[0:10] + "=" + str(results[i])[0:5] + file_ext)
                    loop += 1
                else:
                    os.rename(f, file_name + "_maybe_" + str(labels[i]) + "=" + str(results[i])[0:5] + file_ext)
                    loop += 1

        files_processed += 1

        log.writelines("finshed processing at " + str(datetime.datetime.now()) + "\r\n")

        log.writelines("about to copy file to processed folder \r\n")

        shutil.move(f, "./ML-Processed")

        log.writelines("file should be moved now \r\n")

        # log.writelines("finshed run at _" + str(datetime.datetime.now()))

        #added comment
