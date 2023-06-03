from . import app_plugins
import urllib.parse
from flask import request
from neo4j_db.chatbot_graph import ChatBotGraph
from configobj import ConfigObj
from config import  path_ini   # 导入配置

app = app_plugins

config = ConfigObj(path_ini, encoding='utf-8')    # 导入配置文件
handler = ChatBotGraph()
statement = config["ai"]["statement"]

@app.route('/api', methods=['POST'])
def api():
    message = urllib.parse.unquote(request.data.decode())
    reply_message = handler.chat_main(message)

    if reply_message[0]:
        return {"ai":f"{reply_message[1]}{statement}"}
    else:
        return {"ai":reply_message[1]}

