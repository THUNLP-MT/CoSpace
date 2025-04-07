import json 
import argparse
import re
import os


def load_args():
    parser = argparse.ArgumentParser(description='args for evaluation')
    parser.add_argument('--data_file', type=str, required=True)
    parser.add_argument('--save_dir', type=str, required=True)

    args = parser.parse_args()
    return args
    

if __name__ == '__main__':
    args = load_args()

    data = []
    with open(args.data_file, "r") as f:
        for line in f:
            data.append(json.loads(line))


    num2word = {str(i): word for i, word in enumerate(["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven"], 0)}
    num2wordupper = {str(i): word for i, word in enumerate(["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven"], 0)}
    stat = {}  
            
    for item in data:
        if "planning" not in item["task"]:
            answer = item["answer"]
            pred = item["pred"]

            pred = pred.replace("Answer", "")
            pred = pred.replace("answer", "")

            if "counting" in item["task"] or "dif-ang" in item["task"]:
                match = re.search(r'\b\d+\b', pred)
                if match:
                    pred = match.group(0)
                else:
                    try:
                        word = num2word[answer]
                        wordupper = num2wordupper[answer]
                        if word in pred or wordupper in pred:
                            pred = answer
                        else:
                            pred = "-1"
                    except:
                        pred = "-1"

            else:
                answer_ = f"{answer}."
                others = ["A.", "B.", "C.", "D."]
                others.remove(answer_)
                flag = True
                if answer_ in pred:
                    for other in others:
                        if other in pred:
                            flag = False
                    if flag:
                        pred = answer
                else:
                    match = re.findall(r'[A-Z]', pred)
                    if match:
                        pred = match[-1]
                    else:
                        pred = 'E'

            if item["task"] not in stat:
                stat[item["task"]] = {"succ": 0, "alls": 0}
            stat[item["task"]]["alls"] = stat[item["task"]]["alls"] + 1
            if pred == answer:
                stat[item["task"]]["succ"] = stat[item["task"]]["succ"] + 1
                
        else:

            pred = item["pred"]
            answer_qa = item["answer-qa"]
            answer_dec = item["answer-dec"]
            try:
                cleaned_string = pred.split("{", 1)[1].rsplit("}", 1)[0].strip()
                cleaned_string = cleaned_string.replace("'", '"').replace(":", ": ")
                json_string = "{" + cleaned_string + "}"
                pred = json.loads(json_string)
                pred_qa = pred["Answer1"]
                pred_dec = pred["Answer2"]
                match_qa = re.findall(r'[A-Z]', pred_qa)
                if match_qa:
                    pred_qa = match_qa[-1]
                else:
                    pred_qa = pred_qa[0]
                match_dec = re.findall(r'[A-Z]', pred_dec)
                if match_dec:
                    pred_dec = match_dec[-1]
                else:
                    pred_dec = pred_dec[0]
            except:
                pred_qa = "E"
                pred_dec = "E"

            if "-2" not in item["task"]:
                if "planning-qa" not in stat and "planning-dec" not in stat:
                    stat["planning-qa"] = {"succ": 0, "alls": 0}
                    stat["planning-dec"] = {"succ": 0, "alls": 0}
                stat["planning-qa"]["alls"] = stat["planning-qa"]["alls"] + 1
                stat["planning-dec"]["alls"] = stat["planning-dec"]["alls"] + 1
                if pred_qa == answer_qa:
                    stat["planning-qa"]["succ"] = stat["planning-qa"]["succ"] + 1
                if pred_dec == answer_dec:
                    stat["planning-dec"]["succ"] = stat["planning-dec"]["succ"] + 1
    
            else:
                if "planning-qa-2" not in stat and "planning-dec-2" not in stat:
                    stat["planning-qa-2"] = {"succ": 0, "alls": 0}
                    stat["planning-dec-2"] = {"succ": 0, "alls": 0}
                stat["planning-qa-2"]["alls"] = stat["planning-qa-2"]["alls"] + 1
                stat["planning-dec-2"]["alls"] = stat["planning-dec-2"]["alls"] + 1
                if pred_qa == answer_qa:
                    stat["planning-qa-2"]["succ"] = stat["planning-qa-2"]["succ"] + 1
                if pred_dec == answer_dec:
                    stat["planning-dec-2"]["succ"] = stat["planning-dec-2"]["succ"] + 1

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
        print(f"Creating Directory: {args.save_dir}")

    result_path = os.path.join(args.save_dir, args.data_file.split("/")[-1].replace(".jsonl", ".txt"))
    with open(result_path, "w") as f:
        f.write(f"Evaluated File: {args.data_file}\n")
        for key, value in stat.items():
            succ = value["succ"]
            alls = value["alls"]
            try:
                print(f"task {key}: pass {succ}, all {alls}, accuracy {succ/alls}")
                f.write(f"task {key}: pass {succ}, all {alls}, accuracy {succ/alls}\n")
            except:
                pass