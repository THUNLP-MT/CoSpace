from PIL import Image 
import requests 
from transformers import AutoModelForCausalLM 
from transformers import AutoProcessor 
from tqdm import tqdm
import argparse
import json

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
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path, 
        device_map="cuda", 
        trust_remote_code=True, 
        torch_dtype="auto", 
        _attn_implementation='eager'    
    )
    processor = AutoProcessor.from_pretrained(
        args.model_path, 
        trust_remote_code=True, 
        num_crops=4
    ) 

    print("===== predicting =====")
    for item in tqdm(data):
        images = [Image.open(image) for image in item["images"]]
        num_image = len(item["images"])
        placeholder = ""
        for idx, image in enumerate(images, start=1):
            placeholder = placeholder + f"<|image_{idx}|>\n"
        question = placeholder + item["query"]
        messages = [{"role": "user", "content": question}]
        prompt = processor.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        inputs = processor(prompt, images, return_tensors="pt").to("cuda:0") 
        generation_args = { 
            "max_new_tokens": 1000, 
            "temperature": 0.0, 
            "do_sample": False, 
        } 
        generate_ids = model.generate(**inputs, 
            eos_token_id=processor.tokenizer.eos_token_id, 
            **generation_args
        )
        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
        response = processor.batch_decode(generate_ids, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=False)[0] 
        with open(args.output_path, "a") as f:
            item["pred"] = response
            f.write(json.dumps(item) + '\n')
    
