from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import gluonnlp as nlp
import argparse
import os
import mxnet as mx
import json

parser = argparse.ArgumentParser(description='Comparison script for BERT model in Tensorflow'
                                             'and that in Gluon. This script works with '
                                             'google/bert@f39e881b',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_file', type=str, default='input.txt',
                    help='sample input file for testing')
parser.add_argument('--cased', action='store_true',
                    help='if not set, inputs are converted to lower case')
parser.add_argument('--gluon_dataset', type=str, default=None,
                    help='gluon dataset name')
parser.add_argument('--gluon_model', type=str, default='bert_12_768_12',
                    help='gluon model name')
parser.add_argument('--gluon_parameter_file', type=str, default=None,
                    help='gluon parameter file name.')
parser.add_argument('--gluon_vocab_file', type=str, default=None,
                    help='gluon vocab file corresponding to --gluon_parameter_file.')

args = parser.parse_args()

input_file = os.path.expanduser(args.input_file)
do_lower_case = not args.cased
max_length = 11
if not args.gluon_dataset:
    with open(args.gluon_vocab_file) as f:
        vocab_str = json.load(f)
    vocab = nlp.vocab.BERTVocab.from_json(json.dumps(vocab_str))
else:
    vocab = None
bert, vocabulary = nlp.model.get_model(args.gluon_model,
                                       dataset=args.gluon_dataset,
                                       vocab=vocab,
                                       pretrained=not args.gluon_parameter_file,
                                       use_pooler=False,
                                       use_decoder=False,
                                       use_classifier=False,
                                       output_all_encodings=True)
if args.gluon_parameter_file:
    try:
        bert.cast('float16')
        bert.load_parameters(args.gluon_parameter_file, ignore_extra=True)
        bert.cast('float32')
    except AssertionError:
        bert.cast('float32')
        bert.load_parameters(args.gluon_parameter_file, ignore_extra=True)

print(bert)
tokenizer = nlp.data.BERTTokenizer(vocabulary, lower=do_lower_case)
dataset = nlp.data.TSVDataset(input_file, field_separator=nlp.data.Splitter('|||'))

trans = nlp.data.BERTSentenceTransform(tokenizer, max_length)
dataset = dataset.transform(trans)

bert_dataloader = mx.gluon.data.DataLoader(dataset, batch_size=1,
                                           shuffle=True, last_batch='rollover')

# verify the output of the first sample
for i, seq in enumerate(bert_dataloader):
    input_ids, valid_length, type_ids = seq
    out = bert(input_ids, type_ids,
               valid_length.astype('float32'))
    length = valid_length.asscalar()
    b = [x.asnumpy().squeeze(0) for x in out]
    print(b)