# MODEL_PATH: path to the model checkpoint
# OUTPUT_PATH: path to the save the prediction results
# SAVE_DIR: directory to the save the evaluation results
# for task, all stands for evaluating on all tasks, also you can specify the task name, e.g. direction, object, etc.

MODEL_PATH=./models/ckpts/MiniCPM-V-2_6
OUTPUT_PATH=./output/micicpm.jsonl
SAVE_DIR=./results

CUDA_VISIBLE_DEVICES=0 python ./scripts/pred_minicpm.py \
            --model_path ${MODEL_PATH} \
            --data_path ../data \
            --output_path ${OUTPUT_PATH} \
            --task all

python eval.py --data_file ${OUTPUT_PATH} --save_dir ${SAVE_DIR}