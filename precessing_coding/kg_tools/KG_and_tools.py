# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2018/12/31
"""从adversial中获得的API，需要用到./目录下的en文件夹"""

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

##################################################
# WordNet
##################################################
from nltk.corpus import wordnet as wn

"""两个替换操作"""
# use in wn_up
def replace_underbar(input_str): return input_str.replace('_',' ')
# use in wn_up
def replace_space(input_str): return input_str.replace(' ','_')

def wn_up  (input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  input_str = replace_space(input_str)
  results = []

  for synset in wn.synsets(input_str):
    if pos and synset.pos() != pos:
      continue
    try:
      parent = synset.hypernym_paths()[0][-2]  # 这个负二是什么时候有用的？
    except Exception as e:
      return []
    if verbose:
      print('\tPARENT:',parent,parent.min_depth())
    for l in parent.lemmas()[:max_lemmas]:
      if l.name() != input_str:
        results.append(l.name())

  results = results[:max_entities]
  return [replace_underbar(w) for w in results]

def wn_down(input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  input_str = replace_space(input_str)
  hyponyms = []
  for synset in wn.synsets(input_str):
    if pos and synset.pos() != pos:
      continue
    for s in synset.hyponyms()[:max_entities]:
      if verbose:
        print('\tHYPER:',s, s.min_depth())
      for l in s.lemmas()[:max_lemmas]:
        if l.name() != input_str:
          hyponyms.append(l.name())
  hyponyms = hyponyms[:max_entities]
  return [replace_underbar(w) for w in hyponyms]

def wn_part(input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  input_str = replace_space(input_str)
  meronyms = []
  for synset in wn.synsets(input_str):
    if pos and synset.pos() != pos:
      continue
    #print('Part_Meronyms:')
    for s in synset.part_meronyms()[:max_entities]:
      if verbose:
        print('\tMERONY:',s, s.min_depth())
      for l in s.lemmas()[:max_lemmas]:
        if l.name() != input_str:
          meronyms.append(l.name())
  meronyms = meronyms[:max_entities]
  return [replace_underbar(w) for w in meronyms]

def wn_move(input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  input_str = replace_space(input_str)
  hyponyms = []
  for synset in wn.synsets(input_str):
    if pos and synset.pos() != pos:
      continue
    # go up
    try:
      parent = synset.hypernym_paths()[0][-2]
    except Exception as e:
      return []
    parents = []
    for l in parent.lemmas()[:max_lemmas]:
      parents.append(l.name())
    # go down
    for synset2 in wn.synsets(parents[0]):
      if pos and synset2.pos() != pos:
        continue
      for s in synset2.hyponyms()[:max_entities]:
        if verbose:
          print('\tMOVE:',parent,parent.min_depth(), s, s.min_depth())
        for l in s.lemmas()[:max_lemmas]:
          if l.name() != input_str:
            hyponyms.append(l.name())
  hyponyms = hyponyms[:max_entities]
  return [replace_underbar(w) for w in hyponyms]

def wn_anto(input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  input_str = replace_space(input_str)
  antos = []
  for synset in wn.synsets(input_str):
    if pos and synset.pos() != pos:
      continue
    #print('Antonyms:')
    #print([(l.name(),l.antonyms())) for l in synset.lemmas() if len(l.antonyms())>0]
    antos = [a.name() for l in synset.lemmas()[:max_lemmas] if len(l.antonyms())>0 for a in l.antonyms() ]
  anots = [a for a in antos if a != input_str]
  antos = antos[:max_entities]
  return [replace_underbar(w) for w in antos]

def wn_syn (input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  input_str = replace_space(input_str)
  syns = []
  for synset in wn.synsets(input_str):
    if pos and synset.pos() != pos:
      continue
    for l in synset.lemmas()[:max_lemmas]:
      syns.append(l.name().lower())
  syns = list(set(syns))
  syns = [a for a in syns if a != input_str]
  syns = syns[:max_entities]
  return [replace_underbar(w) for w in syns]

# sheng_guo_wei
def wn_syn (input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  input_str = replace_space(input_str)
  syns = []
  for synset in wn.synsets(input_str):
    if pos and synset.pos() != pos:
      continue
    for l in synset.lemmas()[:max_lemmas]:
      syns.append(l.name().lower())
  syns = list(set(syns))
  syns = [a for a in syns if a != input_str]
  syns = syns[:max_entities]
  return [replace_underbar(w) for w in syns]


"""
整个过程到底是怎么样的
1.替换格式适用于wordnet的格式
2.判断词性,词性一致的继续
3.然后得到词元
4.在更改为不适用与wordnet的格式
"""





ruler = {}
ruler['wordnet'] = {
    'up'  : wn_up,
    'syn' : wn_syn,
}

def transform(sent, lhs, rhs):
  #print(str(lhs))
  #sent = str(sent)
  return sent.lower().replace(str(lhs), str(rhs))



#
#  input: a is good, output: a is NOT good

#def hand_wordNet()





#################################################
# Hand: NEGATE / SWAP / DELETE
#################################################
import spacy

# python -m spacy download en ,必须要下载才行
nlp = spacy.load('en')

# input: a is good, output: a is NOT good
# 单纯的加入负例的方法
def hand_negate(input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  nlp = spacy.load('en')
  import en_core_web_sm as en
  parsed = nlp(input_str)
  #print(parsed)
  parsed_dic = {p.dep_:p.orth_ for p in parsed}

  if 'neg' in parsed_dic:
    print('NEG detected',parsed_dic['neg'])
    return ' '.join([p.orth_ for p in parsed if p.dep_ != 'neg'])
  else:
    output_str = []
    for p in parsed:
      if p.dep_ == 'ROOT':
        if p.orth_ in ['am','is','was','were','are']:
          output_str.append(p.orth_)
          output_str.append('not')
        else:
          try:
            present = en.verb.present(p.orth_)
            if present != p.orth_:
              output_str.append('did')
            else:
              output_str.append('do')
          except Exception as e:
            print('wrong',e)
            continue
          output_str.append('not')
          output_str.append(p.orth_)
      else:
        output_str.append(p.orth_)
      #print('fake',output_str)
    return ' '.join(output_str)
# # input: a is good, output: a is NOT good
# def hand_swap(input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  # return
# # input: a is good, output: a is NOT good
# def hand_delete(input_str, pos=None, max_entities=-1, max_lemmas=-1, verbose=False):
  # return


def parse_pos(input,ruler):
      parsed       = nlp(input)
      # print(parsed)
      sentence_pos = [(token,token.pos_) for token in parsed]


      sentence_giveback = []      # 最终的返回的值

      for each_token,each_pos in sentence_pos:
          # todo: 放到了考虑下，但，更多的会因为action_ruler时，自然而然会过滤掉过程；
          if each_pos == u"VERB":
            this_pos = wn.VERB
          elif each_pos == u"NOUN":
            this_pos = wn.NOUN
          else:
            continue

          for action_type,action_rule in ruler['wordnet'].items():
            wn_result = action_rule(str(each_token), pos=this_pos, max_entities=1, max_lemmas=1)
            #print('wn_result',wn_result)
            if len(wn_result) == 0: continue
            for rhs in list(set(wn_result)):
                output = transform(input, each_token, rhs)
                if output == input: continue
                sentence_giveback.append(output)
      return sentence_giveback

# 上义词和同义词
def parse_pos_only_NOUN(input, ruler):
  parsed = nlp(input)
  # print(parsed)
  sentence_pos = [(token, token.pos_) for token in parsed]
  sentence_giveback = []  # 最终的返回的值
  for each_token, each_pos in sentence_pos:
    # todo: 放到了考虑下，但，更多的会因为action_ruler时，自然而然会过滤掉过程；
    # if each_pos == u"VERB":
    #   this_pos = wn.VERB
    # elif each_pos == u"NOUN":
    #   this_pos = wn.NOUN
    # else:
    #   continue

    if each_pos == u"NOUN":
      this_pos = wn.NOUN
    else:
      continue

    for action_type, action_rule in ruler['wordnet'].items():
      wn_result = action_rule(str(each_token), pos=this_pos, max_entities=1, max_lemmas=1)
      # print('wn_result',wn_result)
      if len(wn_result) == 0: continue
      for rhs in list(set(wn_result)):
        output = transform(input, each_token, rhs)
        if output == input: continue
        sentence_giveback.append(output)
  return sentence_giveback





if __name__ == '__main__':
    pass
    # KG_tools
    #



    ##################################################
    # WordNet
    ##################################################

    # 艹，这种东西有个屁用啊。
    #print(wn_up('pig'))
    #print(wn_up('pig',pos='v'))

    # print('fake',wn_up('pig',pos=wn['VERB']))





    #input = u"I did think that it was the complete set"

    #parsed = nlp(input)

    # print('SYN:',) wn_syn('car', pos='n', max_entities=2, max_lemmas=2, verbose=False)
    # print('UP:',) wn_up('bad weather', pos='n', max_entities=3, max_lemmas=3, verbose=False)
    # print('DOWN:',) wn_down('weather', pos='n', max_entities=3, max_lemmas=3, verbose=False)
    # print('PART:',) wn_part('tree', pos='n', max_entities=3, max_lemmas=3, verbose=False)
    # print('MOVE:',) wn_move('human', pos='n', max_entities=3, max_lemmas=3, verbose=False)
    # print('ANTO:',) wn_anto('cool down', pos='n', max_entities=3, max_lemmas=3, verbose=False)

    #################################################
    # Hand: NEGATE / SWAP / DELETE
    #################################################


    # # 思想我也是懂的，先句法分析，再词法分析


    # 最终确定下的用法
    sheng_input = u"judging from not previous pig this used to not be a good place , but not any longer"
    #[print(eachline) for eachline in parse_pos(sheng_input,ruler)]
    print('hahhah',hand_negate(sheng_input))

    #wn.synsets("dog")

    sheng_input = 'I have a spider in my burger.'
    print(parse_pos_only_NOUN(sheng_input,ruler))

    # import pdb; pdb.set_trace()
    # print([(p.dep_,) p.orth_) for p in parsed]

    # parsed_dic = {p.dep_: p.orth_ for p in parsed}
    # print('parsed_dic',parsed_dic)


    ### 句法的