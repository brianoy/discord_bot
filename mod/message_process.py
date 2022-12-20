from auto_roll_call.roll_call import auto_roll_call
from mod.addlog import addlog#不要用print()，而是用addlog.debug()或addlog.info()等等

class message_process:
    def message_process(message):
        addlog.debug(str(message.author) + "/" + str(message.channel) + " : " + str(message.content))
        if str(message.channel) == "點名頻道" and "https://itouch.cycu.edu.tw" in message.content and "active_system/query_course/learning" in message.content:
            try:
                return auto_roll_call.url_login(message.content)
            except:
                return "點名錯誤，請再試一次"
        else:
            return False
