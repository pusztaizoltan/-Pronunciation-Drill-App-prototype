# -*- coding: utf-8 -*-
"""
Created on Sat May  8 20:59:18 2021

@author: Z-oly
"""
import regex as re
import random
language_code ="EN"

def readtext(filename): # return raw wordlist
    try:
        data = open(filename, 'r', encoding='utf-8-sig')
        w_list = data.readlines()
    except:
        data = open(filename, 'r', encoding='ISO-8859-1')
        w_list = data.readlines()
    w_list = [line.rstrip('\n') for line in w_list]
    data.close()
    return w_list

def get_affixes(wordlist, affixtype, maxlength=5, prepared=[]):
    def stringorderer(word, affixtype=affixtype):
        if affixtype == "suffix":
            return word[::-1]
        elif affixtype == "prefix":
            return word
        else:
            return word
        
    affixset = set(prepared)
    for word in wordlist:
        for chars in range(1, maxlength +1):
            affix = stringorderer(stringorderer(word)[:chars])
            affixset.add(affix)
    return list(affixset)

def analize_affixes(wordpairs, affixes, affixtype, withaccent=False):
    def stringorderer(word, affixtype=affixtype):
        if affixtype == "suffix":
            return word[::-1]
        elif affixtype == "prefix":
            return word
        else:
            return word
    def fit_affix(word, affix, affixtype=affixtype):
        if affixtype == "suffix":
            return word.endswith(affix)
        elif affixtype == "prefix":
            return word.startswith(affix)
        else:
            return word.startswith(affix)
    if withaccent:
        wordthrees = [pair + [pair[1]] for pair in wordpairs]
    else:
        wordthrees = [pair + [pair[1].replace("ˈ","").replace("ˌ", "")] for pair in wordpairs]
    stats = [["","", 0]]
    for affix in affixes:
        affixeds = [three for three in wordthrees if fit_affix(three[0], affix)]
        phonetic_affixes = []
        for affixed in affixeds:
            for index in range(1,min(len(affix)+3, len(affixed[2])+1)):
                phonetic_affix = stringorderer(stringorderer(affixed[2])[:index])
                phonetic_affixes.append(phonetic_affix)
        
        uniques = sorted(list(set(phonetic_affixes)), key=stringorderer, reverse=True)
        for unique in uniques:
            statline = [affix, unique, phonetic_affixes.count(unique)]
        
            c0 = statline[2] == len(affixeds)
            c1 = stats[-1][0] == statline[0]
            c2 = fit_affix(stats[-1][1], statline[1])
            c3 = stats[-1][2] >= statline[2]
            if c0 and not (c1 and c2 and c3):
                stats.append(statline)

    return stats[1:]

def aggregate_affixes(affixstats, affixtype, prepared=[]):
    def stringorderer(word, affixtype=affixtype):
        if affixtype == "suffix":
            return word[::-1]
        elif affixtype == "prefix":
            return word
        else:
            return word

    prepared = [stringorderer(affix) for affix in prepared]
    temp = [[stringorderer(stat[0]), stringorderer(stat[1]), stat[2]] for stat in affixstats]
    runingcount = len(temp)

#    print ("------------------------------------------")
#    print ("----remowe redundant short affixess-------")
#    print ("------------------------------------------")
 
    temp = sorted(temp, key=lambda a : a[0], reverse=True)
    temp0 = [i[0] for i in temp]
    temp1 = [i[1] for i in temp]
    temp2 = [i[2] for i in temp]
    for i0, val in enumerate(temp0):
#        if affixtype == "prefix":
#            print (temp[i0])    

        try: temp1[i0 + 1]
        except:
            break
        c1 = temp0[i0].startswith(temp0[i0 + 1])
        c2 = temp1[i0].startswith(temp1[i0 + 1])
        c3 = temp2[i0] >= temp2[i0 + 1]
        while c1 and c2 and c3:
#            print(temp[i0 + 1], "redundant for:", temp[i0] )
            
            del temp[i0 + 1], temp0[i0 + 1], temp1[i0 + 1], temp2[i0 + 1]
            try: temp1[i0 + 1]
            except:
                break
            c1 = temp0[i0].startswith(temp0[i0 + 1])
            c2 = temp1[i0].startswith(temp1[i0 + 1])
            c3 = temp2[i0] >= temp2[i0 + 1]
    reduction = runingcount - len(temp0)
#    print("----------reduction:", reduction, len(temp0), "from:", runingcount)
    runingcount = len(temp0)
#    print("---------------------------------------")
#        
#    print ("-------------------------------------------")
#    print ("-----remove redundant long affixess--------")
#    print ("-------------------------------------------")

    temp = sorted(temp, key=lambda a : a[0], reverse=False)
    temp0 = [i[0] for i in temp]
    temp1 = [i[1] for i in temp]
    temp2 = [i[2] for i in temp]
    for i0, val in enumerate(temp0):
        if affixtype == "prefix":
            print (temp[i0])    

        lookforward = 1
        try: temp1[i0 + lookforward]
        except:
            break
        c1 = temp0[i0 + lookforward].startswith(temp0[i0])
        c2 = temp1[i0 + lookforward].startswith(temp1[i0])
        c3 = temp2[i0 + lookforward] <= 6
        c4 = temp2[i0] - temp2[i0 + lookforward] <=6
        while c1 and c2 :
            if c3 or c4:
                if affixtype == "prefix":   
                    print(temp[i0 + lookforward], "redundant for:", temp[i0] )
                #                print(temp[i0 + lookforward], "redundant for:", temp[i0] )
                del temp[i0 + lookforward], temp0[i0 + lookforward], temp1[i0 + lookforward], temp2[i0 + lookforward]
            else: lookforward +=1
            try: temp1[i0 + lookforward]
            except:
                break
            c1 = temp0[i0 + lookforward].startswith(temp0[i0])
            c2 = temp1[i0 + lookforward].startswith(temp1[i0])
            c3 = temp2[i0 + lookforward] <= 6
            c4 = temp2[i0] - temp2[i0 + lookforward] <=6
            
    reduction = runingcount - len(temp0)
#    print("----------reduction:", reduction, len(temp0), "from:", runingcount)
    runingcount = len(temp0)
    
#    print ("-------------------------------------------")
#    print ("------remowe singleton and pair patterns---")
#    print ("-------------------------------------------")
    temp = [i for i in temp if i[2] >= 3]
    temp0 = [i[0] for i in temp]
    temp1 = [i[1] for i in temp]
    temp2 = [i[2] for i in temp]
    reduction = runingcount - len(temp0)
#    print("")
#    print("----------reduction:", reduction, len(temp0), "from:", runingcount)
    runingcount = len(temp0)

    temp = [[stringorderer(stat[0]), stringorderer(stat[1]), stat[2]] for stat in temp]

    return temp

def separate_by_affix(wordpairs, affixaggregate, affixtype, withaccent=False):
    if withaccent:
        temp = wordpairs.copy()
    else:
        temp = [[pair[0]] + [pair[1].replace("ˈ","").replace("ˌ", "")] for pair in wordpairs]

    def fit_affix(word, affix, affixtype=affixtype):
        if affixtype == "suffix":
            return word.endswith(affix)
        elif affixtype == "prefix":
            return word.startswith(affix)
        else:
            return word.startswith(affix)

    affixes = sorted(affixaggregate, key=lambda a: a[2], reverse=False)
    tar = []
    for affix in affixes:
        affixeds = [pair for pair in temp if fit_affix(pair[0], affix[0]) and fit_affix(pair[1], affix[1])]
        if len(affixeds)>=3:
            temp = [pair for pair in temp if pair not in affixeds]
            affixeds = [pair[0] for pair in affixeds]
            tar.append(affixeds)
    return tar, temp

def format_to_block(llists, maxlinecontent=4):
    blocks = []
    maxchars = maxlinecontent * 8
    for llist in llists:
        result = []
        random.shuffle(llist)
        while len(llist[maxlinecontent:]) >= maxlinecontent:
            line = []
            wnum = 1
            charnum = len(llist[0])
            while wnum <= maxlinecontent and charnum <= maxchars:
                line.append(llist[0])    
                llist = llist[1:]
                wnum +=1
                charnum += len(llist[0])
            segment = " ".join(line)
            result.append(segment)
            random.shuffle(llist)
        if len(llist) <=maxlinecontent:
            random.shuffle(llist)
            result.append(" ".join(llist))
        else:
            random.shuffle(llist)
            resthalf = int(len(llist)/2)+1
            result.append(" ".join(llist[:resthalf]))
            result.append(" ".join(llist[resthalf:]))

        block = "" if len(result) == 0 else ",\n".join(result).capitalize() + "."
        blocks.append(block)
    random.shuffle(blocks)
    return "\n\n----------------------------------------\n".join(blocks)



def get_practice(wordpairs, affixtype, prepaffixes, maxlinecontent=4):
    literals = [i[0] for i in wordpairs]
    affixes = get_affixes(literals, affixtype, prepared=prepaffixes)
    affixstats = analize_affixes(wordpairs=wordpairs, affixes=affixes, affixtype=affixtype)
    affixaggregate = aggregate_affixes(affixstats, affixtype, prepared=[])
    affixeds, rest = separate_by_affix(wordpairs, affixaggregate, affixtype)
#----------shuffle add for typ practice---------
    random.shuffle(affixeds)
    temp = []
    ss = []
    i = 0
    s = 0
    while i<len(affixeds):
        if len(ss) < 70 and s < 4:
            ss.extend(affixeds[i])
            s+=1
            i+=1
        else:
            temp.append(ss)
            ss = []
            s = 0
    temp.append(ss)
    affixeds = temp
#    print(affixeds)
#------------------------------------

    formated_affixeds = format_to_block(affixeds, maxlinecontent=maxlinecontent)
    return formated_affixeds, rest, sum(len(i) for i in affixeds)


prepsuffixes = readtext(language_code + "_suffixes.txt")
prepprefixes = readtext(language_code + "_prefixes.txt")

ww = readtext('new--2.txt')
ww = [i.split("\t") for i in ww]
ll = len(ww)*(280)//(220 + 280)
random.shuffle(ww)
ww1 = ww[:ll]

les = []
formated_prefixeds1, prefrest, l = get_practice(wordpairs=ww1,
                                               affixtype="prefix", 
                                               prepaffixes=prepprefixes,
                                               maxlinecontent=6)
les.append(l)
formated_suffixeds1, suffrest, l = get_practice(wordpairs=ww1,
                                                affixtype="suffix", 
                                                prepaffixes=prepsuffixes,
                                                maxlinecontent=6)
les.append(l)

ww2 = ww[ll:] + prefrest + [i for i in suffrest if i not in prefrest]

formated_prefixeds2, prefrest, l = get_practice(wordpairs=ww2,
                                                affixtype="prefix", 
                                                prepaffixes=prepprefixes,
                                                maxlinecontent=6)
les.append(l)
formated_suffixeds2, suffrest, l = get_practice(wordpairs=ww2,
                                                affixtype="suffix", 
                                                prepaffixes=prepsuffixes,
                                                maxlinecontent=6)
les.append(l)
del l

text_file = open("_EN_prefixeds1" + '.txt', "w", encoding='utf-8-sig')
n = text_file.write(formated_prefixeds1)
text_file.close()

text_file = open("_EN_suffixeds1" + '.txt', "w", encoding='utf-8-sig')
n = text_file.write(formated_suffixeds1)
text_file.close()

text_file = open("_EN_prefixeds2" + '.txt', "w", encoding='utf-8-sig')
n = text_file.write(formated_prefixeds2)
text_file.close()

text_file = open("_EN_suffixeds2" + '.txt', "w", encoding='utf-8-sig')
n = text_file.write(formated_suffixeds2)
text_file.close()
