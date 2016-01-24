from flask import Flask, jsonify, request
from urllib.parse import quote
import wolfram_helper, sms_helper, wikipedia, traceback

reply_start = '''<?xml version="1.0" encoding="UTF-8"?><Response><Sms>'''
reply_end = '''</Sms></Response>'''
SMS_image_ext = ['.gif','.jpg','.jpeg','.png','.tiff']

app = Flask(__name__)
previous_query_msg = ""


def get_xml_return(str):
    return reply_start + str + reply_end


@app.route('/get_reply')
def get_reply():
    global previous_query_msg, previous_query_type, previous_wolfram_obj, previous_wiki_string
    msg = str(request.args.get('Body'))
    to_number = str(request.args.get('From'))
    from_number = sms_helper.get_from_number()
    if msg.lower() == "--help": return get_xml_return("Welcome to the Smart Twilio Messenger! Just text me anything you want to know about, and have fun! @shirj23 #UofTHakcs2016")
    if "awesome" in msg.lower() and "this" in msg.lower(): return get_xml_return("Thank you!")
    if "more" in msg.lower() and previous_query_msg != "":
        if previous_query_type == "wolfram":
            for pod in previous_wolfram_obj.pods:
                if "pedia" in pod.title:
                    sms_helper.send_mms(to_number, from_number, pod.title + ":", pod.img)
            return reply_start + \
                   '\n'.join(wolfram_helper.get_all_title_and_answer_str_from_resultObj(previous_wolfram_obj)) + \
                   reply_end
        elif previous_query_type == "wiki":
            wikiObj = wikipedia.page(previous_query_msg)
            split_ind = previous_wiki_string.index('\n')
            try:
                i = 0
                while not any(word in wikiObj.images[i] for word in SMS_image_ext):
                    i += 1
                sms_helper.send_mms(to_number,from_number, "(continue...)\n"+
                                    previous_wiki_string[split_ind+1:min(len(previous_wiki_string),split_ind+1000)]+"...",
                                    wikiObj.images[i])
                print("Wiki MMS message sent")
            except Exception as e:
                print("Wiki MMS message failed")
                traceback.print_tb(e.__traceback__)
            return reply_start + \
                   wikiObj.url + ':\n' + previous_wiki_string[0:split_ind] + \
                   reply_end

    else:
        previous_query_msg = msg

    # try:
    wolframResObj = wolfram_helper.get_wolframalpha_resultObj(msg)
    if wolframResObj.pods and "wikipedia" not in msg.lower():
        previous_query_type = "wolfram"
        previous_wolfram_obj = wolframResObj
        if wolfram_helper.get_answer_str_from_resultObj(wolframResObj) != "":
            ans_w_tit = wolfram_helper.get_answer_with_title_from_resultObj(wolframResObj)
            return reply_start+ans_w_tit+reply_end
        else:
            if return_query_and_answer(wolframResObj):
                body = get_query_and_answer_mms_body(wolframResObj)
                media_url = get_query_and_answer_mms_media_URL(wolframResObj)
            else:
                body = wolfram_helper.get_answer_title_from_resultObj(wolframResObj)
                media_url = [wolfram_helper.get_answer_img_from_resultObj(wolframResObj)]
            sms_helper.send_mms(to_number, from_number, body, media_url)
            return reply_start+"An MMS result is sent:\n"+reply_end
    else:
        if "wikipedia" in msg.lower():
            msg = msg[msg.find("Wikipedia")+len("Wikipedia")+1:]
        previous_query_type = "wiki"
        try:
            previous_wiki_string = wikipedia.summary(msg)
            return reply_start+previous_wiki_string[0:min(len(previous_wiki_string),100)]+'...'+reply_end
        except wikipedia.exceptions.PageError:
            related = wikipedia.search(msg)
            if related:
                previous_query_msg = related[0]
                previous_wiki_string = wikipedia.summary(previous_query_msg)
                return reply_start+ previous_query_msg + '\n'+ previous_wiki_string[0:min(len(previous_wiki_string),100)]+'...' + \
                       "\nAlso try ask about: " + ",".join(related[1:min(5, len(related))]) + reply_end
            else:
                return get_error_message(msg)
        except wikipedia.exceptions.DisambiguationError as e:
            return get_xml_return("Do you mean:\n" + ",".join(e.options))

    # except:
        # return get_error_message(msg)


def return_query_and_answer(resObj):
    return wolfram_helper.get_query_str_from_resultObj(resObj) != ""


def get_query_and_answer_mms_body(resObj):
    return wolfram_helper.get_query_title_from_resultObj(resObj) + ':\n' + \
           wolfram_helper.get_query_str_from_resultObj(resObj) + '\n' + \
           wolfram_helper.get_answer_title_from_resultObj(resObj) + ':\n'


def get_query_and_answer_mms_media_URL(resObj):
    return [wolfram_helper.get_answer_img_from_resultObj(resObj)]


def get_google_search(msg):
    return "https://www.google.ca/search?q=" + quote(msg, safe='')


def get_error_message(msg):
    return reply_start+"Bzzzz Sorry we could not find any results... but stay tuned as we update! Try:\n"+\
           get_google_search(msg)+reply_end


@app.route('/')
def index():
    msg = str(request.args.get('Body'))
    return reply_start+"You sent: "+msg+reply_end

# @app.route('/add')
# def add():
#     n1 = float(request.args.get('n1')) # GET request variables
#     n2 = float(request.args.get('n2'))
#     return jsonify({'sum':n1+n2})

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')