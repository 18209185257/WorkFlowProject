#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中文AI助手回答
"""

import sys
import os
sys.path.append(r"C:\Users\82251\PycharmProjects\ThickModelProject\experiment_word")

from test_model import DeepSeekChatBot

def test_chinese_response():
    """测试中文回答"""
    print("=" * 50)
    print("测试中文AI助手回答")
    print("=" * 50)
    
    # 创建机器人实例
    bot = DeepSeekChatBot()
    
    # 检查模型是否存在
    if not os.path.exists(bot.model_path):
        print(f"❌ 模型路径不存在: {bot.model_path}")
        return
    
    # 加载模型
    print("正在加载模型...")
    if not bot.load_model():
        return
    
    # 测试问题
    test_questions = [
        "你是谁？",
        "你好",
        "请介绍一下你自己"
    ]
    
    for question in test_questions:
        print(f"\n{'='*20}")
        print(f"测试问题: {question}")
        print(f"{'='*20}")
        
        print(f"你：{question}")
        print("思考中...")
        
        answer = bot.ask(question)
        print(f"模型：{answer}")
        
        # 检查中文含量
        import re
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', answer)
        english_chars = re.findall(r'[a-zA-Z]', answer)
        
        print(f"中文字符数: {len(chinese_chars)}")
        print(f"英文字符数: {len(english_chars)}")
        
        if len(chinese_chars) > len(english_chars) * 2:  # 中文字符远多于英文字符
            print("✅ 中文回答良好")
        elif len(chinese_chars) > 0:
            print("⚠️ 部分中文回答")
        else:
            print("❌ 未检测到中文回答")
        
        print("-" * 50)

if __name__ == "__main__":
    test_chinese_response()