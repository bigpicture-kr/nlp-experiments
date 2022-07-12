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
        row['sentiment'] = sentiment_model(row['speech']).lower()
    
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
    parser.add_argument('--out_dir', type=str, required=True, default=None)
    args = parser.parse_args()
    
    sentiment_model = Pororo(task="sentiment", model="brainbert.base.ko.nsmc", lang="ko")

    filelist = get_filelist(args.in_dir)
    for input_path in tqdm(filelist):
        data = build_corpus(input_path, sentiment_model)
        filename = os.path.splitext(os.path.basename(input_path))[0] + '.csv'
        output_path = os.path.join(args.out_dir, filename)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
