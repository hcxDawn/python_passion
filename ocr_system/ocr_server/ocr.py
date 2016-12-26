import numpy as np
import math
import json
import os
import sys


class OCRHandle:
    theta1 = []
    theta2 = []
    hidden_layer_bias = []
    output_layer_bias = []
    NUM_HIDDEN_NODES = 15
    LEARNING_RATE = 0.1
    PARA_FILE_PATH = "ANNPara.json"

    def __init__(self):
        print("OCRHandle init")
        if os.path.isfile(self.PARA_FILE_PATH):
            print("load para form file")
            self.get_para()
        else:
            print("set random para")
            self.theta1 = self._rand_initialize_weights(400, self.NUM_HIDDEN_NODES)
            self.theta2 = self._rand_initialize_weights(self.NUM_HIDDEN_NODES, 10)
            self.hidden_layer_bias = self._rand_initialize_weights(1, self.NUM_HIDDEN_NODES)
            self.output_layer_bias = self._rand_initialize_weights(1, 10)

    @staticmethod
    def get_cur_info(self):
        print(sys._getframe().f_code.co_filename)
        print(sys._getframe().f_code.co_name)
        print(sys._getframe().f_lineno)

    @staticmethod
    def _rand_initialize_weights(size_in, size_out):
        return [((x * 0.12) - 0.06) for x in np.random.rand(size_out, size_in)]

    @staticmethod
    def sigmoid_array(value):
        for i in range(len(value)):
            value[i] = OCRHandle.sigmoid(value[i])
        return value

    @staticmethod
    def sigmoid(val):
        return 1/(1 + math.e ** -float(val))

    def sigmoid_prime(self, value):
        for i in range(0, len(value)):
            value[i] = self.sigmoid(value[i]) * (1 - self.sigmoid(value[i]))
        return value

    def artificial_neural_network_train(self, train_data, is_train):
        y0 = train_data["data"]
        digit = train_data["label"]

        y1 = np.dot(np.mat(self.theta1), np.mat(y0).T)
        sum1 = np.add(y1, np.array(self.hidden_layer_bias))
        y1 = OCRHandle.sigmoid_array(sum1)
        print("y1 shape", end=" ")
        print(y1.shape)

        y2 = np.dot(np.mat(self.theta2), y1)
        sum2 = np.add(y2, np.array(self.output_layer_bias))
        y2 = OCRHandle.sigmoid_array(sum2)
        print("y2 shape", end=" ")
        print(y2.shape)

        if not is_train:
            output_vector = y2.T.tolist()[0]
            print(output_vector)
            predict_digit = output_vector.index(max(output_vector))
            print("predict_digit : ", end="")
            print(predict_digit)
            return predict_digit

        output_correct = [0]*10
        output_correct[digit] = 1
        output_errors = np.mat(output_correct).T - y2
        print("output_error", end=" ")
        print(output_errors.shape)
        hidden_errors = np.multiply(np.dot(np.mat(self.theta2).T, output_errors), self.sigmoid_prime(sum1))
        print("hidden_errors", end=" ")
        print(hidden_errors.shape)

        self.theta1 += self.LEARNING_RATE * np.dot(np.mat(hidden_errors), np.mat(y0))
        self.theta2 += self.LEARNING_RATE * np.dot(np.mat(output_errors), np.mat(y1).T)
        self.hidden_layer_bias += self.LEARNING_RATE * hidden_errors
        self.output_layer_bias += self.LEARNING_RATE * output_errors
        print("hidden bias", end="")
        print(self.hidden_layer_bias.shape)
        print("output bias", end="")
        print(self.output_layer_bias.shape)
        self.save_para()

    def save_para(self):
        para_json = {
            "theta1": self.theta1.tolist(),
            "theta2": self.theta2.tolist(),
            "hidden_layer_bias": self.hidden_layer_bias.tolist(),
            "output_layer_bias": self.output_layer_bias.tolist()
        }
        with open(self.PARA_FILE_PATH, "w") as f:
            json.dump(para_json, f)

    def get_para(self):
        with open(self.PARA_FILE_PATH, "r") as f:
            para_json = json.load(f)
        self.theta1 = para_json["theta1"]
        self.theta2 = para_json["theta2"]
        self.hidden_layer_bias = para_json["hidden_layer_bias"]
        self.output_layer_bias = para_json["output_layer_bias"]

if __name__ == "__main__":
    test_data = {
        "data": [0]*400,
        "label": 0
    }
    ocr_obj = OCRHandle()
    ocr_obj.artificial_neural_network_train(test_data, True)
