# -*- coding: utf-8 -*-
from itertools import product
from itertools import permutations
import Korean
import nlp
import we

#####
# 유사 질의 확장
# 1. 동의어 확장
# 2. we 확장
# 3. 어미 다변화
# 4. 어순 도치 확장
#####

### 원문(txt) 가져오기 ###
origin_utter = list()
f = open("test.txt", "r")
lines = f.readlines()
for line in lines:
    if line != '\n':
        origin_utter.append(line.replace('\n', ''))
f.close()

### 동의어사전(tsv) 가져오기 ###
# 비밀번호	비번, 패스워드
syn_dict = dict()
f = open("syn_dict.tsv", "r")
lines = f.readlines()
for line in lines:
    if line != '\n':
        syn_dict_values = line.split('\t')[1].replace('\n', '')
        syn_dict[line.split('\t')[0]] = syn_dict_values.split(', ')
f.close()

### 어미다변화사전(tsv) 가져오기 ###
# 해줘	해줘라, 해줄래, 해봐
eowrd_dict = dict()
f = open("eowrd_dict.tsv", "r")
lines = f.readlines()
for line in lines:
    if line != '\n':
        eowrd_dict_values = line.split('\t')[1].replace('\n', '')
        eowrd_dict[line.split('\t')[0]] = eowrd_dict_values.split(', ')
f.close()

### 1. 동의어 확장 ###
pro_utter = list()

# 동의어 변환 딕셔너리 저장
# utter_syn_dict = {"a는 b입니까": [["a", "a1"], ["b", "b1"]]...}
utter_syn_dict = dict()
for utter in origin_utter:
    for syn_dict_key in syn_dict.keys():
        # 동의어 발견
        if utter.find(syn_dict_key) > -1:
            # 이미 utter_syn_dict가 추가되어 있을 경우
            if utter_syn_dict.get(utter):
                # 임시의 리스트에 대표어 저장
                temp_list = [syn_dict_key]
                # 임시의 리스트에 동의어 저장 후 dict에 저장
                for syn_value in syn_dict[syn_dict_key]:
                    temp_list.append(syn_value)
                utter_syn_dict[utter].append(temp_list)
                utter_syn_dict[utter] = utter_syn_dict[utter]
            else:
                # 임시의 리스트에 대표어 저장
                temp_list = [syn_dict_key]
                # 임시의 리스트에 동의어 저장 후 dict에 저장
                for syn_value in syn_dict[syn_dict_key]:
                    temp_list.append(syn_value)
                utter_syn_dict[utter] = [temp_list]

# 동의어 변환 과정
for utter in utter_syn_dict.keys():
    # 동의어의 조합이 있을 경우
    if len(utter_syn_dict[utter]) > 1:
        # product_list에 동의어의 조합 관리
        product_list = list(product(*utter_syn_dict[utter]))
        i = 0
        while i < len(product_list):
            temp_utter = utter
            o = 0
            while o < len(product_list[i]):
                find_cnt = temp_utter.count(product_list[0][o])
                phoneme = Korean.Korean(unicode(product_list[i][o])[-1:]) 
                # 동의어 변환
                temp_utter = temp_utter.replace(
                    product_list[0][o], product_list[i][o], find_cnt)
                
                try:
                    # 종성이 있는 경우 (비문 처리)
                    if phoneme[0].phoneme_coda: 
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"는", product_list[i][o]+"은", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"가", product_list[i][o]+"이", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"를", product_list[i][o]+"을", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"와", product_list[i][o]+"과", find_cnt)
                    # 종성이 없는 경우 (비문 처리)
                    else:
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"은", product_list[i][o]+"는", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"이", product_list[i][o]+"가", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"을", product_list[i][o]+"를", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"과", product_list[i][o]+"와", find_cnt)
                except:
                    pass
                o += 1
            pro_utter.append(temp_utter)
            i += 1
    # 동의어의 조합이 없을 경우
    else:
        for rep_value in utter_syn_dict[utter][0]:
            find_cnt = utter.count(utter_syn_dict[utter][0][0])
            phoneme = Korean.Korean(unicode(rep_value)[-1:])

            # 동의어 변환
            temp_utter = utter.replace(
                utter_syn_dict[utter][0][0], rep_value, find_cnt)
          
            try:
                # 종성이 있는 경우 (비문 처리)
                if phoneme[0].phoneme_coda:
                    temp_utter = temp_utter.replace(
                        rep_value+"는", rep_value+"은", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"가", rep_value+"이", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"를", rep_value+"을", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"와", rep_value+"과", find_cnt)
                # 종성이 없는 경우 (비문 처리)
                else:
                    temp_utter = temp_utter.replace(
                        rep_value+"은", rep_value+"는", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"이", rep_value+"가", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"을", rep_value+"를", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"과", rep_value+"와", find_cnt)
            except:
                pass

            pro_utter.append(temp_utter)

# 완성된 리스트의 중복 제거
#for utter in list(set(pro_utter)):
#    print utter

### 어미 다변화 ###
pro_utter = list()

for utter in origin_utter:
    pro_utter.append(utter)
    for eowrd_dict_key in eowrd_dict.keys():
        if utter.find(eowrd_dict_key) == len(utter) - len(eowrd_dict_key):
            for eowrd_value in eowrd_dict[eowrd_dict_key]:
                pro_utter.append(utter.replace(eowrd_dict_key, eowrd_value))

#for utter in list(set(pro_utter)):
    #print utter

### 문장 도치 ###
pro_utter = list()
nlp_client = nlp.NlpClient()

for utter in origin_utter:
    split_list = utter.split(' ')
    split_permu = list(permutations(split_list))
    for permu in split_permu:
        temp_utter = str()
        for permu_value in permu:
            temp_utter += permu_value  + ' '
        print "--------------"
        print temp_utter
        for typeee in nlp_client.morp_analyze(temp_utter):
            print typeee['lemma'], typeee['type']
        print "---------------"
        #print nlp_client.morp_analyze(utter)
        #print temp_utter

### word embedding ###
pro_utter = list()

nlp_client = nlp.NlpClient()
we_client = we.WordEmbeddingAnalysis()

utter_we_dict = dict()

for utter in origin_utter:
    morp_analyze = nlp_client.morp_analyze(utter)
    for morp in morp_analyze:
        if morp['type'] == 'nc':
            we_results = we_client.get_word_embedding_result(morp['lemma'])
            if we_results:
                if utter_we_dict.get(utter):
                    temp_list = [morp['lemma']]
                    for we_result in we_results:
                        temp_list.append(we_result)
                    utter_we_dict[utter].append(temp_list)
                    utter_we_dict[utter] = utter_we_dict[utter]
                else:
                    temp_list = [morp['lemma']]
                    for we_result in we_results:
                        temp_list.append(we_result)
                    utter_we_dict[utter] = [temp_list]
            else:
                pro_utter.append(utter)

for utter in utter_we_dict.keys():
    if len(utter_we_dict[utter]) > 1:
        product_list = list(product(*utter_we_dict[utter]))
        i = 0 
        while i < len(product_list):
            temp_utter = utter
            o = 0
            while o < len(product_list[i]):
                find_cnt = temp_utter.count(product_list[0][o])
                phoneme = Korean.Korean(unicode(product_list[i][o])[-1:])

                # 동의어 변환 
                temp_utter = temp_utter.replace(
                    product_list[0][o], product_list[i][o], find_cnt)

                try:
                    # 종성이 있는 경우 (비문 처리)
                    if phoneme[0].phoneme_coda:
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"는", product_list[i][o]+"은", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"가", product_list[i][o]+"이", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"를", product_list[i][o]+"을", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"와", product_list[i][o]+"과", find_cnt)
                    # 종성이 없는 경우 (비문 처리)
                    else:
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"은", product_list[i][o]+"는", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"이", product_list[i][o]+"가", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"을", product_list[i][o]+"를", find_cnt)
                        temp_utter = temp_utter.replace(
                            product_list[i][o]+"과", product_list[i][o]+"와", find_cnt)
                except:
                    pass
                o += 1
            pro_utter.append(temp_utter)
            i += 1
    else:
        for rep_value in utter_we_dict[utter][0]:
            find_cnt = utter.count(utter_we_dict[utter][0][0])
            phoneme = Korean.Korean(unicode(rep_value)[-1:])
            
            # 동의어 변환 
            temp_utter = utter.replace(
                utter_we_dict[utter][0][0], rep_value, find_cnt)

            try:
                # 종성이 있는 경우 (비문 처리)
                if phoneme[0].phoneme_coda:
                    temp_utter = temp_utter.replace(
                        rep_value+"는", rep_value+"은", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"가", rep_value+"이", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"를", rep_value+"을", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"와", rep_value+"과", find_cnt)
                # 종성이 없는 경우 (비문 처리)
                else:
                    temp_utter = temp_utter.replace(
                        rep_value+"은", rep_value+"는", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"이", rep_value+"가", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"을", rep_value+"를", find_cnt)
                    temp_utter = temp_utter.replace(
                        rep_value+"과", rep_value+"와", find_cnt)
            except:
                pass

            pro_utter.append(temp_utter)

#for utter in list(set(pro_utter)):
#    print utter

