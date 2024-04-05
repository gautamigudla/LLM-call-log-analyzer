from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch

# Paths to your local model and tokenizer directories
model_dir = '/Users/gautami/Desktop/Gautami/Job/Cleric Project/AWS_LLM/model'
tokenizer_dir = '/Users/gautami/Desktop/Gautami/Job/Cleric Project/AWS_LLM/tokenizer'

# Load the model and tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)

def answer_question(question, context):
    """
    Takes a question and context; returns the model's answer.
    """
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    # Find the most probable answer span
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    # Get the answer tokens and convert them to a string
    answer_tokens = input_ids[answer_start:answer_end]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)

    # Sometimes the answer is empty, in such cases, return None
    if not answer:
        return None
    
    return answer
