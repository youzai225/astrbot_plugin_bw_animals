import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.all import register
from astrbot.api.model.Message import Plain

BLACK_WHITE_MEMBERS = {
    "卑鄙小企鹅": {
        "name": "嗣大林", 
        "desc": "群主本想自称“卑微小企鹅”并撤回防脱脸，却被群友无情截胡并嘲讽为“卑鄙小企鹅”。"
    },
    "大海雀": {
        "name": "嗣大林", 
        "desc": "高级防屏蔽平替！为了绕开群主的企鹅识别Bot，群友找来长相酷似的海鸟破防群主。"
    },
    "黑白动物": {
        "name": "嗣大林", 
        "desc": "企鹅的终极代称。群友直接用“霸凌的黑白动物”指代动不动就撤回别人消息的群主。"
    },
    "企鹅": {
        "name": "嗣大林", 
        "desc": "群主的本体！因常被内涵，他甚至写了识别机器人防图，是不在场时也会被拉出来研究的万恶之源。"
    },
    "斑马": {
        "name": "嗣大林", 
        "desc": "群友用“黑白配色”打哑谜内涵群主，结果因缺乏“鸟类”特征，被吐槽难道你想让斑马飞。"
    },
    "鸵鸟": {
        "name": "嗣大林", 
        "desc": "同样为了避开屏蔽，群友精准提取了“不会飞”和“黑白配色”两大属性找来的绝佳替身。"
    },
    "熊猫": {
        "name": "嗣大林", 
        "desc": "万物皆可平替！群友发“对着熊猫哈气”疯狂暗示，被极其敏感的群主光速动用权限撤回。"
    }
}

@register("bw_animal_detector", "黑白动物梗侦测", "自动检测QQ群聊中群友用黑白动物代指某人的内部梗。", "1.0.0")
class BWAnimalDetectorPlugin:
    def __init__(self, context):
        self.context = context
        self.animals = sorted(list(BLACK_WHITE_MEMBERS.keys()), key=len, reverse=True)
        self.pattern = re.compile(f"({'|'.join(self.animals)})")

    @filter.on_message()
    async def handle_group_message(self, event: AstrMessageEvent):
        msg_text = event.message_str.strip()
        
        ignore_words = ["百度", "百科", "科普", "水族馆", "动物园", "视频"]
        if any(word in msg_text for word in ignore_words):
            return

        match = self.pattern.search(msg_text)
        if match:
            found_animal = match.group(1)
            target = BLACK_WHITE_MEMBERS[found_animal]
            
            reply_text = (
                f"📡 【黑白动物梗侦测成功】\n"
                f"发现高频代称：【{found_animal}】\n"
                f"🎯 对应群友：@{target['name']}\n"
                f"📖 内部梗概：{target['desc']}"
            )
            
            event.stop_event() # 阻断后续大模型普通对话
            await event.send_message([Plain(reply_text)])
