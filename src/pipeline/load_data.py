import json
from prompt import *

def extract_answer(answer, option):
    if option == "A":
        answer = answer.split("A")[-1].split("B")[0].split(".")[-1].strip()
    elif option == "B":
        answer = answer.split("B")[-1].split("C")[0].split(".")[-1].strip()
    elif option == "C":
        answer = answer.split("C")[-1].split("D")[0].split(".")[-1].strip()
    else:
        answer = answer.split("D")[-1].split(".")[-1].strip()
    return answer

def process_input(line, task):
    if "direction" in task:
        query = EVAL_TEMPLATE_DIR
        query = query.replace("{question}", line["question"])
        query = query.replace("{option}", line["options"])
        if "turn" in task:
            query = query.replace("{order}", "the first image is shot towards east, the second towards south, the third towards west and the fourth towards north")
        elif "-2" in task:
            query = query.replace("{order}", "four images are respectively shot towards north, east, south and west, and you only know that the first image is towards north, while the direction of other images needs to be deduced")
        else:
            query = query.replace("{order}", "the first image is shot towards north, the second towards east, the third towards south and the fourth towards west")
        
    elif "object" in task:
        query = EVAL_TEMPLATE_OBJ
        query = query.replace("{question}", line["question"])
        query = query.replace("{option}", line["options"])
        if "turn" in task:
            query = query.replace("{order}", "the first image is shot towards east, the second towards south, the third towards west and the fourth towards north")
        elif "-2" in task:
            query = query.replace("{order}", "four images are respectively shot towards north, east, south and west, and you only know that the first image is towards north, while the direction of other images needs to be deduced")
        else:
            query = query.replace("{order}", "the first image is shot towards north, the second towards east, the third towards south and the fourth towards west")

    elif "counting" in task:
        query = EVAL_TEMPLATE_CNT
        query = query.replace("{question}", line["question"])
        if "turn" in task:
            query = query.replace("{order}", "the first image is shot towards east, the second towards south, the third towards west and the fourth towards north")
        elif "-2" in task:
            query = query.replace("{order}", "four images are respectively shot towards north, east, south and west, and you only know that the first image is towards north, while the direction of other images needs to be deduced")
        else:
            query = query.replace("{order}", "the first image is shot towards north, the second towards east, the third towards south and the fourth towards west")

    elif "angle" in task:
        query = EVAL_TEMPLATE_ANG
        query = query.replace("{question}", line["question"])
        query = query.replace("{option}", line["options"])
        if "-2" in task:
            query = query.replace("{order}", "they are originally shot in the clockwise sequence and the turning angle between the adjacent images are all the same, but they are not presented in the right sequence")
        else:
            query = query.replace("{order}", "they are arranged clockwise and the turning angle between adjacent images are the same")

    elif "dif-ang" in task:
        query = EVAL_TEMPLATE_DIF_ANG
        query = query.replace("{question}", line["question"])


    elif "planning" in task:
        query = EVAL_TEMPLATE_PLA
        query = query.replace("{question_qa}", line["question-qa"])
        query = query.replace("{option_qa}", line["options-qa"])
        query = query.replace("{question_dec}", line["question-dec"])
        query = query.replace("{option_dec}", line["options-dec"])
        if "-2" in task:
            query = query.replace("{order}", "You are provided with 4 images that cover the entire surroundings, where you are facing the direction in the first image, with other three images respectively showing the scene to your right, back and left, but you do not know their sequence and it needs to be deduced")
        else:
            query = query.replace("{order}", "You are provided with 4 images that cover the entire surroundings, where you are facing the direction in the first image, with the second image showing the scene to your right, the third image showing the scene at your back, and the fourth image showing the scene to your left")

    return query

def load_data(args):
    data_list = []
    task_list = ["direction", "direction-turn", "direction-2", "object", "object-turn", "object-2", "counting", "counting-turn", "counting-2", "angle", "dif-ang", "planning", "planning-2"]

    if args.task == "all":
        for task in task_list:
            anno_path = f"{args.data_path}/anno/{task}.jsonl"
            with open(anno_path, 'r') as f:
                for line in f:
                    line = json.loads(line)
                    query = process_input(line, task)
                    line["query"] = query
                    data_list.append(line)
                    
    else:
        anno_path = f"{args.data_path}/anno/{args.task}.jsonl"
        with open(anno_path, 'r') as f:
            for line in f:
                line = json.loads(line)
                query = process_input(line, args.task)
                line["query"] = query
                data_list.append(line)

    return data_list

