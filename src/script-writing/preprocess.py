import os
import argparse
import docx
import csv
from pororo import Pororo
from glob import glob
from tqdm import tqdm

def parse_paragraph(index, metadata, paragraph, sentiment_model):
    row = {
        **metadata,
        'type': 'nouse',
        'speaker': 'none',
        'raw_speech': paragraph,
        'speech': paragraph,
        'sentiment': 'neural',
        'sentiment_positive': 0.0,
        'sentiment_negative': 0.0,
        'emotion': 'none',
        'emotion_intensity': 0
    }

    if ':' in paragraph:
        row['type'] = 'speech'
        row['speaker'], row['speech'] = paragraph.split(':', 1)
    elif index == 0:
        row['script_title'] = paragraph
        metadata['script_title'] = paragraph
    
    if row['type'] == 'speech':
        sentiment = sentiment_model(row['speech'], show_probs=True)
        row['sentiment'] = 'positive' if sentiment['positive'] >= 0.5 else 'negative'
        row['sentiment_positive'] = sentiment['positive']
        row['sentiment_negative'] = sentiment['negative']
    
    row = {x: str(row[x]).strip() for x in row.keys()}
    return row

def build_corpus(filepath, sentiment_model):
    doc = docx.Document(filepath)
    data = []
    metadata = {
        'series': '',
        'script_no': '',
        'script_title': ''
    }

    for i, paragraph in enumerate(doc.paragraphs):
        if len(paragraph.text.strip()) == 0:
            # 빈 행인 경우
            continue
        elif paragraph.text.count('/')+1 == paragraph.text.count(':') and paragraph.text.count('/') >= 1:
            # 한 행에 여러 대사가 존재하는 경우
            subparagraphs = paragraph.text.split('/')
            for subparagraph in subparagraphs:
                data.append(parse_paragraph(i, metadata, subparagraph, sentiment_model))
        else:
            data.append(parse_paragraph(i, metadata, paragraph.text, sentiment_model))
    
    return data

def get_filelist(dataset_path):
    filelist = []
    pattern = '*.docx'

    for dir, _, _ in os.walk(dataset_path):
        filelist.extend(glob(os.path.join(dir, pattern)))
    
    return filelist

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', type=str, required=True, default=None)
    parser.add_argument('--out_file', type=str, required=True, default=None)
    args = parser.parse_args()
    
    sentiment_model = Pororo(task='sentiment', model='brainbert.base.ko.nsmc', lang='ko')

    filelist = get_filelist(args.in_dir)
    datalist = []
    fieldnames = None
    for input_path in tqdm(filelist):
        data = build_corpus(input_path, sentiment_model)
        datalist.append(data[1:])
        if fieldnames == None:
            fieldnames = list(data[0].keys())
    
    os.makedirs(os.path.dirname(args.out_file), exist_ok=True)
    with open(args.out_file, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in datalist:
            writer.writerows(data)
