# MODEL_PATH: path to the model checkpoint
# OUTPUT_PATH: path to the save the prediction results
# for task, all stands for evaluating on all tasks, also you can specify the task name, e.g. direction, object, etc.

CUDA_VISIBLE_DEVICES=0 python ./scripts/pred_minicpm.py \
            --model_path ${MODEL_PATH} \
            --data_path ../data \
            --output_path ${OUTPUT_PATH} \
            --task all