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
    processor = AutoProcessor.from_pretrained(args.model_path, do_image_spliting=False)
    model = AutoModelForVision2Seq.from_pretrained(
        args.model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

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
        inputs = processor(text=prompt, images=images, return_tensors="pt").to(model.device)
        generated_ids = model.generate(**inputs, max_new_tokens=500, temperature=0.0, do_sample=False)
        response = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].split('\nAssistant: ')[1].split('.')[0]
        with open(args.output_path, "a") as f:
            item["pred"] = response
            f.write(json.dumps(item) + '\n')
    