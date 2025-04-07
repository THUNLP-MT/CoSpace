import json
import os
import random

for file in os.listdir('../anno_final'):
    if file in ["direction.jsonl", "object.jsonl", "counting.jsonl", "angle.jsonl", "dif-ang.jsonl", "planning.jsonl"]:
        if file == "direction.jsonl":
            data = []
            with open("./direction.jsonl", 'r') as f:
                for line in f:
                    data.append(json.loads(line)) 
            data_2 = []
            with open("./direction-2.jsonl", 'r') as f:
                for line in f:
                    data_2.append(json.loads(line))
            total_accuracy_q = 0
            total_accuracy_p = 0
            for _ in range(100):
                correct = 0
                correct_both = 0
                for item in data:
                    options = ['A', 'B', 'C', 'D']
                    random_answer_1 = random.choice(options)
                    random_answer_2 = random.choice(options)
                    if random_answer_1 == item['answer']:
                        correct += 1
                    if random_answer_2 == item['answer']:
                        correct += 1
                    if random_answer_1 == item['answer'] and random_answer_2 == item['answer']:
                        correct_both += 1
                accuracy = correct / (len(data) * 2)
                accuracy_both = correct_both / len(data)
                total_accuracy_q += accuracy
                total_accuracy_p += accuracy_both
            average_accuracy_q = total_accuracy_q * 100 / 100
            average_accuracy_p = total_accuracy_p * 100 / 100
            print(f"Average accuracy for {file}: {average_accuracy_q:.2f}, {average_accuracy_p:.2f}")
        elif file == "object.jsonl":
            data = []
            with open("./object.jsonl", 'r') as f:
                for line in f:
                    data.append(json.loads(line)) 
            data_2 = []
            with open("./object-2.jsonl", 'r') as f:
                for line in f:
                    data_2.append(json.loads(line))
            total_accuracy_q = 0
            total_accuracy_p = 0
            for _ in range(100):
                correct = 0
                correct_both = 0
                for item in data:
                    options = ['A', 'B', 'C', 'D']
                    random_answer_1 = random.choice(options)
                    random_answer_2 = random.choice(options)
                    if random_answer_1 == item['answer']:
                        correct += 1
                    if random_answer_2 == item['answer']:
                        correct += 1
                    if random_answer_1 == item['answer'] and random_answer_2 == item['answer']:
                        correct_both += 1
                accuracy = correct / (len(data) * 2)
                accuracy_both = correct_both / len(data)
                total_accuracy_q += accuracy
                total_accuracy_p += accuracy_both
            average_accuracy_q = total_accuracy_q * 100 / 100
            average_accuracy_p = total_accuracy_p * 100 / 100
            print(f"Average accuracy for {file}: {average_accuracy_q:.2f}, {average_accuracy_p:.2f}")
        elif file == "counting.jsonl":
            data = []
            with open("./counting.jsonl", 'r') as f:
                for line in f:
                    data.append(json.loads(line)) 
            data_2 = []
            with open("./counting-2.jsonl", 'r') as f:
                for line in f:
                    data_2.append(json.loads(line))
            total_accuracy_q = 0
            total_accuracy_p = 0
            for _ in range(100):
                correct = 0
                correct_both = 0
                for item in data:
                    options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
                    random_answer_1 = random.choice(options)
                    random_answer_2 = random.choice(options)
                    if random_answer_1 == item['answer']:
                        correct += 1
                    if random_answer_2 == item['answer']:
                        correct += 1
                    if random_answer_1 == item['answer'] and random_answer_2 == item['answer']:
                        correct_both += 1
                accuracy = correct / (len(data) * 2)
                accuracy_both = correct_both / len(data)
                total_accuracy_q += accuracy
                total_accuracy_p += accuracy_both
            average_accuracy_q = total_accuracy_q * 100 / 100
            average_accuracy_p = total_accuracy_p * 100 / 100
            print(f"Average accuracy for {file}: {average_accuracy_q:.2f}, {average_accuracy_p:.2f}")
        elif file == "angle.jsonl":
            data = []
            with open("./angle.jsonl", 'r') as f:
                for line in f:
                    data.append(json.loads(line)) 
            total_accuracy = 0
            for _ in range(100):
                correct = 0
                for item in data:
                    options = ['A', 'B']
                    random_answer = random.choice(options)
                    if random_answer == item['answer']:
                        correct += 1
                accuracy = correct / len(data)
                total_accuracy += accuracy
            average_accuracy = total_accuracy * 100 / 100
            print(f"Average accuracy for {file}: {average_accuracy:.2f}")
        elif file == "dif-ang.jsonl":
            data = []
            with open("./dif-ang.jsonl", 'r') as f:
                for line in f:
                    data.append(json.loads(line)) 
            total_accuracy = 0
            for _ in range(100):
                correct = 0
                for item in data:
                    options = ['1', '2', '3', '4', '5']
                    random_answer = random.choice(options)
                    if random_answer == item['answer']:
                        correct += 1
                accuracy = correct / len(data)
                total_accuracy += accuracy
            average_accuracy = total_accuracy * 100 / 100
            print(f"Average accuracy for {file}: {average_accuracy:.2f}")
        elif file == "planning.jsonl":
            data = []
            with open("./planning.jsonl", 'r') as f:
                for line in f:
                    data.append(json.loads(line)) 
            total_accuracy_qa = 0
            total_accuracy_dec = 0
            for _ in range(100):
                correct_qa = 0
                correct_dec = 0
                for item in data:
                    options = ['A', 'B', 'C', 'D']
                    random_answer_qa = random.choice(options)
                    random_answer_dec = random.choice(options)
                    if random_answer_qa == item['answer-qa']:
                        correct_qa += 1
                    if random_answer_dec == item['answer-dec']:
                        correct_dec += 1
                accuracy_qa = correct_qa / len(data)
                accuracy_dec = correct_dec / len(data)
                total_accuracy_qa += accuracy_qa
                total_accuracy_dec += accuracy_dec
            average_accuracy_qa = total_accuracy_qa * 100 / 100
            average_accuracy_dec = total_accuracy_dec * 100 / 100
            print(f"Average accuracy for {file}: {average_accuracy_qa:.2f}, {average_accuracy_dec:.2f}")