import requests
import string
import dict_util

COLLEGIATE_DICT_API_KEY, COLLEGIATE_THES_API_KEY = dict_util.get_api_keys()


def search_thesaurus(word):
    word = word.lower()
    dictionary = requests.get(f'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={COLLEGIATE_THES_API_KEY}').json()
    # word matched in dictionary (perhaps more than one)
    word_dicts = []
    exact_word_found = False
    try:
        for each_word in dictionary:
            if dict_util.del_non_alpha_endings(each_word['meta']['id']) == word:
                exact_word_found = True
                word_dicts.append(each_word)
    except TypeError:
        return None

    if not exact_word_found:
        word_dicts.append(dictionary[0])

    # descriptions consist of description (result we get from word)
    descriptions = []
    for word_dict in word_dicts:
        description = {}
        if exact_word_found:
            description['word'] = word
        else:
            description['word'] = word_dict['meta']['id'] 
        
        # part-of-speech
        description['pos'] = word_dict['fl']
        # stems (similar words) (list)
        description['stems'] = word_dict['meta']['stems'] 
        # meanings (all meanings summary) (list)
        description['all_meanings'] = []
        for meaning in word_dict['shortdef']:
            description['all_meanings'].append(dict_util.manage_braces(meaning))
        # definitions (meaning,example,syn,ant) (list)
        description['definitions'] = []
        for divider in word_dict['def']:
            verb_divider = ''
            if 'vd' in divider:
                verb_divider = divider['vd']
            for sense_seq in divider['sseq']:
                for sense in sense_seq:
                    if sense[0] != 'sense': continue
                    sense = sense[1]
                    definition = {}
                    definition['verb_divider'] = verb_divider

                    definition['categories'] = []
                    if 'sls' in sense:
                        definition['categories'] = sense['sls']
                    
                    definition['examples'] = []
                    for dt_element in sense['dt']:
                        if dt_element[0] == 'text':
                            definition['meaning'] = dict_util.manage_braces(dt_element[1])
                        elif dt_element[0] == 'vis':
                            for ex in dt_element[1]:
                                definition['examples'].append(dict_util.manage_braces(ex['t']))

                    definition['synonyms'] = []
                    if 'syn_list' in sense:
                        for syn_group in sense['syn_list']:
                            for syn in syn_group:
                                synonym = syn['wd']
                                if 'wvrs' in syn:
                                    for sub_word in syn['wvrs']:
                                        synonym += '/' + sub_word['wva'] 
                                if 'wvbvrs' in syn:
                                    for sub_word in syn['wvbvrs']:
                                        synonym += '/' + sub_word['wvbva'] 
                                definition['synonyms'].append(synonym)
                    if 'sim_list' in sense:            
                        for sim_group in sense['sim_list']:
                            for sim in sim_group:
                                synonym = sim['wd']
                                if 'wvrs' in sim:
                                    for sub_word in sim['wvrs']:
                                        synonym += '/' + sub_word['wva'] 
                                if 'wvbvrs' in sim:
                                    for sub_word in sim['wvbvrs']:
                                        synonym += '/' + sub_word['wvbva'] 
                                definition['synonyms'].append(synonym)

                    definition['synonymous_phrases'] = []
                    if 'phrase_list' in sense:
                        for phr_group in sense['phrase_list']:
                            for phr in phr_group:
                                synonymous_phrase = phr['wd']
                                if 'wvbvrs' in phr:
                                    for sub_word in phr['wvbvrs']:
                                        synonymous_phrase += '/' + sub_word['wvbva'] 
                                definition['synonymous_phrases'].append(synonymous_phrase)

                    definition['antonyms'] = []
                    if 'ant_list' in sense:
                        for ant_group in sense['ant_list']:
                            for ant in ant_group:
                                antonym = ant['wd']
                                if 'wvrs' in ant:
                                    for sub_word in ant['wvrs']:
                                        antonym += '/' + sub_word['wva'] 
                                if 'wvbvrs' in ant:
                                    for sub_word in ant['wvbvrs']:
                                        antonym += '/' + sub_word['wvbva'] 
                                definition['antonyms'].append(antonym)
                    if 'opp_list' in sense:
                        for opp_group in sense['opp_list']:
                            for opp in opp_group:
                                antonym = opp['wd']
                                if 'wvrs' in opp:
                                    for sub_word in opp['wvrs']:
                                        antonym += '/' + sub_word['wva'] 
                                if 'wvbvrs' in opp:
                                    for sub_word in opp['wvbvrs']:
                                        antonym += '/' + sub_word['wvbva'] 
                                definition['antonyms'].append(antonym)
                    if 'near_list' in sense:
                        for near_group in sense['near_list']:
                            for near in near_group:
                                near_antonym = near['wd']
                                if 'wvrs' in near:
                                    for sub_word in near['wvrs']:
                                        near_antonym += '/' + sub_word['wva'] 
                                if 'wvbvrs' in near:
                                    for sub_word in near['wvbvrs']:
                                        near_antonym += '/' + sub_word['wvbva'] 
                                definition['antonyms'].append(near_antonym)
                    
                    if definition['meaning'] != '': description['definitions'].append(definition)
       
        descriptions.append(description)
    
    return descriptions


def search_dictionary(word):
    word = word.lower()
    dictionary = requests.get(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={COLLEGIATE_DICT_API_KEY}').json()
    # word matched in dictionary (perhaps more than one)
    word_dicts = []
    exact_word_found = False
    try:
        for each_word in dictionary:
            if dict_util.del_non_alpha_endings(each_word['meta']['id']) == word:
                exact_word_found = True
                word_dicts.append(each_word)
    except TypeError:
        return None

    if not exact_word_found:
        word_dicts.append(dictionary[0])

    # descriptions consist of description (result we get from word)
    descriptions = []
    for word_dict in word_dicts:
        description = {}
        if exact_word_found:
            description['word'] = word
        else:
            description['word'] = word_dict['meta']['id'] 
        
        # part-of-speech
        description['pos'] = word_dict['fl']
        # stems (similar words) (list)
        description['stems'] = word_dict['meta']['stems'] 
        # meanings (all meanings summary) (list)
        description['all_meanings'] = []
        for meaning in word_dict['shortdef']:
            description['all_meanings'].append(dict_util.manage_braces(meaning))
        # definitions (meaning,example,syn,ant) (list)
        description['definitions'] = []
        for divider in word_dict['def']:
            verb_divider = ''
            if 'vd' in divider:
                verb_divider = divider['vd']
            for sense_seq in divider['sseq']:
                for sense in sense_seq:
                    if sense[0] != 'sense': continue
                    sense = sense[1]
                    
                    definition = {}
                    definition['verb_divider'] = verb_divider

                    definition['categories'] = []
                    if 'sls' in sense:
                        definition['categories'] = sense['sls']
                    
                    definition['examples'] = []
                    for dt_element in sense['dt']:
                        if dt_element[0] == 'text':
                            definition['meaning'] = dict_util.manage_braces(dt_element[1])
                        elif dt_element[0] == 'vis':
                            for ex in dt_element[1]:
                                definition['examples'].append(dict_util.manage_braces(ex['t']))
                    
                    definition['closely_related_meaning'] = ''
                    definition['closely_related_examples'] = []
                    if 'sdsense' in sense:
                        for dt_element in sense['sdsense']['dt']:
                            if dt_element[0] == 'text':
                                definition['closely_related_meaning'] = dict_util.manage_braces(dt_element[1])
                            elif dt_element[0] == 'vis':
                                for ex in dt_element[1]:
                                    definition['closely_related_examples'].append(dict_util.manage_braces(ex['t']))

                    if definition['meaning'] != '': description['definitions'].append(definition)

        # syllable division
        description['syllable'] = word_dict['hwi']['hw']
        # audio link
        description['audio_links'] = []
        if 'prs' in word_dict['hwi']:
            for sound_obj in word_dict['hwi']['prs']:
                if 'sound' in sound_obj:
                    # description['enunciation'] = sound_obj['mw']
                    audio_filename = sound_obj['sound']['audio']
                    if audio_filename.startswith('bix'):
                        audio_subdir = 'bix'
                    elif audio_filename.startswith('gg'):
                        audio_subdir = 'gg'
                    elif audio_filename[0] in string.punctuation or audio_filename[0].isdigit():
                        audio_subdir = 'number'
                    else:
                        audio_subdir = audio_filename[0]
                    description['audio_links'].append(f'https://media.merriam-webster.com/audio/prons/en/us/mp3/{audio_subdir}/{audio_filename}.mp3')

        descriptions.append(description)
    
    return descriptions