"""
This script is an example script which is used to predict the results of the MiniCPM model.
To evaluate a new model, please modify the script to correctly load the model checkpoint and generate the prediction results.
"""

import json 
from tqdm import tqdm
import argparse
from transformers import AutoModel, AutoTokenizer
import torch
from PIL import Image

from load_data import load_data


def load_args():
    parser = argparse.ArgumentParser(description='args for evaluation')
    parser.add_argument('--model_path', type=str, required=True)
    parser.add_argument('--data_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--task', type=str, required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = load_args()

    print("===== loading data =====")
    data = load_data(args)

    print("===== loading model =====")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModel.from_pretrained(args.model_path, trust_remote_code=True, attn_implementation=None, torch_dtype=torch.bfloat16)
    model = model.eval().cuda()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)

    print("===== predicting =====")
    for item in tqdm(data):
        images = [Image.open(image) for image in item["images"]]
        content = [image for image in images]
        question = item["query"]
        content.append(question)
        messages = [
            {
                "role": "user",
                "content": content,
            }    
        ]
        response = model.chat(
            image=None,
            msgs=messages,
            temperature=0.01,
            tokenizer=tokenizer
        )
        with open(args.output_path, "a") as f:
            item["pred"] = response
            f.write(json.dumps(item) + '\n')
    