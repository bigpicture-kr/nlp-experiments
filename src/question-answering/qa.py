import torch
from transformers import BertConfig, BertForQuestionAnswering, BertTokenizer
from ivete.deploy import DeployArguments, deploy

args = DeployArguments(
    pretrained_model_name="beomi/kcbert-base",
    downstream_model_path="./checkpoints/",
    inference_args={
        'max_seq_length': 128,
        'max_query_length': 32,
    }
)

checkpoint = torch.load(
    args.downstream_model_path, 
    map_location=torch.device("cpu"),
)

pretrained_model_config = BertConfig.from_pretrained(
    args.pretrained_model_name
)
model = BertForQuestionAnswering(pretrained_model_config)

model.load_state_dict({k.replace("model.", ""): v for k, v in checkpoint['state_dict'].items()})

model.eval()

tokenizer = BertTokenizer.from_pretrained(
    args.pretrained_model_name,
    do_lower_case=False,
)

def inference(question: str, context: str):
    if question and context:
        truncated_query = tokenizer.encode(
            question,
            add_special_tokens=False,
            truncation=True,
            max_length=args.inference_args['max_query_length'],
       )
        inputs = tokenizer.encode_plus(
            text=truncated_query,
            text_pair=context,
            truncation="only_second",
            padding="max_length",
            max_length=args.inference_args['max_seq_length'],
            return_token_type_ids=True,
        )
        with torch.no_grad():
            outputs = model(**{k: torch.tensor([v]) for k, v in inputs.items()})
            start_pred = outputs.start_logits.argmax(dim=-1).item()
            end_pred = outputs.end_logits.argmax(dim=-1).item()
            pred_text = tokenizer.decode(inputs['input_ids'][start_pred:end_pred+1])
    else:
        pred_text = ""
    return {
        'question': question,
        'context': context,
        'answer': pred_text,
        'output': pred_text,
    }

app = deploy(
    inference=inference,
    api_name="qa",
)
app.run()
