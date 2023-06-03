# -*- coding=utf-8 -*-
# ======主程序======
import os
from log_ger import *

# 检测配置文件
def detection_config_file():
    import time
    from configobj import ConfigObj
    from config import  path_ini,default_config_ini_json   # 导入配置
    logger.info("正在检测配置文件")
    # 判断配置文件 是否存在 或 为空
    if (os.path.exists(path_ini) == False or os.stat(path_ini).st_size == 0):
        # 配置文件 json 转 ini 
        config_ini_test = ""
        for i in range(0,list(default_config_ini_json).__len__()):
            section = list(default_config_ini_json)[i]
            config_ini_test += "[" + section + "]\n"
            for j in range(0,list(default_config_ini_json[section]).__len__()):
                key = list(default_config_ini_json[section])[j]
                value = default_config_ini_json[section][key]
                config_ini_test += key + " = " + value + "\n"
            config_ini_test += "\n"
        config_ini_test = config_ini_test[:-1]

        logger.error("配置文件（config.ini），不存在，正在创建。")
        file_config = open(str(path_ini), "w", encoding='UTF8')
        file_config.write(config_ini_test)
        file_config.close()
        logger.error("配置文件以创建（config.ini），请修改后再次启动程序。")
        time.sleep(5) 
        sys.exit()  # 退出程序


    # 检测配置文件是否缺失，并修复
    config = ConfigObj(path_ini, encoding='utf-8')    # 导入配置文件
    for i in range(0,list(default_config_ini_json).__len__()):
        section = list(default_config_ini_json)[i]
        if section not in config:
            logger.warning(f"配置文件缺失 {section} 节，准备添加该节。")
            config[section] = {}
            config.write()
            logger.info(f"添加 {section} 节成功")
        for j in range(0,list(default_config_ini_json[section]).__len__()):
            key = list(default_config_ini_json[section])[j]
            value = default_config_ini_json[section][key]
            if key not in config[section]:
                logger.warning(f"配置文件 {section} 节中缺失 {key} 键，准备添加该键。")
                config[section][key] = value
                config.write()
                logger.info(f"添加 {key} 键成功")

    # 配置文件重新排序
    config = ConfigObj(path_ini, encoding='utf-8')    # 导入配置文件
    config_ini = ""
    for i in range(0,list(default_config_ini_json).__len__()):
        section = list(default_config_ini_json)[i]
        config_ini += "[" + section + "]\n"
        for j in range(0,list(default_config_ini_json[section]).__len__()):
            key = list(default_config_ini_json[section])[j]
            value = config[section][key]
            if "{" in value and "}" in value:
                config_ini += key + " = '" + value + "'\n"
            else:
               config_ini += key + " = " + value + "\n"
        config_ini += "\n"
    config_ini = config_ini[:-1]

    file_config = open(str(path_ini), "w", encoding='UTF8')
    file_config.write(config_ini)
    file_config.close()

    logger.info("配置文件检测完成")

# 检测配置文件
def detection_environment():
    from configobj import ConfigObj
    from py2neo import Graph    
    from config import  path_ini
    logger.info("正在检测环境")
    config = ConfigObj(path_ini, encoding='utf-8')    # 导入配置文件
    # 检测 neo4j 数据库 连接是否正常
    agreement = config["neo4j_db"]["agreement"]
    host = config["neo4j_db"]["host"]
    port = config["neo4j_db"]["port"]
    Username = config["neo4j_db"]["Username"]
    password = config["neo4j_db"]["password"]
    try:
        graph = Graph(f"{agreement}://{host}:{port}", auth=(Username, password))
        graph.run("MATCH (n) RETURN count(n)").to_table()
    except Exception as e:
        logger.error("连接 neo4j 数据库失败", e)
        exit()
    
    dict_directory = config["neo4j_db"]["dict_directory"]
    if not os.path.exists(dict_directory):
        logger.info(f"{dict_directory}不存在")
        os.makedirs(dict_directory)
        logger.info(f"{dict_directory}已创建")

    logger.info("环境检测完成")

if __name__ == '__main__':
    detection_config_file() # 检测配置文件
    detection_environment() # 检测环境

    def custom_error(message):
        print('错误：缺少必需的参数，请参阅帮助信息以获取更多信息。')
        parser.print_help()
        sys.exit(2)

    import argparse
    parser = argparse.ArgumentParser(prog='myprogram', add_help=False)  
    parser.error = custom_error

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-h', '--help', action='help', help='显示帮助')
    group.add_argument('-i', '--import_data_to_neo4j', action='store_true', help='将数据导入neo4j数据库（知识图谱数据导入）')
    group.add_argument('-t', '--test_chatbot_graph', action='store_true', help='在py启动问答程序脚本（用于测试）')
    group.add_argument('-w', '--web', action='store_true', help='启动web服务')
    args = parser.parse_args()

    if args.import_data_to_neo4j:
        logger.info("正在将数据导入neo4j数据库（知识图谱数据导入）")

        from configobj import ConfigObj
        from config import  path_ini   # 导入配置
        config = ConfigObj(path_ini, encoding='utf-8')    # 导入配置文件  
        json_data = config["neo4j_db"]["json_data"]
        if not os.path.exists(json_data):
            logger.error(f"{json_data}不存在")
            exit()

        from neo4j_db import import_data_to_neo4j
        import_data_to_neo4j.main()

    if args.test_chatbot_graph:
        logger.info("正在启动 在py启动问答程序脚本（用于测试）")
        from neo4j_db import chatbot_graph
        chatbot_graph.main()

    if args.web:
        logger.info("正在启动 web 服务")
        from web import web_main
        web_main.main()     # 启动服务

    # from neo4j_db import import_data_to_neo4j, chatbot_graph
    # from web import web_main
    
    # import_data_to_neo4j.main()  # 将数据导入neo4j数据库（知识图谱数据导入）
    # chatbot_graph.main()    # 问答程序脚本
    
    # web_main.main()     # 启动服务