import tornado.ioloop
import tornado.web
import os,cv2,json
import numpy as np
import tensorflow as tf
from PIL import Image



saver = tf.train.import_meta_graph("./model/model.ckpt-2605.meta", clear_devices=True)
graph = tf.get_default_graph()
x = graph.get_tensor_by_name("data-input:0")
pred = graph.get_tensor_by_name("predict_max_idx:0")
keep = graph.get_tensor_by_name("keep-prob:0")

def resize_img(img_file):
    img = Image.open(img_file)
    if img.size[0]==img.size[1]==64:
        return img_file
    else:
        img = img.resize((64, 64), Image.ANTIALIAS)
        # new_img="./temp/temp.png"
        img.save(img_file)
        return img_file

def get_result(img_file):
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint("./model/"))
        predict = sess.run(pred, feed_dict={x: [np.asarray(cv2.imread(resize_img(img_file)), dtype=np.float32).flatten()], keep: 1.0})
        result=predict[0][0]+1
        if result==1:
            return "anger"
        elif result==2:
            return "contempt"
        elif result == 3:
            return "disgust"
        elif result == 4:
            return "fear"
        elif result == 5:
            return "happy"
        elif result == 6:
            return "sadness"
        elif result == 7:
            return "surprise"
        else:
            return "i don't know"

class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
        <html>
          <head><title>Upload File</title></head>
          <body>
            <form action='file' enctype="multipart/form-data" method='post'>
            <input type='file' name='file'/><br/>
            <input type='submit' value='submit'/>
            </form>
          </body>
        </html>
        ''')

    def post(self):
        #文件的暂存路径
        ret = {'result': 'OK'}
        upload_path=os.path.join(os.path.dirname(__file__),'files')
        #提取表单中‘name’为‘file’的文件元数据
        file_metas=self.request.files['file']
        for meta in file_metas:
            filename=meta['filename']
            filepath=os.path.join(upload_path,filename)
            #有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            out=get_result("./files/"+filename)
            ret['result']=out
            self.write(json.dumps(ret))
            os.remove("./files/"+filename)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


app=tornado.web.Application([
    (r'/file',UploadFileHandler),
])


if __name__ == '__main__':
    app.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
