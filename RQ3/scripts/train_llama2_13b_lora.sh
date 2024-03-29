deepspeed fastchat/train/train_lora.py \
    --model_name_or_path ../models/Llama-2-13b-hf  \
    --lora_r 8 \
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --data_path retrain_mixed.json \
    --eval_data_path retrain_valid.json \
    --output_dir ./checkpoints \
    --num_train_epochs 10 \
    --fp16 True \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "steps" \
    --eval_steps 100  \
    --save_strategy "steps" \
    --save_steps 1000 \
    --save_total_limit 512 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_strategy "steps" \
    --logging_steps 128 \
    --tf32 True \
    --model_max_length 2048 \
    --q_lora False \
    --deepspeed playground/deepspeed_config.json \
    --gradient_checkpointing True \
    --flash_attn False
