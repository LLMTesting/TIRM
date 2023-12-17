deepspeed fastchat/train/train_baichuan_lora.py \
    --model_name_or_path ../models/Baichuan2-13B-Chat \
    --lora_r 8 \
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --data_path retrain_train.json \
    --eval_data_path retrain_valid.json \
    --output_dir ./checkpoints_Baichuan2-13B-Chat \
    --num_train_epochs 10 \
    --fp16 True \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "steps" \
    --eval_steps 100  \
    --save_strategy "steps" \
    --save_steps 100 \
    --save_total_limit 512 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_strategy "steps" \
    --logging_steps 128 \
    --tf32 True \
    --model_max_length 1024 \
    --deepspeed playground/deepspeed_config.json \
    --gradient_checkpointing False