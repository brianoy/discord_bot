import logging
import requests
file_path = "E:\\work spaces\\project_discord\\log\\bot.log"#若為相對路徑時，有可能會讓在其他資料夾的module無法執行(會寫undefined)
Url = "https://discord.com/api/webhooks/1029631682283843584/rvG-qKW9McTAKTAZmIMbO7mZVOgOLC9GH6J_RWSbheaOibOTYg69c3cdWl7xnkh_mH9"#可考慮換成存取環境變量
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(filename)s %(levelname)s %(message)s",
                    datefmt="%a %d %b %Y %H:%M:%S",
                    filename=file_path,
                    filemode="a")

class addlog:
    def __init__(self,msg):
        self.msg = msg

    def debug(msg):
        msg = str(msg)
        msg = "🟢[DEBUG]" + msg + "\n"
        print(msg)
        logging.debug(msg)
        webhook(msg)

    def info(msg):
        msg = str(msg)
        msg = "🟡[INFO]" + msg + "\n"
        print(msg)
        logging.info(msg)
        webhook(msg)

    def warning(msg):
        msg = str(msg)
        msg = "🟠[WARNING]" + msg + "\n"
        print(msg)
        logging.warning(msg)
        webhook(msg)

    def error(msg):
        msg = str(msg)
        msg = "🔴[ERROR]" + msg + "\n"
        print(msg)
        logging.error(msg)
        webhook(msg)

def webhook(payload)->int:
    data = {"content": str(payload)}
    response = requests.post(Url, json=data)
    return response.status_code
