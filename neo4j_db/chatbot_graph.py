# -*- coding=utf-8 -*-
# ======问答程序脚本======
# 来源：https://github.com/liuhuanyong/QASystemOnMedicalKG

from .question_classifier import *
from .question_parser import *
from .answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        from configobj import ConfigObj
        from config import  path_ini   # 导入配置
        config = ConfigObj(path_ini, encoding='utf-8')    # 导入配置文件
        self.default_answer = config["ai"]["default_answer"]
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = self.default_answer
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return [False,answer]
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return [False,answer]
        else:
            return [True,'\n'.join(final_answers)]


def main():
    handler = ChatBotGraph()
    while 1:
        question = input('user:')
        answer = handler.chat_main(question)
        print('ai:', answer)

