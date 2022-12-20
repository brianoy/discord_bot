import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import requests
from mod.addlog import addlog

txt_path = '../project_discord\price_save\price.txt'#卡了一個小時 須注意相對路徑跟絕對路徑的問題
url = "https://www.jetstar.com/tw/zh/home?adults=1&children=0&destination=NRT&flexible=1&flight-type=1&infants=0&origin=TPE&selected-departure-date=06-02-2023&tab=1"
url2 = "https://booking.jetstar.com/tw/zh/booking/search-flights?Currency=TWD&adults=1&children=0&departuredate1=2023-02-06&destination1=NRT&dotcomFCOutboundMemberPriceShown=false&dotcomFCOutboundPriceShown=false&dotcomFCPricesHidden=false&infants=0&origin1=TPE"
url3 = "https://booking.jetstar.com/"
webhook_url = "https://discord.com/api/webhooks/1050476762691285002/zkYNPnW52TLagD75IoNFvnDjfEimokWaUwPpPfoLjNMmu5HeKRVpGLHwa-cAyg03A1g"
japan_previous_price = ""

class japan:
    def create_uc_object():
        global wd
        wd = uc.Chrome()

    def get_variable():
        try:
            global japan_previous_price
            with open(txt_path, 'r') as f:
                price = f.read()
            japan_previous_price = price
        except:
            addlog.error("抓取價格數據失敗")

    def set_variable(value):
        try:
            with open(txt_path, 'w') as f:
                f.write(str(value))
            japan.get_variable()
        except:
            addlog.error("覆蓋價格數據失敗")

    def webhook(payload)->int:
        try:
            data = {"content": str(payload)}
            response = requests.post(webhook_url, json=data)
        except:
            addlog.error("webhook傳出失敗")
        return response.status_code

    def check_airline_price():
        global japan_previous_price
        try:
            japan.create_uc_object()
        except:
            addlog.error("建立瀏覽器物件失敗")
            wd.quit()

        try:
            #wd.get(url)
            wd.execute_script('return navigator.webdriver')
            wd.get(url3)
            wd.find_element(by=By.TAG_NAME,value= "body").click()#除了傳統防爬蟲測試外，還有需要實際物理點擊或FOCUS的偵測
            time.sleep(1)
            wd.get(url2)
            time.sleep(3)
        except:
            addlog.error("導覽網頁失敗")
            wd.quit()
        '''
        try:
            wd.find_element(by=By.XPATH, value= "/html/body/div[3]/div/div/main/div/div[1]/div[2]/div[2]/div/div/div/section/div/div[4]/button").click()
            addlog.debug("已點擊")
            time.sleep(2)
        except:
            wd.get_screenshot_as_file("screenshot.png")
            addlog.error("查詢價格按鈕失敗")
            wd.quit()
        '''
        try:
            japan.get_variable()
            current_price = str(wd.find_element(by=By.XPATH,value= "/html/body/main/div[8]/form/div[3]/div[1]/div[3]/div/div/ul/li[4]/div[2]/div/span[2]").text).replace(",","")
            if japan_previous_price != current_price:
                japan.webhook("2/6 TPE->NRT 捷星價格已變動 NT$" + current_price)
                japan.set_variable(current_price)
            else:
                addlog.debug("2/6 TPE->NRT 捷星價格無變動 NT$" + current_price)
        except:
            wd.get_screenshot_as_file("screenshot.png")
            addlog.error("抓取或輸出價格失敗")
            wd.quit()
        wd.close()
        wd.quit()