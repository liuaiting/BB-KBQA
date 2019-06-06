#!/usr/bin/env bash
export BERT_BASE_DIR=./chinese_L-12_H-768_A-12
export MY_DATASET=./data/MD
python run_md.py \
  -do_train \
  -do_eval \
  -do_predict \
  -data_dir $MY_DATASET \
  -vocab_file $BERT_BASE_DIR/vocab.txt \
  -bert_config_file $BERT_BASE_DIR/bert_config.json \
  -init_checkpoint $BERT_BASE_DIR/bert_model.ckpt \
  -max_seq_length 60 \
  -batch_size 32 \
  -learning_rate 1e-5 \
  -num_train_epochs 30 \
  -output_dir ./md_output/ \
  -device_map 1
