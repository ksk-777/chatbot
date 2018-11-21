import matplotlib.pyplot as plt
import tensorflow as tf
from algorithm.model import Seq2Seq
from algorithm.util import DataUtil


class ChatTraining(object):

    def __init__(self):
        util = DataUtil()
        self.input_batches, self.target_batches = util.load_data()

    def training(self):
        # 트레이닝
        tf.reset_default_graph()
        with tf.Session() as sess:
            model = Seq2Seq(mode="training")
            model.build()
            data = (self.input_batches, self.target_batches)
            loss_history = model.train(sess, data, from_scratch=True,
                                       save_path=model.ckpt_dir + f'epoch_{model.n_epoch}')

        plt.figure(figsize=(20, 10))
        plt.scatter(range(model.n_epoch), loss_history)
        plt.title('Learning Curve')
        plt.xlabel('Global step')
        plt.ylabel('Loss')
        plt.show()

    def inference(self):
        tf.reset_default_graph()
        with tf.Session() as sess:
            model = Seq2Seq(mode='inference')
            model.build()
            for input_batch, target_batch in zip(self.input_batches, self.target_batches):
                data = (input_batch, target_batch)
                model.inference(sess, data, load_ckpt=model.ckpt_dir + f'epoch_{model.n_epoch}')


def main(_):
    chat = ChatTraining()
    #chat.training()
    chat.inference()

if __name__ == "__main__":
    tf.app.run()