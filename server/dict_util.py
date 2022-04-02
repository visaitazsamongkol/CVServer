import os

current_dir = os.path.dirname(os.path.realpath(__file__))

def get_api_keys():
    with open(os.path.join(current_dir, 'merriam-webster-key.txt'), 'r') as file:
        for line in file:
            key_list = line.split('=')
            if key_list[0].strip() == 'COLLEGIATE_DICT_API_KEY': COLLEGIATE_DICT_API_KEY = key_list[1].strip()
            elif key_list[0].strip() == 'COLLEGIATE_THES_API_KEY': COLLEGIATE_THES_API_KEY = key_list[1].strip()
    return COLLEGIATE_DICT_API_KEY, COLLEGIATE_THES_API_KEY


def manage_braces(text):
    del_index = []
    is_in_brace = False
    is_field = False
    is_field_count_change = False
    field_count = 0
    last_special_char = ''
    last_field_seperator_index = 999999
    first_field_seperator_index = 999999
    for i in range(len(text)):
        if text[i]=='{':
            is_in_brace = True
            is_field = False
            is_field_count_change = False
            last_special_char = text[i]
            del_index.append(i)
        elif text[i]=='}':
            is_in_brace = False
            is_field = False
            is_field_count_change = True
            field_count = 0
            last_special_char = text[i]
            del_index.append(i)
        elif text[i]=='|':
            is_field = True
            is_field_count_change = True
            field_count += 1
            if last_special_char == '{': 
                first_field_seperator_index = i
            last_special_char = text[i]
            last_field_seperator_index = i
            if  field_count >= 3:
                for j in range(first_field_seperator_index+1, last_field_seperator_index):
                    if j not in del_index:
                        del_index.append(j)            
            del_index.append(i)
        else:
            if not is_in_brace:
                is_field_count_change = False
            elif is_in_brace and not is_field:
                is_field_count_change = False
                del_index.append(i)
            elif is_in_brace and is_field:
                if field_count < 2:
                    is_field_count_change = False
                elif field_count == 2:
                    if is_field_count_change:
                        for j in range(first_field_seperator_index+1, last_field_seperator_index):
                            if j not in del_index:
                                del_index.append(j)
                        is_field_count_change = False
                else: 
                    is_field_count_change = False
                    del_index.append(i)
    result = list(text)
    num_adjacent_space = 0
    for i in range(len(result)):
        if i in del_index:
            result[i] = ''
        elif result[i]==' ':
            num_adjacent_space += 1
            if num_adjacent_space >= 2:
                result[i] = ''
        else: num_adjacent_space = 0
    
    return ''.join(result).strip()


def del_non_alpha_endings(word):
    result = word
    for i in range(len(word)-1,0,-1):
        if not word[i].isalpha():
            result = result[:-1]
        else:
            break
    return result.lower()