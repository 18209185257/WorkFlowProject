#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试脚本 - 验证中文回答修复
"""

import sys
import os

def test_chinese_response():
    """测试中文回答功能"""
    print("=" * 50)
    print("中文AI助手最终测试")
    print("=" * 50)
    
    # 添加路径
    sys.path.append(r"C:\Users\82251\PycharmProjects\ThickModelProject\experiment_word")
    
    try:
        from test_model import DeepSeekChatBot
        
        # 创建机器人实例
        bot = DeepSeekChatBot()
        
        # 检查模型路径
        model_path = bot.model_path
        print(f"模型路径: {model_path}")
        
        if not os.path.exists(model_path):
            print(f"[ERROR] 模型路径不存在: {model_path}")
            return False
        
        print("正在加载模型...")
        if not bot.load_model():
            print("[ERROR] 模型加载失败")
            return False
        
        # 测试中文回答
        test_questions = [
            "你是谁？",
            "你好",
            "请用中文介绍你自己"
        ]
        
        success_count = 0
        
        for question in test_questions:
            print(f"\n{'='*30}")
            print(f"问题: {question}")
            print(f"{'='*30}")
            
            try:
                answer = bot.ask(question)
                print(f"回答: {answer}")
                
                # 检查中文含量
                import re
                chinese_chars = re.findall(r'[\u4e00-\u9fff]', answer)
                english_chars = re.findall(r'[a-zA-Z]', answer)
                
                print(f"中文字符: {len(chinese_chars)}, 英文字符: {len(english_chars)}")
                
                if len(chinese_chars) > 0:
                    print("[OK] 中文回答成功")
                    success_count += 1
                else:
                    print("[FAIL] 未检测到中文")
                
            except Exception as e:
                print(f"[ERROR] 回答失败: {e}")
        
        print(f"\n{'='*50}")
        print(f"测试结果: {success_count}/{len(test_questions)} 个问题测试成功")
        
        if success_count == len(test_questions):
            print("🎉 所有测试成功！")
            return True
        else:
            print("⚠️ 部分测试失败，可能需要进一步调整")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_chinese_response()