# -*- coding=utf-8 -*-
# ======配置文件======
import os
import sys

# 程序运行目录
path = os.path.dirname(os.path.realpath(sys.argv[0]))
# 配置文件地址
path_ini =  path + '/config.ini'

# 默认配置文件
default_config_ini_json = {
    "neo4j_db":{
        "agreement":"bolt",
        "host":"127.0.0.1",
        "port":"7687",
        "Username":"neo4j",
        "password":"neo4j",
        "json_data":"data/medical.json",
        "dict_directory":"data/dict"
    },
    "ai":{
        "default_answer":"很抱歉，我们的数据库中没有找到与您的问题匹配的答案。建议您向专业医生咨询，以便得到更准确的答案。或者您可以换一个方式询问。",
        "statement":"<br><br>----------<br>以上内容仅供参考。"
    },
    "web":{
        "disclaimers":"本疾病咨询系统中的所有信息、建议和意见，仅用于提供医学知识和参考，不作为医疗诊断或治疗的替代。请您在遇到任何疾病或健康问题时，及时咨询专业医生，并严格遵守医生的诊治方案和药物使用说明。本系统不对您因使用本系统所提供的任何信息而带来的直接或间接的结果，承担任何责任。任何人士在使用本系统的信息时，应自行承担风险和责任。"
    }
}
