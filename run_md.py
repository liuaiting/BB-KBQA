# -*- coding: utf-8 -*-
import os
import sys

from ner.train_helper import get_args_parser
from ner.bert_lstm_ner import train


def train_ner():
    args = get_args_parser()
    if True:
        param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])
        print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))
    # print(args)
    os.environ['CUDA_VISIBLE_DEVICES'] = args.device_map
    train(args=args)


if __name__ == '__main__':
    train_ner()
