import os
import csv
from glob import glob
from tqdm import tqdm
from minsu.nlp.generation.corpus import logger, GenerationExample

class JjaltoonCorpus:
    def __init__(self, normalizer):
        pass

    def _read_corpus(cls, input_file, quotechar='"'):
        with open(input_file, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file, delimiter=",", quotechar=quotechar))
    
    def _create_examples(self, lines):
        examples = []
        for i, line in enumerate(lines):
            if i == 0:
                continue
            text = line['speech']
            examples.append(GenerationExample(text=text))
        return examples
    
    def get_examples(self, data_root_path, mode):
        data_flist = []
        pattern = '*.csv'
        for dir, _, _ in os.walk(data_root_path):
            data_flist.extend(glob(os.path.join(dir, pattern)))
        
        if len(data_flist) == 0:
            raise FileNotFoundError(f"data file does not exist in {data_root_path}")
        
        examples = []
        for data_fpath in tqdm(data_flist, desc=f"loading {mode} data"):
            logger.info(f"loading {mode} data... LOOKING AT {data_fpath}")
            examples += self._create_examples(self._read_corpus(data_fpath))
        
        return examples
