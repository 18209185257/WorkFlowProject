#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版测试 - 只验证提示词生成
"""

import re

def clean_output(text):
    """测试清洁输出函数"""
    # 彻底清洗乱码、思维链标签，并确保中文回答
    text = re.sub(r'[ĠĊ]+', ' ', text)
    text = re.sub(r'</?think>|[<>|]+', ' ', text)
    text = re.sub(r'^[\W\d\s]*', '', text)  # 移除开头非中文字符
    
    # 检查是否为中文回答，如果不是则强制返回中文回答
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    if len(chinese_chars) < 3:  # 中文字符太少
        # 强制返回标准中文回答
        if "你是谁" in text or "你是" in text:
            return "我是中文AI助手，很高兴为您服务！"
        else:
            return "抱歉，我必须用中文回答您的问题。"
    
    return text.strip()

def generate_prompt(question):
    """生成测试提示词"""
    # 【关键】超强中文角色设定和系统提示
    prompt = f"【系统角色设定】你是一个专业的中文AI助手，只能使用中文进行交流。严格禁止使用任何英文内容，包括单词、句子、符号等。如果用户用中文提问，你必须用中文回答。【用户问题】{question}【必须用中文回答】"
    return prompt

def test_prompt_generation():
    """测试提示词生成和清洁功能"""
    print("=" * 50)
    print("测试提示词生成和中文清洁功能")
    print("=" * 50)
    
    # 测试问题
    test_questions = [
        "你是谁？",
        "你好",
        "请介绍一下你自己",
        "What is your name?"  # 英文问题
    ]
    
    for question in test_questions:
        print(f"\n{'='*20}")
        print(f"测试问题: {question}")
        print(f"{'='*20}")
        
        # 生成提示词
        prompt = generate_prompt(question)
        print(f"生成的提示词:\n{prompt}")
        
        # 模拟不同的回答进行测试
        test_responses = [
            "I am an AI assistant.",  # 英文回答
            "你好，我是AI助手。",    # 中文回答
            "我是AI助手",          # 简短中文
            "",                   # 空回答
            "ĠĊ</think>测试回答"   # 带乱码的回答
        ]
        
        for i, response in enumerate(test_responses):
            print(f"\n测试回答 {i+1}: '{response}'")
            cleaned = clean_output(response)
            print(f"清洁后: '{cleaned}'")
            
            # 检查中文含量
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', cleaned)
            english_chars = re.findall(r'[a-zA-Z]', cleaned)
            
            print(f"中文字符: {len(chinese_chars)}, 英文字符: {len(english_chars)}")
            
            if len(chinese_chars) > 0:
                print("[OK] 包含中文")
            else:
                print("[FAIL] 不包含中文")

if __name__ == "__main__":
    test_prompt_generation()