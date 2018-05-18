from PIL import Image
import numpy as np
from collections import Counter
import tensorflow as tf



CHAR_ODR_MAP={'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '36': 'a', '37': 'b', '38': 'c', '39': 'd', '40': 'e', '41': 'f', '42': 'g', '43': 'h', '44': 'i', '45': 'j', '46': 'k', '47': 'l', '48': 'm', '49': 'n', '50': 'o', '51': 'p', '52': 'q', '53': 'r', '54': 's', '55': 't', '56': 'u', '57': 'v', '58': 'w', '59': 'x', '60': 'y', '61': 'z', '10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F', '16': 'G', '17': 'H', '18': 'I', '19': 'J', '20': 'K', '21': 'L', '22': 'M', '23': 'N', '24': 'O', '25': 'P', '26': 'Q', '27': 'R', '28': 'S', '29': 'T', '30': 'U', '31': 'V', '32': 'W', '33': 'X', '34': 'Y', '35': 'Z'}
CAPTCHA_LEN = 1

MODEL_SAVE_PATH = 'C:/Users/admin/Desktop/result/'




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

    def model_test(pic_list):
        str_result=""
        # 加载graph
        saver = tf.train.import_meta_graph(MODEL_SAVE_PATH + "crack_captcha.model-4000.meta")
        graph = tf.get_default_graph()
        # 从graph取得 tensor，他们的name是在构建graph时定义的(查看上面第2步里的代码)
        input_holder = graph.get_tensor_by_name("data-input:0")
        keep_prob_holder = graph.get_tensor_by_name("keep-prob:0")
        predict_max_idx = graph.get_tensor_by_name("predict_max_idx:0")

        # aa=0

        with tf.Session() as sess:
            saver.restore(sess, tf.train.latest_checkpoint(MODEL_SAVE_PATH))
            for img in pic_list:

                # aa+=1
                # img.save("C:/Users/admin/Desktop/cutout/{0}.jpg".format(str(aa)))  # 保存修改像素点后的图片

                predict = sess.run(predict_max_idx,feed_dict={input_holder: [get_image_data(img)], keep_prob_holder: 1.0})
                predictValue = np.squeeze(predict)
                str_result+=CHAR_ODR_MAP[str(predictValue)]
        return str_result
    return model_test(pic_list)

# img=Image.open("C:/Users/admin/Desktop/zhixing/zhixing22.jpg")
# pic_list=cut(img)
# out=single_pic_to_text(pic_list)
# print(out)

for index in range(1 ,33):
    img=Image.open(r"C:\Users\admin\Desktop\old\{0}.png".format(index))
    # img = Image.open(r"C:\Users\admin\Desktop\zhixing\zhixing{0}.jpg".format(index))

    pic_list=cut(img)
    out=single_pic_to_text(pic_list)
    print("{0}--{1}".format(out,index))


# def pic2text(img_path):
#     pic_list=cut(Image.open(img_path))
#     return single_pic_to_text(pic_list)
#
# import sys
# img_path=sys.argv[1]
# print(pic2text(img_path))

