# NLP Experiments
This repository contains several experiments with transformer based language models.
All experiments in this are being conducted exclusively by the [Bigpicture Team](http://bigpicture.team) and were funded by the [Ministry of SMEs and Startups](https://www.mss.go.kr).

## Contents

### 1. [Topic Classification](https://github.com/bigpicture-kr/nlp-experiments/blob/master/src/topic-classification/NewsTopicClassification.ipynb)

<p align="center">
  <img src="https://user-images.githubusercontent.com/9818523/175227722-e8b503fd-c957-4c9b-ac3b-ef259ca73469.png" />
</p>

This is a fine-tuned model to classify news articles into 9 topics - ITscience, culture, economy, entertainment, health, life, politic, social, sport.

It varies by topic, but shows up to 96% classification accuracy.

### 2. [Sequence Generation](https://github.com/bigpicture-kr/nlp-experiments/tree/master/src/script-writing)

This model has been fine-tuned with 130 [Jjaltoon](https://www.youtube.com/c/%EC%A7%A4%ED%88%B01) scripts.

It takes a short text as input and generates the rest of the sequence.

#### Examples

```
> 아니
아니 그게 뭔 개소리야!
```

```
> 민수
민수에게 헥토파스칼킥, 이후 파운딩) 개새끼야!
```

```
> 인공지능
인공지능 대체 왜... (고개를 확 들며 울먹이며) 남친도 있으면서 대체 왜 나한테 그렇게 이쁘게 웃어줬냐고!!!
```

### 3. [Question and Answering](https://github.com/bigpicture-kr/nlp-experiments/blob/master/src/question-answering/qa.ipynb)

This experiment is to find an answer to a question within a given context. The purpose of this experiment is to verify that answer can be predicted from unstructured natural language documents.
The future works in this Q&A experiment involves finding answer in web documents.

The model used in this experiment is a fine-tuned [KcBERT](https://github.com/Beomi/KcBERT) model using [MiNSU](https://github.com/bigpicture-kr/MiNSU). This can be implemented as a web interface for inference via [ivete](https://github.com/bigpicture-kr/ivete).

#### Examples

```
Preparing...
```
