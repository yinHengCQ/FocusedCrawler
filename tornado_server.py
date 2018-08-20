# -*- coding: utf-8 -*-

import time, os
import tensorflow as tf
import origin
from config import ps_hosts, worker_hosts
from socket_client import send_finish_info, local_ip

GPU_USE_RATE = 0.9

# 模型保存的路径。
MODEL_SAVE_PATH = "./model"

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('job_name', 'worker', ' "ps" or "worker" ')
tf.app.flags.DEFINE_integer('task_index', 0, 'Task ID of the worker/replica running the training.')
tf.app.flags.DEFINE_string("cuda", "", "specify gpu")

if FLAGS.cuda:
    os.environ["CUDA_VISIBLE_DEVICES"] = FLAGS.cuda

is_chief = (FLAGS.task_index == 0)

start_time = time.time()


class MyStopAtStepHook(tf.train.StopAtStepHook):
    def after_run(self, run_context, run_values):
        global_step = run_values.results + 1
        if global_step >= self._last_step:
            print("task finish,total time count:%s" % (time.time() - start_time))
            send_finish_info()
            step = run_context.session.run(self._global_step_tensor)
            if step >= self._last_step:
                run_context.request_stop()


def main(argv=None):
    cluster = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})
    server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)

    if FLAGS.job_name == 'ps':
        with tf.device("/cpu:0"):
            server.join()

    hooks = [MyStopAtStepHook(last_step=origin.TRAINING_STEPS)]
    device_setter = tf.train.replica_device_setter(ps_device="/job:ps/task:%d" % FLAGS.task_index,
                                                   worker_device="/job:worker/task:%d" % FLAGS.task_index,
                                                   cluster=cluster)

    with tf.device(device_setter):
        origin.build_model(is_chief)
        sess_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False,
                                     gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=GPU_USE_RATE))

    with tf.train.MonitoredTrainingSession(master=server.target, is_chief=is_chief, checkpoint_dir=MODEL_SAVE_PATH,
                                           hooks=hooks,
                                           save_checkpoint_secs=origin.SAVE_CHECKPOINT_SECS,
                                           config=sess_config) as mon_sess:
        print("session started.")
        step = 0

        while True:
            current_info = origin.train_model(session=mon_sess, step=step)
            for info in current_info:
                print(info)
            step += 1


if __name__ == "__main__":
    try:
        tf.app.run()
    except:
        exit(1)
