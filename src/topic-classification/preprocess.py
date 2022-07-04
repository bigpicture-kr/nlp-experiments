import os
import json
import argparse
from collections import OrderedDict
from tqdm import tqdm

def data_to_json(data):
    file_data = OrderedDict()
    file_data['chars'] = list(data)
    print(json.dumps(file_data, ensure_ascii=False))

    with open('rr.json', 'w', encoding='utf-8') as file:
        json.dump(file_data, file, ensure_ascii=False)

def get_every_filename():
    filenames = []

    for i in range(1, 10):
        filenames.append('NIRW190000000' + str(i))
    for i in range(10, 31):
        filenames.append('NIRW19000000' + str(i))
    
    for i in range(1, 10):
        filenames.append('NLRW190000000' + str(i))
    for i in range(10, 100):
        filenames.append('NLRW19000000' + str(i))
    for i in range(100, 162):
        filenames.append('NLRW1900000' + str(i))

    for i in range(1, 10):
        filenames.append('NPRW190000000' + str(i))
    for i in range(10, 71):
        filenames.append('NPRW19000000' + str(i))

    for i in range(1, 10):
        filenames.append('NWRW190000000' + str(i))
    for i in range(10, 61):
        filenames.append('NWRW19000000' + str(i))

    filenames.append('NZRW1900000001')
    return filenames

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', type=str, required=True, default=None)
    parser.add_argument('--out_dir', type=str, required=True, default=None)
    parser.add_argument('--train_data_size', type=int, default=500)
    parser.add_argument('--validation_data_size', type=int, default=50)
    args = parser.parse_args()

    topic = {
        '정치': 'politic',
        '경제': 'economy',
        '사회': 'social',
        '생활': 'life',
        'IT/과학': 'ITscience',
        '연예': 'entertainment',
        '스포츠': 'sport',
        '문화': 'culture',
        '미용/건강': 'health'
    }

    filenames = get_every_filename()
    sample_type = {v: 'train' for v in topic.values()}
    train_samples_sizes = {v: 0 for v in topic.values()}
    valid_samples_sizes = {v: 0 for v in topic.values()}

    for filename in tqdm(filenames):
        #print(f'{filename} is running...')

        with open(f'{args.in_dir}/{filename}.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        for news_idx in range(len(json_data['document'])):
            news_data = json_data['document'][news_idx]
            id = news_data['id'].replace('.', '_')
            topic_eng = topic[news_data['metadata']['topic']]

            # Sampling a specific number of data for each label
            if sample_type[topic_eng] == 'train' and train_samples_sizes[topic_eng] >= args.train_data_size:
                sample_type[topic_eng] = 'validation'
            elif sample_type[topic_eng] == 'validation' and valid_samples_sizes[topic_eng] >= args.validation_data_size:
                continue
            if sample_type[topic_eng] == 'train':
                train_samples_sizes[topic_eng] += 1
            elif sample_type[topic_eng] == 'validation':
                valid_samples_sizes[topic_eng] += 1

            content = ''
            for line in news_data['paragraph']:
                content += (line['form'] + '\n')
            
            #print('id: ', id)
            #print('topic: ', topic_eng)
            #print('content: ', content)

            output_path = f'{args.out_dir}/{sample_type[topic_eng]}/{topic_eng}/{id}.txt'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(content)
