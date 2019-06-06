#!/usr/bin/env bash
export BERT_BASE_DIR=./chinese_L-12_H-768_A-12
export MY_DATASET=./data/PM
python run_classifier.py \
  --task_name=nlpccpmwm \
  --do_train=false \
  --do_eval=false \
  --do_predict=true \
  --data_dir=$MY_DATASET \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --max_seq_length=60 \
  --train_batch_size=32 \
  --learning_rate=5e-5 \
  --num_train_epochs=3.0 \
  --output_dir=./pm_output_with_mention/