#coding:utf-8
from datetime import datetime
import  math
import  time
import  tensorflow as tf
batch_size=32
num_batches=100
#用来显示每一层结构,展示每一个卷积层和池化层输出tensor的尺寸，
#它接受一个tensor作为输入，并显示其名称t.op.name和尺寸t.get_shape().as_list()
def print_activations(t):
    print(t.op.name,'',t.get_shape().as_list())
def inference(images):
    parameters=[]
    #1
    with tf.name_scope('conv1') as scope:#使用name_scope可以讲Variable自动命名为conv1/***，便于区分不同卷积层之间的组件
        kernel=tf.Variable(tf.truncated_normal([11,11,3,64],#使用truncated_normal正太分布函数，初始化卷积核的参数，卷积尺寸为11*11,3为通道数，64为卷积核数量
                                               dtype=tf.float32,stddev=1e-1),name='weights')
        conv=tf.nn.conv2d(images,kernel,[1,4,4,1],padding='SAME')#nn.conv2d对输入的图像进行卷积操作，strides步长设为4*4，padding模式设为same
        biases=tf.Variable(tf.constant(0.0,shape=[64],dtype=tf.float32),
                           trainable=True,name='biases')#将biases全部初始化为零
        bias=tf.nn.bias_add(conv,biases)#将卷积结果和偏执相加
        conv1=tf.nn.relu(bias,name=scope)#将相加结果送到激活函数进行激活
        print_activations(conv1)#打印出卷积层的结构
        parameters+=[kernel,biases]#将参数添加到parameters

        #添加LRN层和最大池化层
        #先使用tf.nn.lrn对前面输出的tensor进行LRN处理，其中depth_radius为4，其他网络都放弃的LRN层因为效果不明显
    # lrn1=tf.nn.lrn(conv1,4,bias=1.0,alpha=0.001/9,beta=0.75,name='lrn1')
    pool1=tf.nn.max_pool(conv1,ksize=[1,3,3,1],strides=[1,2,2,1],#池化尺寸为3*3，取样步长为2*2，padding模式为VALID，即取样不能超过边框
                         padding='VALID',name='pool1')#SAME模式是可以进行边界填充的
    print_activations(pool1)





    #第二个卷积层，忽略注释

    with tf.name_scope('conv2') as scope:  # 使用name_scope可以讲Variable自动命名为conv1/***，便于区分不同卷积层之间的组件
        kernel = tf.Variable(
            tf.truncated_normal([5, 5, 64, 192],  # 使用truncated_normal正太分布函数，初始化卷积核的参数，卷积尺寸为11*11,3为通道数，64为卷积核数量
                                dtype=tf.float32, stddev=1e-1), name='weights')
        conv = tf.nn.conv2d(pool1, kernel, [1, 1, 1, 1],
                            padding='SAME')  # nn.conv2d对输入的图像进行卷积操作，strides步长设为4*4，padding模式设为same
        biases = tf.Variable(tf.constant(0.0, shape=[192], dtype=tf.float32),
                             trainable=True, name='biases')  # 将biases全部初始化为零
        bias = tf.nn.bias_add(conv, biases)  # 将卷积结果和偏执相加
        conv2 = tf.nn.relu(bias, name=scope)  # 将相加结果送到激活函数进行激活
        
        parameters += [kernel, biases]  # 将参数添加到parameters
        print_activations(conv2)  # 打印出卷积层的结构

    #对第二个卷积层进行处理，参数与之前的都一样！


    # lrn1 = tf.nn.lrn(conv1, 4, bias=1.0, alpha=0.001 / 9, beta=0.75, name='lrn1')
    pool2 = tf.nn.max_pool(conv2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1],
                           # 池化尺寸为3*3，取样步长为2*2，padding模式为VALID，即取样不能超过边框
                           padding='VALID', name='pool1')  # SAME模式是可以进行边界填充的
    print_activations(pool1)
    
    
    #3
    with tf.name_scope('conv3') as scope:#使用name_scope可以讲Variable自动命名为conv3/***，便于区分不同卷积层之间的组件
        kernel=tf.Variable(tf.truncated_normal([3,3,192,384],#使用truncated_normal正太分布函数，初始化卷积核的参数，卷积尺寸为11*11,3为通道数，64为卷积核数量
                                               dtype=tf.float32,stddev=1e-1),name='weights')
        conv=tf.nn.conv2d(pool2,kernel,[1,1,1,1],padding='SAME')#nn.conv2d对输入的图像进行卷积操作，strides步长设为4*4，padding模式设为same
        biases=tf.Variable(tf.constant(0.0,shape=[384],dtype=tf.float32),
                           trainable=True,name='biases')#将biases全部初始化为零
        bias=tf.nn.bias_add(conv,biases)#将卷积结果和偏执相加
        conv3=tf.nn.relu(bias,name=scope)#将相加结果送到激活函数进行激活
        
        parameters+=[kernel,biases]#将参数添加到parameters
        print_activations(conv3)  # 打印出卷积层的结构






    #4
    with tf.name_scope('conv4') as scope:  # 使用name_scope可以讲Variable自动命名为conv4/***，便于区分不同卷积层之间的组件
        kernel = tf.Variable(
            tf.truncated_normal([3, 3, 384, 256],  # 使用truncated_normal正太分布函数，初始化卷积核的参数，卷积尺寸为11*11,3为通道数，64为卷积核数量
                                dtype=tf.float32, stddev=1e-1), name='weights')
        conv = tf.nn.conv2d(conv3, kernel, [1, 1, 1, 1],
                            padding='SAME')  # nn.conv2d对输入的图像进行卷积操作，strides步长设为4*4，padding模式设为same
        biases = tf.Variable(tf.constant(0.0, shape=[256], dtype=tf.float32),
                             trainable=True, name='biases')  # 将biases全部初始化为零
        bias = tf.nn.bias_add(conv, biases)  # 将卷积结果和偏执相加
        conv4 = tf.nn.relu(bias, name=scope)  # 将相加结果送到激活函数进行激活

        parameters += [kernel, biases]  # 将参数添加到parameters
        print_activations(conv4)  # 打印出卷积层的结构
        
        
        
    #5
    with tf.name_scope('conv5') as scope:  # 使用name_scope可以讲Variable自动命名为conv5/***，便于区分不同卷积层之间的组件
        kernel = tf.Variable(
            tf.truncated_normal([3, 3, 256, 256],  # 使用truncated_normal正太分布函数，初始化卷积核的参数，卷积尺寸为11*11,3为通道数，64为卷积核数量
                                dtype=tf.float32, stddev=1e-1), name='weights')
        conv = tf.nn.conv2d(conv4, kernel, [1, 1, 1, 1],
                            padding='SAME')  # nn.conv2d对输入的图像进行卷积操作，strides步长设为4*4，padding模式设为same
        biases = tf.Variable(tf.constant(0.0, shape=[256], dtype=tf.float32),
                             trainable=True, name='biases')  # 将biases全部初始化为零
        bias = tf.nn.bias_add(conv, biases)  # 将卷积结果和偏执相加
        conv5 = tf.nn.relu(bias, name=scope)  # 将相加结果送到激活函数进行激活

        parameters += [kernel, biases]  # 将参数添加到parameters
        print_activations(conv5)  # 打印出卷积层的结构




    pool5 = tf.nn.max_pool(conv5, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1],
                           # 池化尺寸为3*3，取样步长为2*2，padding模式为VALID，即取样不能超过边框
                           padding='VALID', name='pool1')  # SAME模式是可以进行边界填充的
    print_activations(pool1)


    return pool5,parameters
#因为全连接层的计算量很小就不放在计算速度测评中了，他们对计算耗时影响非常小





#评估AlexNet每轮计算时间的函数
#session,target需要测评的运算算子,info_string测试的名称
def time_tensorflow_run(session,target,info_string):
    num_steps_burn_in=10#定义预热轮数，只考虑10轮以后的时间
    total_duration=0.0#用来计算方差
    total_duration_squared=0.0


    for i in range(num_batches+num_steps_burn_in):
        start_time=time.time()
        _=session.run(target)
        duration=time.time()-start_time#计算出运算时间
        if i>=num_steps_burn_in:
            if not i % 10:
                print('%s: step %d,duration=%.3f'%
                      (datetime.now(),i-num_steps_burn_in,duration))
                total_duration+=duration
                total_duration_squared+=duration*duration


    mn=total_duration/num_batches#每轮平均耗时
    vr=total_duration_squared/num_batches-mn*mn
    sd=math.sqrt(vr)#计算方差
    print('%s: %s across %d steps,%.3f +/- %.3f sec / batch' %
          (datetime.now(),info_string,num_batches,mn,sd))



#主函数
def run_benchmark():
    with tf.Graph().as_default():
        image_size=224
        images=tf.Variable(tf.random_normal([batch_size,
                                             image_size,
                                             image_size,3],
                                            dtype=tf.float32,
                                            stddev=1e-1))
        pool5,parameters=inference(images)


        init=tf.global_variables_initializer()
        sess=tf.Session()
        sess.run(init)

        time_tensorflow_run(sess,pool5,"Forward")

        objective=tf.nn.l2_loss(pool5)
        grad=tf.gradients(objective,parameters)
        time_tensorflow_run(sess,grad,"Forward-backward")




run_benchmark()
