import json 
from tqdm import tqdm
import argparse
from transformers import AutoProcessor, AutoModelForVision2Seq
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
    processor = AutoProcessor.from_pretrained(args.model_path)
    model = AutoModelForVision2Seq.from_pretrained(
        args.model_path,
        device_map="auto",
    ).to(device)
    generation_kwargs = {
        "max_new_tokens": 1024,
        "num_beams": 1,
        "temperature": 0.01,
        "do_sample": False
    }

    print("===== predicting =====")
    for item in tqdm(data):
        images = [Image.open(image) for image in item["images"]]
        num_image = len(item["images"])
        content = [{"type": "image"} for i in range(num_image)]
        question = item["query"]
        content.append({"type": "text", "text": question})
        messages = [
            {
                "role": "user",
                "content": content,
            }    
        ]
        prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(text=prompt, images=images, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        generated_ids = model.generate(**inputs, **generation_kwargs)
        response = processor.batch_decode(generated_ids[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]
        with open(args.output_path, "a") as f:
            item["pred"] = response
            f.write(json.dumps(item) + '\n')
    