import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
from onmt.utils.logging import logger
import common_util_functions as util

def handle_single_token(token):
   try:
       if isfloat(token):
            return (token)
       elif util.token_is_date(token):
           print("returning date")
           return token     
       elif token.isalnum():
            logger.info("transliterating alphanum")
            return transliterate_text(token)
       elif len(token) > 1 and token_is_alphanumeric_char(token):
            if len(token) ==3 and (token[0].isalnum() == False) and (token[1].isalnum() == True):
                return token 
            prefix,suffix,translation_text = separate_alphanumeric_and_symbol(token)
            # translation_text = transliterate_text(translation_text)
            return prefix+translation_text+suffix
       elif token.isalpha() and len(token)==1:
            return (token)
                
       else:
            logger.info("returning token as it is")
            return token
   except:
       logger.info("returning token as it is")
       return token
          

def replace_from_LC_table(token):
    hindi_number=list()
    for char in token:
        if char.isdigit():
            with open("lookup_table.txt", "r") as f:
                            for line in f:
                                if line.startswith(char):
                                    char = line.split('|||')[1].strip() 

        hindi_number.append(char) 
    s = [str(i) for i in hindi_number] 
    res = ("".join(s)) 
    return res 

def isfloat(str):
    try: 
        float(str)
    except ValueError: 
        return False
    return True

def capture_prefix_suffix(text):
    prefix = text[0]
    suffix = text[-1] 
    if (prefix.isalpha() or prefix.isdigit()) and (suffix.isalpha() or suffix.isdigit() or suffix == '.'):
        prefix = ""
        suffix = ""
        translation_text = text
    elif (prefix.isalpha() or prefix.isdigit()) and (suffix.isalpha()== False and suffix.isdigit()==False and suffix != '.'): 
        prefix = ""
        translation_text = text[0:]
    elif (prefix.isalpha()==False or prefix.isdigit()==False) and (suffix.isalpha()== False and suffix.isdigit()==False and suffix != '.'):
        translation_text = text[1:-1]  
    elif (prefix.isalpha()==False or prefix.isdigit()==False) and (suffix.isalpha() or suffix.isdigit() or suffix == '.'):  
        suffix = ""
        translation_text = text[1:]     
    print(prefix,suffix,translation_text)
    return prefix,suffix,translation_text

def token_is_alphanumeric_char(token):
    "checking if single token consists of alphanumeric and symbolic characters. But, symbol only at the begining and end are considerd"
    if re.match(r'^[\w]+$', token) is None:
        return True

def separate_alphanumeric_and_symbol(text):
    try:
        # print(re.sub(r"^\W+|\W+$", "", text),"in separate")     
        start = re.match(r"^\W+|\W+$", text)
        end = re.match(r'.*?([\W]+)$', text)
        translation_text = re.sub(r"^\W+|\W+$", "", text)    
                  
        if start:
            start = start.group(0)
            if start.endswith('(') and len(translation_text)>1 and translation_text[0].isalnum() and translation_text[1]== ')':
                start = start + translation_text[0] + translation_text[1]
                translation_text = translation_text[2:]
                start_residual_part = re.match(r"^\W+|\W+$", translation_text)
                # print("1",translation_text)    
                if start_residual_part:
                    start_residual_part = start_residual_part.group(0)
                    start = start+start_residual_part
                    translation_text = re.sub(r"^\W+|\W+$", "", translation_text) 
                    # print("2",translation_text)     

        else:
            start = ""           
        if end:
            end = end.group(1)
            if end.startswith('.'):
                end = end[1:]
                translation_text = translation_text + '.' 
        else:
            end = ""            
    
        print(start,end,translation_text)     
        return start,end,translation_text
    except:
        print("in except,anciliary fun")
        return "","",text


def transliterate_text(text):
    print(transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI))
    return transliterate(text.lower(), sanscript.ITRANS, sanscript.DEVANAGARI)

def replace_hindi_numbers(text):
    hindi_numbers = ['०', '१', '२', '३','४','५','६','७','८','९']
    eng_numbers = ['0','1','2','3','4','5','6','7','8','9'] 
 
    for i in hindi_numbers : 
        text = text.replace(i,eng_numbers[hindi_numbers.index(i)]) 
    return text    


"below is for handling dates which are splitted in more than 1 token and other special cases"
def special_case_fits(text):
    if util.token_is_date(text):
        return True
        

def handle_special_cases(text):
    if util.token_is_date(text):
        text = transliterate_text(text)
        logger.info('transliterating dates in long alpha-numeric format')
        return text
