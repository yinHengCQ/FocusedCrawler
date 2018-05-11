import tensorflow as tf
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

CAPTCHA_LEN = 1

MODEL_SAVE_PATH = 'C:/Users/admin/Desktop/result/'
TEST_IMAGE_PATH = 'C:/Users/admin/Desktop/old/'

CHAR_ODR_MAP={'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '36': 'a', '37': 'b', '38': 'c', '39': 'd', '40': 'e', '41': 'f', '42': 'g', '43': 'h', '44': 'i', '45': 'j', '46': 'k', '47': 'l', '48': 'm', '49': 'n', '50': 'o', '51': 'p', '52': 'q', '53': 'r', '54': 's', '55': 't', '56': 'u', '57': 'v', '58': 'w', '59': 'x', '60': 'y', '61': 'z', '10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F', '16': 'G', '17': 'H', '18': 'I', '19': 'J', '20': 'K', '21': 'L', '22': 'M', '23': 'N', '24': 'O', '25': 'P', '26': 'Q', '27': 'R', '28': 'S', '29': 'T', '30': 'U', '31': 'V', '32': 'W', '33': 'X', '34': 'Y', '35': 'Z'}



def get_image_data_and_name(fileName, filePath=TEST_IMAGE_PATH):
    pathName = os.path.join(filePath, fileName)
    img = Image.open(pathName)
    # 转为灰度图
    img = img.convert("L")
    image_array = np.array(img)
    image_data = image_array.flatten() / 255
    image_name = fileName[0:CAPTCHA_LEN]
    return image_data, image_name


def digitalStr2Array(digitalStr):
    digitalList = []
    def char2pos(c):
        if c == '_':
            k = 62
            return k
        k = ord(c) - 48
        if k > 9:
            k = ord(c) - 55
            if k > 35:
                k = ord(c) - 61
                if k > 61:
                    raise ValueError('No Map')
        return k

    for c in digitalStr:
        print(c)
        digitalList.append(char2pos(c))
    return np.array(digitalList)


def model_test():
    nameList = []
    for pathName in os.listdir(TEST_IMAGE_PATH):
        nameList.append(pathName.split('/')[-1])
    totalNumber = len(nameList)
    # 加载graph
    saver = tf.train.import_meta_graph(MODEL_SAVE_PATH + "crack_captcha.model-1900.meta")
    graph = tf.get_default_graph()
    # 从graph取得 tensor，他们的name是在构建graph时定义的(查看上面第2步里的代码)
    input_holder = graph.get_tensor_by_name("data-input:0")
    keep_prob_holder = graph.get_tensor_by_name("keep-prob:0")
    predict_max_idx = graph.get_tensor_by_name("predict_max_idx:0")
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint(MODEL_SAVE_PATH))
        count = 0
        for fileName in nameList:
            img_data, img_name = get_image_data_and_name(fileName, TEST_IMAGE_PATH)
            predict = sess.run(predict_max_idx, feed_dict={input_holder: [img_data], keep_prob_holder: 1.0})
            filePathName = TEST_IMAGE_PATH + fileName
            print(filePathName)
            # img = Image.open(filePathName)
            # plt.imshow(img)
            # plt.axis('off')
            # plt.show()
            predictValue = np.squeeze(predict)
            rightValue = digitalStr2Array(img_name)
            # if np.array_equal(predictValue, rightValue):
            if rightValue[0]==predictValue:
                result = '正确'
                count += 1
            else:
                result = '错误'
            print('实际值：{}， 预测值：{}，测试结果：{}'.format(rightValue, predictValue, result))
            print(CHAR_ODR_MAP[str(predictValue)])
            print('\n')

        print('正确率：%.2f%%(%d/%d)' % (count * 100 / totalNumber, count, totalNumber))


if __name__ == '__main__':
    model_test()