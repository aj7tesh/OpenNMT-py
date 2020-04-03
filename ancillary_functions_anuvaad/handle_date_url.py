import re
import ancillary_functions_anuvaad.common_util_functions as common_utils
from config.regex_patterns import patterns, hindi_numbers
from onmt.utils.logging import logger


def tag_number_date_url(text):
  try: 
    resultant_str = list()
    count_date = 0
    date_original = list()
    count_url = 0
    url_original = list()
    for word in text.split():
        print("word",word)
        # if len(word)>4 and len(word)<12 and token_is_date(word):
        ext = [".",",","?","!"]
        if word.isalpha()== False and word[:-1].isalpha() == False and len(word)>4 and common_utils.token_is_date(word):
            if word.endswith(tuple(ext)):
              end_token = word[-1]
              word = word[:-1]
              if len(word)<7 and int(word):
                word = word+end_token
                print("kkkk")
              else:
                date_original.append(word)
                word = 'DdAaTtEe'+str(count_date)+end_token
                count_date +=1
                print("jjj")
            else:
              date_original.append(word)  
              word = 'DdAaTtEe'+str(count_date)
              count_date +=1
              print("ggg")
        elif common_utils.token_is_url(word):
            url_original.append(word)
            word = 'UuRrLl'+str(count_url)
            count_url +=1
            print("kkk")

        resultant_str.append(word)   
        s = [str(i) for i in resultant_str] 
        res = str(" ".join(s))  
    print("res",res,date_original,url_original)    

    return res,date_original,url_original 
  except Exception as e:
    print(e)   

def replace_tags_with_original(text,date_original,url_original):
  try:
    resultant_str = list()
    for word in text.split():
      print("word-1",word[:-1])
      if word[:-1] == 'DdAaTtEe':
        word = date_original[int(word[-1])]
        print(word,"date")
      elif word[:-1] == 'UuRrLl':
        word = url_original[int(word[-1])]  
        print("url",word)

      resultant_str.append(word)
      s = [str(i) for i in resultant_str] 
      res = str(" ".join(s))

    print(res,"response")
    return res    
  except Exception as e:
    print(e)
    pass

"merge below two functions and above two, when training for tamil again..above two are used in tamil 2108, rest all will use below one"

def tag_number_date_url_1(text):
  try: 
    resultant_str = list()
    count_date = 0
    date_original = list()
    count_url = 0
    url_original = list()
    count_number = 0
    # number_original = list()
    num_array = re.findall(patterns['p3']['regex'],text)
    num_array = list(map(int, num_array)) 
    num_array.sort(reverse = True)
    for j in num_array:
      text = text.replace(str(j),'NnUuMm'+str(hindi_numbers[count_number]),1)
      count_number +=1
      if count_number >30:
        print("count exceeding 30")
        count_number = 30

    logger.info("Number tagging done")
    for word in text.split():
        # if len(word)>4 and len(word)<12 and token_is_date(word):
        try:
          ext = [".",",","?","!"]
          if word.isalpha()== False and word[:-1].isalpha() == False and len(word)>4 and common_utils.token_is_date(word):
            if word.endswith(tuple(ext)):
              end_token = word[-1]
              word = word[:-1]
              if len(word)<7 and int(word):
                word = word+end_token
              else:
                date_original.append(word)
                word = 'DdAaTtEe'+str(count_date)+end_token
                count_date +=1
            else:
              date_original.append(word)  
              word = 'DdAaTtEe'+str(count_date)
              count_date +=1
          elif common_utils.token_is_url(word):
            url_original.append(word)
            word = 'UuRrLl'+str(count_url)
            count_url +=1
        except Exception as e:
          print(e)
          logger.error("In handle_date_url:tag_num function:{}".format(e))
          word = word
        

        resultant_str.append(word)   
        s = [str(i) for i in resultant_str] 
        res = str(" ".join(s))   
    logger.info("tagged response:{} and date:{} and url:{}".format(res,date_original,url_original)) 
    return res,date_original,url_original,num_array 
  except Exception as e:
    logger.error("In handle_date_url:tag_num function parent except block:{}".format(e))
    return text,[],[],(num_array or []) 

def replace_tags_with_original_1(text,date_original,url_original,num_array):
  try:
    resultant_str = list()
      
    if len(text) == 0:
      return ""
    for word in text.split():
      if word[:-1] == 'DdAaTtEe' and len(date_original) > 0:
        word = date_original[int(word[-1])]
      elif word[:-1] == 'UuRrLl' and len(url_original)> 0 :
        word = url_original[int(word[-1])]          

      resultant_str.append(word)
      s = [str(i) for i in resultant_str] 
      res = str(" ".join(s))

    logger.info("response after url and date replacemnt:{}".format(res))
    array = re.findall(r'NnUuMm..|NnUuMm.', res)   
    logger.info("NnUuMm array after translation:{}".format(array))
    for j in array:
      try:
        if j[-2:] in hindi_numbers:
          end_hin_number = j[-2:]
          index = hindi_numbers.index(end_hin_number)
          res = res.replace(j,str(num_array[index]),1)
        elif j[:-1]== "NnUuMm":
          end_hin_number = j[-1]
          index = hindi_numbers.index(end_hin_number)
          res = res.replace(j,str(num_array[index]),1)
        else:
          end_hin_number = j[-2]
          j = j[:-1]
          index = hindi_numbers.index(end_hin_number)     
          res = res.replace(j,str(num_array[index]),1)
      
      except Exception as e:
        logger.info("inside str.replace error,but handling it:{}".format(e))
        res = res.replace(j,"",1)

    logger.info("response after tags replacement:{}".format(res))
    return res    
  except Exception as e:
    logger.error("Error in parent except block of replace_tags_with_original_1 function, returning tagged output:{}".format(e))
    return text


def regex_pass(text,regex_list):
  try:
    regex_list = regex_list
    for pattern in regex_list:
      text = re.sub(pattern,r'\1\2',text)

    return text
    
  except Exception as e:
    logger.error("Error in regex_pass: handle_date_url function:{}".format(e))
    return text