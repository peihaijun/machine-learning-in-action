#coding:utf-8
import tensorflow as tf
from numpy.random import RandomState
#定义训练数据集
batch_size=8

#定义神经网络参数
w1=tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
w2=tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))

#shape里使用None可以方便使用不大的batch
x=tf.placeholder(tf.float32,shape=(None,2),name='x-input')
y_=tf.placeholder(tf.float32,shape=(None,1),name='y-input')

#前向传播
a=tf.matmul(x,w1)
y=tf.matmul(a,w2)

#定义损失函数
#tf.clip_by_value(A, min, max)：输入一个张量A，
# 把A中的每一个元素的值都压缩在min和max之间。小于min的让它等于min，大于max的元素的值等于max
#交叉熵解释;y_代表正确的结果，y代表预测的结果，tf.clip_by_value(y,1e-10,1.0)是为了避免出现log0或者概率大于1的现象
cross_entropy=-tf.reduce_mean(y_*tf.log(tf.clip_by_value(y,1e-10,1.0)))
train_step=tf.train.AdamOptimizer(0.001).minimize(cross_entropy)


#通过随机数生成一个模拟数据集
rdm=RandomState(1)
dataset_size=128
X=rdm.rand(dataset_size,2)#以给定的形状创建一个数组，并在数组中加入在[0,1]之间均匀分布的随机样本。
#定义规则来给出样本标签，所有的x1+x2<1的样例都被认为是正样本，而其他被
#认为是负样本（不合格），这里使用0表示负样本，1表示正样本
Y=[[int(x1+x2<1)] for (x1,x2) in X]#Y是用来打标注的，利用int来将之和小于1的设为0大于一的设为1
# print Y
#创建一个会话来运行tensorflow程序
with tf.Session() as sess:
    # 这是初始化所有变量的方法
    init_op=tf.initialize_all_variables()
    sess.run(init_op)

    print sess.run(w1)
    print sess.run(w2)

    #设定训练的轮数
    STEPS=5000
    for i in range(STEPS):
        #每次选取batch_size个样本进行训练
        start=(i*batch_size)%dataset_size
        end=min(start+batch_size,dataset_size)

        #通过选取的样本训练神经网络并更新参数
        sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})
        if i % 1000==0:
            #每个一段时间计算在所有数据上的交叉熵输出
            total_cross_entropy=sess.run(cross_entropy,feed_dict={x:X,y_:Y})
            print ("After %d training steps, cross entropy on all data is %g"%
                   (i,total_cross_entropy))



    print sess.run(w1)
    print sess.run(w2)


