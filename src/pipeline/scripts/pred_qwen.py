import json 
from tqdm import tqdm
import argparse
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
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
    model = Qwen2VLForConditionalGeneration.from_pretrained(args.model_path, torch_dtype="auto", device_map="auto")
    processor = AutoProcessor.from_pretrained(args.model_path)

    print("===== predicting =====")
    for item in tqdm(data):
        images = [Image.open(image) for image in item["images"]]
        content = [{"type": "image", "image": path, "resized_height": 560, "resized_width": 1120} for path in item["images"]]
        question = item["query"]
        content.append({"type": "text", "text": question})
        messages = [
            {
                "role": "user",
                "content": content,
            }
        ]
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        ).to("cuda")
        generated_ids = model.generate(**inputs, max_new_tokens=128, temperature=0.01)
        generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
        response = processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        with open(args.output_path, "a") as f:
            item["pred"] = response
            f.write(json.dumps(item) + '\n')