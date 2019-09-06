# -*- coding: utf-8 -*-
import os
from os import path
from subprocess import check_call, call
from src_helpers import parse_arguments, check_default_qdisc
import project_root  # 'project_root.DIR' is the root directory of Pantheon

def main():

    # 第三方库pcc-rl源码所在地址
    cc_repo = path.join(project_root.DIR, 'third_party', 'pcc-rl')

    src_dir = path.join(cc_repo, 'src')
    lib_dir = path.join(src_dir, 'core')

    app_dir = path.join(src_dir, 'app')

    # 接收端/发送端路径
    send_src = path.join(app_dir, 'pccclient')
    recv_src = path.join(app_dir, 'pccserver')
    # # 确定安装路径，若算法有需要安装其他东西的，可通过此接口指定路径



    os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
    cmd = [recv_src, 'recv', '9000']  # 要不要改成9000？
    check_call(cmd)
    print("testing ...")

    os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
    # 指定端口和IP(要不要换成具体值，待测试)
    cmd = [send_src, 'send', '127.0.0.1', '9000']
    # 指定速率控制(参数含义待测试)
    cmd += ['--pcc-rate-control=python']

    cmd += ['-pyhelper=loaded_client']
    cmd += ['-pypath={}'.format(src_dir) + '/udt-plugins/testing/']
    cmd += ['--history-len=10']

    # 指定模型路径参数
    cmd += ['--model-path={}'.format(cc_repo) + '/model']
    check_call(cmd)

if __name__ == '__main__':
    main()
