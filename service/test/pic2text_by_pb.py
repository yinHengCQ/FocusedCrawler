#coding=utf-8
#读取存储的图，可运行
import tensorflow as tf
import numpy as np
from PIL import Image
from collections import Counter


CHAR_ODR_MAP={'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '36': 'a', '37': 'b', '38': 'c', '39': 'd', '40': 'e', '41': 'f', '42': 'g', '43': 'h', '44': 'i', '45': 'j', '46': 'k', '47': 'l', '48': 'm', '49': 'n', '50': 'o', '51': 'p', '52': 'q', '53': 'r', '54': 's', '55': 't', '56': 'u', '57': 'v', '58': 'w', '59': 'x', '60': 'y', '61': 'z', '10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F', '16': 'G', '17': 'H', '18': 'I', '19': 'J', '20': 'K', '21': 'L', '22': 'M', '23': 'N', '24': 'O', '25': 'P', '26': 'Q', '27': 'R', '28': 'S', '29': 'T', '30': 'U', '31': 'V', '32': 'W', '33': 'X', '34': 'Y', '35': 'Z'}






# x_2 = tf.placeholder("float", shape=[None, 2025], name="data-input")
# y__2 = tf.placeholder("float", [None, 62], name='label-input')

def cut(img):
    temp = []
    temp_point_position = {}

    def classify_color_point(orgin, result=[]):
        standard_point = np.asarray(orgin[0][0].split('-'), dtype=int)
        temp_orgin = orgin.copy()
        for var in orgin[1:]:
            if abs(np.asarray(var[0].split('-'), dtype=int) - standard_point).sum() < 10:
                temp_orgin.remove(var)
        temp_orgin.remove(orgin[0])
        result.append(orgin[0][0].split('-'))
        if len(result) < 4:
            classify_color_point(temp_orgin, result)
            return result
        else:
            return result

    def is_nearby_point(current_point, color_point_position=[]):
        for i in color_point_position:
            if abs(i[0] - current_point[0]) < 3 and abs(i[1] - current_point[1]) < 20:
                return True
            else:
                False

    def resize_box(im):
        x_list = []
        y_list = []
        for x_index in range(im.shape[1]):
            for y_index in range(im.shape[0]):
                point = im[y_index][x_index]
                if not point.sum():
                    x_list.append(x_index)
                    y_list.append(y_index)
        left, up, right, down = min(x_list), min(y_list), max(x_list), max(y_list)
        if right - left < 15:
            return left - 6, up, right + 6, down
        else:
            return left, up, right, down

    def change_color(img, specify_color):
        width = img.size[0]  # 长度
        height = img.size[1]  # 宽度

        color_point_position = []
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                data = (img.getpixel((i, j)))  # 打印该图片的所有点
                if (abs(data[0] - int(specify_color[0])) < 10 and abs(data[1] - int(specify_color[1])) < 10 and abs(
                        data[2] - int(specify_color[2])) < 10):
                    color_point_position.append(np.asarray([i, j]))
                elif color_point_position != [] and is_nearby_point(np.asarray([i, j]), color_point_position):
                    pass
                else:
                    img.putpixel((i, j), (255, 255, 255, 255))

        img = img.convert("L")  # 把图片强制转成RGB

        threshold = 255;
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        out = img.point(table, '1')

        box = resize_box(np.asarray(out))
        out = out.crop(box).resize((45, 45))

        # out.save("C:/Users/admin/Desktop/cutout/{0}.jpg".format(str(specify_color[0])))  # 保存修改像素点后的图片
        return out


    def list2str(orgin):
        temp = {}
        for i in orgin:
            temp[temp_point_position["-".join(i)]] = i
        key_list = []
        for k, v in temp.items():
            key_list.append(int(k))
        key_list.sort()
        result = []
        for i in key_list:
            result.append(temp[i])
        return result

    def cut_pic(img):
        pic_list=[]
        im = np.asarray(img)
        for x_index in range(im.shape[1]):
            for y_index in range(im.shape[0]):
                point = im[y_index][x_index]
                point_describe = point.sum()
                if point_describe < 730:
                    # point_temp = "{0}-{1}-{2}-{3}".format(point[0], point[1], point[2], point[3])

                    point_temp = "{0}-{1}-{2}".format(point[0], point[1], point[2])

                    temp.append(point_temp)
                    temp_point_position[point_temp] = x_index

        char_point_color = classify_color_point(Counter(temp).most_common()[:15])
        char_point_color = list2str(char_point_color)
        for i in range(len(char_point_color)):
            pic_list.append(change_color(img.copy(), char_point_color[i]))
        return pic_list

    return cut_pic(img)

def single_pic_to_text(pic_list):
    def get_image_data(img):
        img = img.convert("L")
        image_array = np.array(img)
        image_data = image_array.flatten() / 255
        return image_data

    str_result = ""
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()
        output_graph_path = r'C:\Users\admin\Desktop\java_result\graph.pb'

        with open(output_graph_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")

        with tf.Session() as sess:
            tf.initialize_all_variables().run()
            input_x = sess.graph.get_tensor_by_name("data-input:0")
            keep_prob_holder = sess.graph.get_tensor_by_name("keep-prob:0")
            output = sess.graph.get_tensor_by_name("predict_max_idx:0")

            for img in pic_list:
                y_conv_2 = sess.run(output, feed_dict={input_x: [get_image_data(img)],keep_prob_holder: 1.0})
                predictValue = np.squeeze(y_conv_2)
                str_result += CHAR_ODR_MAP[str(predictValue)]
        return str_result

img=Image.open("C:/Users/admin/Desktop/sss/37.jpg")
pic_list=cut(img)
out=single_pic_to_text(pic_list)
print(out)
