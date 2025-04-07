EVAL_TEMPLATE_DIR="""You are provided with four images shot in the same scene towards different direction. These images overlap in a certain manner, and are arranged in the following order: {order}. Carefully analyze these images, and answer the following question from the given options. 
Question: {question} Options: {option}. 
You should generate your answer from 'A, B, C or D'. Your answer:"""

EVAL_TEMPLATE_OBJ="""You are provided with four images shot in the same scene towards different direction. These images overlap in a certain manner, and are arranged in the following order: {order}. Carefully analyze these images, and answer the following question from the given options. 
Question: {question} Options: {option}. 
You should generate your answer from 'A, B, C or D'. Your answer:"""

EVAL_TEMPLATE_CNT="""You are provided with four images shot in the same scene towards different direction. These images overlap in a certain manner, and are arranged in the following order: {order}. Carefully analyze these images, and answer the following question. 
Question: {question}
You should generate a single number as your answer. Your answer:"""

EVAL_TEMPLATE_ANG="""You are provided with four images shot in the same scene. They are taken from the same position but towards different directions. For example, after taking the first image, the photographer turns a certain degree clockwise. These images are arranged the same sequence they are shot and the turning angle between adjacent images are the same. Also note that the image sequence does not always cover a full 360-degree scene.
Carefully analyze these images, and answer the following question from the given options. 
Question: {question} Options: {option}.
You should generate your answer from 'A or B'. Your answer:"""

EVAL_TEMPLATE_DIF_ANG="""You are provided with five images shot in the same scene at the same position towards different directions. In these five images, four are taken in the following way: after taking the first image, the photographer turns a certain degree clockwise to take the next one and the degree always remains the same. These images are also arranged as the sequence they are taken. However, the rest one image is shot towards totally different direction and is randomly inserted into the image sequence.
Question: {question}
You should generate a single number as your answer, where 1 represents the first image and 5 represents the last image. Your answer:"""

EVAL_TEMPLATE_PLA="""You are a human like robot. You can only go straight ahead If you want to walk in the other direction, you need to first turn to the target direction and then move forward. {order}.
There are two questions for you to answer at the same time. Please carefully analysis your surroundings and answer the following quesitons:
Question 1: {question_qa} Options: {option_qa}.
Question 2: {question_dec} Options: {option_dec}.
You should generate your answer in a json dict containing 2 fields:
```json
{
  'Answer1': type str, answer to quesiton 1, in the form of 'A', 'B', 'C' or 'D', 
  'Answer2': type str, answer to quesiton 2, in the form of 'A', 'B', 'C' or 'D'.
}
```
Your response:"""
