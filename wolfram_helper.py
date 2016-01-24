import wolframalpha
app_id = "" # APP ID for WolframAlpha
client = wolframalpha.Client(app_id)

QUERY_POD = 0
ANSWER_POD = 1


def get_wolframalpha_resultObj(query_str):
    return client.query(query_str)


def get_answer_str_from_resultObj(resObj):
    ret = resObj.pods[ANSWER_POD].text
    if ret is None:
        return ""
    return ret


def get_query_str_from_resultObj(resObj):
    ret = resObj.pods[QUERY_POD].text
    if ret is None:
        return ""
    return ret


def get_answer_img_from_resultObj(resObj):
    ret = resObj.pods[ANSWER_POD].img
    if ret is None:
        return ""
    return ret


def get_query_img_from_resultObj(resObj):
    ret = resObj.pods[QUERY_POD].img
    if ret is None:
        return ""
    return ret


def get_answer_title_from_resultObj(resObj):
    ret = resObj.pods[ANSWER_POD].title
    if ret is None:
        return ""
    return ret


def get_query_title_from_resultObj(resObj):
    ret = resObj.pods[QUERY_POD].title
    if ret is None:
        return ""
    return ret


def get_all_answer_str_from_resultObj(resObj):
    return [pod.text if pod.text is not None else "" for pod in resObj]


def get_all_title_and_answer_str_from_resultObj(resObj):
    return [pod.title + ":\n" + pod.text for pod in resObj if pod.text is not None]


def get_answer_str(query_str):
    ret = get_answer_str_from_resultObj(get_wolframalpha_resultObj(query_str))
    if ret is None:
        return ""
    return ret    


def get_answer_with_title_from_resultObj(resObj):
    ans = get_answer_str_from_resultObj(resObj)
    tit = get_answer_title_from_resultObj(resObj)
    if tit == "":
        return ans
    return tit+":\n"+ans


if __name__ == '__main__':
    res = client.query('bye bye')
    print("Answer:")
    print(get_answer_str_from_resultObj(res))
    print("All:")
    print("\n".join(get_all_answer_str_from_resultObj(res)))
    print("Answer with title:")
    print(get_answer_with_title_from_resultObj(res))
    
    #res1 = client.query('When was Bill born?')
    #print("Answer:")
    #print(get_answer_str_from_resultObj(res1))
    #print("All:")
    #print("\n".join(get_all_answer_str_from_resultObj(res1)))
    #print("Answer with title:")
    #print(get_answer_with_title_from_resultObj(res1))      


