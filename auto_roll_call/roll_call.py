from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from project_discord.mod.addlog import addlog
userlist = ["11021340","10922248","10922347"]
pwlist = ["Aa123456789","Oylt0925","Jeremy7774789"]
namelist = ["歐陽","狸玖","日月夷"]

class auto_roll_call:
    def create_browzer_object():
        global wd
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')#無視窗
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent=Mozilla/5.0')
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--example-flag')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-infobars")
        wd = webdriver.Chrome(options=chrome_options)

    def url_login(msg)->str:
        global url
        global time_and_classname
        start_time = time.time()
        url = str(msg).replace("&afterLogin=true","").replace(":443","")
        try:
            auto_roll_call.create_browzer_object()
            wd.get(url)
            not_open = "未開放 QRCODE簽到功能" in wd.page_source
            time_and_classname = str(wd.find_element(by=By.XPATH, value='/html/body/div/div[2]/p').text).replace("課程點名", "").replace("　　", " ")
            #xpath = '/html/body/div/div[2]/p/text()[4]'
            #curriculum_name = str(wd.find_element(by=By.XPATH, value=xpath).text)  
            if not_open:
                '''fail_login_status = len(userlist)
                messageout = "🟥警告❌，點名並沒有開放，請稍後再試或自行手點，全數點名失敗\n"
                not_send_msg = True
                print("傳出flexmsg")
                line_bot_api.reply_message(event.reply_token, flex_message)
                not_send_msg = False'''
                addlog.debug("🟥警告❌，點名並沒有開放，請稍後再試或自行手點，全數點名失敗\n")
            else:
                auto_roll_call.open_tab()
                auto_roll_call.login()
                messageout = str(auto_roll_call.message_print())
            messageout = (messageout + "\n此次點名耗費時間:" + str(round((time.time() - start_time + 2), 2)) +"秒")#(最後時間-觸發時間)+2誤差值，四捨五入取小數點到第二位
        except IndexError:
            messageout = "🟥🟥FATAL ERROR🟥🟥\n可能是由ilearning網頁故障或是輸入錯誤的網址所引起\n請盡快手點和連繫我"
        wd.quit()#完整退出瀏覽器
        addlog.info(messageout)
        return messageout

    def open_tab():
        for i in range(0,len(userlist),1):#總共會有len(userlist)+1個分頁被開啟
            wd.execute_script("window.open('');")#取一 我也不知道差在哪
            #wd.switch_to.new_window('tab')#但是這個就是會當掉，run到登入完頁面就會停止
            wd.switch_to.window(wd.window_handles[i+1])
            wd.get(url)#打開所有對應數量的分頁並到網址
            addlog.debug("已打開第"+ str(i) + "個分頁")

    def login():
        for i in range(0,len(userlist),1):#輸入帳號密碼 並登入
            wd.switch_to.window(wd.window_handles[i+1])#先跑到對應的視窗
            usr =  userlist[i]
            pwd = pwlist[i]
            wd.execute_script('document.getElementById("UserNm").value ="' + usr + '"')
            wd.execute_script('document.getElementById("UserPasswd").value ="' + pwd + '"')
            wd.execute_script('document.getElementsByClassName("w3-button w3-block w3-green w3-section w3-padding")[0].click();')
            addlog.debug("已登入第"+ str(i) + "個分頁")

    def message_print()->str:
        information = ""
        for i in range(0,len(userlist),1):
            usr =  userlist[i]#之後的訊息要顯示
            name = namelist[i]
            wd.switch_to.window(wd.window_handles[i+1])#先跑到對應的視窗
            password_wrong = EC.alert_is_present()(wd)#如果有錯誤訊息#不太確定要先切換視窗再按確認還是反過來
            if password_wrong:
                failmsg = password_wrong.text
                password_wrong.accept()
                information = (information + "學號:" + usr + "\n🟥點名失敗❌\n錯誤訊息:密碼錯誤" + failmsg +'\n\n')#error login
            else:
                try:#嘗試找尋失敗#D06079
                    wd.find_element(by=By.CSS_SELECTOR, value= "[stroke='#D06079']")#第一次用cssselector 如果沒有紅色就會是成功訊息
                    fail_msg = str(wd.find_element(by=By.XPATH,value= "/html/body/div[1]/div[3]/div").text)
                    information = (information + "\n🟥點名失敗❌，"+ name +"好可憐喔😱\n失敗訊息:" + fail_msg +'\n\n')
                    if "簽到未開放" in fail_msg:
                        information = "🟥警告❌，點名尚未開始，請稍後再試，全數點名失敗\n"
                        addlog.debug("🟥警告❌，點名尚未開始")
                        break
                except NoSuchElementException:#找不到#D06079就會是成功#73AF55
                    detailmsg = wd.find_element(by=By.XPATH,value= "/html/body/div[1]/div[3]/div").text
                    information = (information + "\n🟩點名成功✅，"+ name +"會非常感謝你\n成功訊息:" + detailmsg.replace('&#x6708;','月').replace('&#x65e5;','日').replace('&#x3a;',':').replace('<br>','\n')+'\n\n')
        information = information + time_and_classname
        addlog.debug(information)
        return information

#auto_roll_call.url_login("https://itouch.cycu.edu.tw/active_system/query_course/learning_activity_stulogin.jsp?act_no=15ce5f9e-5f1c-47be-89af-ad160ccc3dc5")#test