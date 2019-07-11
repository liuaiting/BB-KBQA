#!/usr/bin/env bash
export BERT_BASE_DIR=./chinese_L-12_H-768_A-12
export MY_DATASET=./data/XQPM
python run_classifier.py \
  --task_name=nlpccxqpm \
  --do_train=true \
  --do_eval=true \
  --do_predict=true \
  --data_dir=$MY_DATASET \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --max_seq_length=60 \
  --train_batch_size=32 \
  --learning_rate=5e-5 \
  --num_train_epochs=5 \
  --output_dir=./xqpm_output/