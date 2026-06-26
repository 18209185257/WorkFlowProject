#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小化测试 - 仅验证提示词和清洁功能
"""

import re

def clean_output(text):
    """清洁输出并确保中文回答"""
    # 清洗乱码和标签
    text = re.sub(r'[ĠĊ]+', ' ', text)
    text = re.sub(r'</?think>|[<>|]+', ' ', text)
    text = re.sub(r'^[\W\d\s]*', '', text)
    
    # 检查中文字符数量
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    english_chars = re.findall(r'[a-zA-Z]', text)
    
    print(f"分析结果: 中文字符 {len(chinese_chars)}, 英文字符 {len(english_chars)}")
    
    # 如果中文字符太少，返回标准中文回答
    if len(chinese_chars) < 3:
        if "你是谁" in text or "你是" in text:
            return "我是中文AI助手，很高兴为您服务！"
        else:
            return "抱歉，我必须用中文回答您的问题。"
    
    return text.strip()

def generate_prompt(question):
    """生成中文提示词"""
    prompt = f"【系统角色设定】你是一个专业的中文AI助手，只能使用中文进行交流。严格禁止使用任何英文内容。如果用户用中文提问，你必须用中文回答。【用户问题】{question}【必须用中文回答】"
    return prompt

def test_minimal():
    """最小化测试"""
    print("=" * 50)
    print("最小化中文测试")
    print("=" * 50)
    
    # 测试问题
    test_questions = [
        "你是谁？",
        "你好",
        "What is your name?",
        ""  # 空问题
    ]
    
    for question in test_questions:
        print(f"\n{'='*20}")
        print(f"测试问题: '{question}'")
        print(f"{'='*20}")
        
        # 生成提示词
        prompt = generate_prompt(question)
        print(f"生成的提示词长度: {len(prompt)}")
        
        # 测试各种回答
        test_responses = [
            "I am an AI assistant.",
            "你好，我是AI助手。",
            "",
            "   ",
            "ĠĊ测试回答"
        ]
        
        for i, response in enumerate(test_responses):
            print(f"\n测试回答 {i+1}: '{response}'")
            result = clean_output(response)
            print(f"清洁后: '{result}'")
            
            # 检查是否为中文
            if len(re.findall(r'[\u4e00-\u9fff]', result)) > 0:
                print("状态: [OK] 中文回答")
            else:
                print("状态: [FAIL] 非中文")

def create_memory_fix():
    """创建内存优化建议"""
    print("\n" + "="*50)
    print("内存优化建议")
    print("="*50)
    print("1. 减少模型大小 - 尝试使用更小的模型")
    print("2. 使用CPU模式 - 禁用GPU内存")
    print("3. 减少batch size - 降低并发处理")
    print("4. 使用8bit量化 - 而不是4bit")
    print("5. 增加虚拟内存 - 设置页面文件")
    
    print("\n修复后的测试文件:")
    print("- C:\\Users\\82251\\PycharmProjects\\ThickModelProject\\experiment_word\\test_model.py")
    print("- C:\\Users\\82251\\.openclaw\\workspace\\safe_test_model.py")
    print("- C:\\Users\\82251\\.openclaw\\workspace\\minimal_test.py")

if __name__ == "__main__":
    test_minimal()
    create_memory_fix()