#coding:utf-8
import tensorflow as tf
#定义权重矩阵，并设定seed值保证每次计算结果都是一样的
w1=tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
w2=tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
#设定初始值#定义placeholder作为存放 数据的地方，shape也不一定需要定义，有的话会减少错误率
x=tf.placeholder(dtype=tf.float32,shape=(2,2),name="input")
# x=tf.constant([[0.7,0.9]])
#前向传播
a=tf.matmul(x,w1)
y=tf.matmul(a,w2)
#创建新会话
sess=tf.Session()
#初始化w1,,w2
init_op=tf.initialize_all_variables()#直接对所有的变量进行初始化
sess.run(init_op)
# sess.run(w1.initializer)
# sess.run(w2.initializer)
#输出
# print(sess.run(y))
print(sess.run(y,feed_dict={x:[[0.7,0.9],[0.1,0.4]]}))#feed_dict是一个字典用来给出每个用到的placeholder的取值
#定义交叉熵,来刻画预测值与真实之间的差距
cross_entropy=-tf.reduce_mean(y_*tf.log(tf.clip_by_value(y,1e-10,1.0)))
#定义学习率
learning_rate=0.001
#定义反向传播算法来优化神经网络中的参数
train_step=tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
sess.run(train_step )
# 关闭会话
sess.close()

