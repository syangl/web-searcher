import sys

def process_bar(now, total):
    '''
    :param now:当前时刻完成度
    :param total:任务总数
    :return: 进度条
    '''
    rate = float(now)/total
    rate_num = int(100*rate)
    r = '\r[{}{}]{}%'.format('#'*rate_num,' '*(100-rate_num), rate_num)
    sys.stdout.write(r)
    sys.stdout.flush()