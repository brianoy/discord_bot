from mod.addlog import addlog
def voice_chat_log(member, before, after):
    before_channel = str(before.channel)
    after_channel = str(after.channel)
    member = str(member)
    if before_channel == "None" :
        addlog.info(member + " 加入了 " + after_channel)
    elif after_channel == "None" :
        addlog.info(member + " 離開了 " + before_channel)
    elif before_channel == after_channel:
        pass
        member_voice_status(member, before, after)
    else:
        addlog.info(member + " 從 " + before_channel + " 跑到了 " + after_channel)

def member_voice_status(member, before, after):
    if before.self_mute != after.self_mute:
        if before.self_mute == True:
            addlog.info(member + " 開啟麥克風")
        else:
            addlog.info(member + " 關閉麥克風")
    elif before.self_deaf != after.self_deaf:
        if before.self_deaf == True:
            addlog.info(member + " 開啟耳機")
        else:
            addlog.info(member + " 關閉耳機")
    elif before.self_stream != after.self_stream:
        if before.self_stream == True:
            addlog.info(member + " 關閉直播")
        else:
            addlog.info(member + " 開啟直播")
    elif before.suppress != after.suppress:
        if before.suppress == True:
            addlog.warning(member + " 所以這到底是啥1")
        else:
            addlog.warning(member + " 所以這到底是啥2")
    elif before.requested_to_speak_at != after.requested_to_speak_at:
        if before.requested_to_speak_at == True:
            addlog.info(member + " 要求講話")
        else:
            addlog.info(member + " 無要求講話")
    else:
        pass
