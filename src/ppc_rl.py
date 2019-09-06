# -*- coding: utf-8 -*-
import os
from os import path
from subprocess import check_call, call
from src_helpers import parse_arguments, check_default_qdisc
import project_root  # 'project_root.DIR' is the root directory of Pantheon

def main():

    # 返回命令行指定的参数
    args = parse_arguments('receiver_first')

    # 第三方库pcc-rl源码所在地址
    cc_repo = path.join(project_root.DIR, 'third_party', 'pcc-rl')

    src_dir = path.join(cc_repo, 'src')
    lib_dir = path.join(src_dir, 'core')

    app_dir = path.join(src_dir, 'app')

    # 接收端/发送端路径
    send_src = path.join(app_dir, 'pccclient')
    recv_src = path.join(app_dir, 'pccserver')

    # # 确定安装路径，若算法有需要安装其他东西的，可通过此接口指定路径
    # setup_src = path.join(cc_repo, 'example_setup')

    # 可选，安装算法需要的特定环境，例如要求TensorFlow?pytorch?填上代码
    # if args.option == 'deps':
    #     # 添加执行pcc-rl所需依赖环境的代码
    #     print("test for pcc")

    # 必选，指定哪个先运行
    if args.option == 'run_first':

        print 'reveiver'

    # 可选，确定以非root用户运行
    if args.option == 'setup':
        # avoid running anything as root here
        # 可添加一下安装时，加以控制的代码
        # 添加运行编译的代码
        # check_call([setup_src])
        check_call(['make'], cwd=src_dir)

    # 可选，指定队列大小，默认值就好
    if args.option == 'setup_after_reboot':
        check_default_qdisc('pcc_rl')

    # 必选，指定接收端IP和端口
    if args.option == 'receiver':
        # 添加指定端口和ip的代码，如果run_first为receiver，指定其端口和IP
        # cd src export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:pwd/core/ ./app/pccserver recv 9000

        # cd ../pcc-rl/src  # 进入编译文件所在目录
        # make  # 编译并生成两个app，client和server
        # LD_LIBRARY_PATH =$LD_LIBRARY_PATH:pwd/core # 设置当路径
        # ./app/pccserver recv 9000  # 启动reveiver并监听9000端口

        os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
        cmd = [recv_src, 'recv', args.port]  # 要不要改成9000？
        check_call(cmd)
        print("testing ...")

    # 必选，指定发送端IP和端口
    if args.option == 'sender':
        # ./app/pccclient send 127.0.0.1 9000
        # --pcc-rate-control=python
        # -pyhelper=loaded_client
        #
        # -pypath=/path/to/pcc-rl/src/udt-plugins/testing/
        # /home/tky/zhao/pantheon/third_party/pcc-rl/src/udt-plugins/testing /
        #
        # --history-len=10
        # --pcc-utility-calc=linear
        #
        # --model-path=/path/to/your/model/
        # /home/tky/zhao/pantheon/third_party/pcc-rl/model

        os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
        # 指定端口和IP(要不要换成具体值，待测试)
        cmd = [send_src, 'send', args.ip, args.port]
        # 指定速率控制(参数含义待测试)
        cmd += ['--pcc-rate-control=python']

        cmd += ['-pyhelper=loaded_client']
        cmd += ['-pypath={}'.format(src_dir) + '/udt-plugins/testing/']
        cmd += ['--history-len=10']
        cmd += ['--pcc-utility-calc=linear']

        # 指定模型路径参数
        cmd += ['--model-path={}'.format(cc_repo) + '/model']
        check_call(cmd)



if __name__ == '__main__':
    main()
