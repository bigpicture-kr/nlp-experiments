#!/bin/bash

if [ "$1" = "train" ]; then
    python run_qa.py \
        --model_name_or_path bert-base-multilingual-cased \
        --dataset_name squad_kor_v1 \
        --do_train \
        --do_eval \
        --per_device_train_batch_size 8 \
        --learning_rate 3e-5 \
        --num_train_epochs 2 \
        --max_seq_length 384 \
        --doc_stride 128 \
        --output_dir /tmp/debug_squad_kor_v1/
elif [ "$1" = "eval" ]; then
    python ./squad_kor_v1_local/evaluate.py ./data/KorQuAD_v1.0_dev.json ./tmp/debug_squad_kor_v1/predictions.json
if [ "$1" = "train_v2" ]; then
    python run_qa.py \
        --model_name_or_path bert-base-uncased \
        --dataset_name squad_kor_v2 \
        --do_train \
        --do_eval \
        --per_device_train_batch_size 8 \
        --learning_rate 3e-5 \
        --num_train_epochs 2 \
        --max_seq_length 384 \
        --doc_stride 128 \
        --output_dir /tmp/debug_squad_kor_v2/
elif [ "$1" = "eval_v2" ]; then
    python ./squad_kor_v2_local/evaluate.py ./data/KorQuAD_v2.0_dev.json ./tmp/debug_squad_kor_v2/predictions.json
else
	echo "Invalid Option Selected"
fi
