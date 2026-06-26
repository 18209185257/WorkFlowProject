#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整修复方案 - 最终版本
"""

import os
import subprocess
import sys

def install_dependencies():
    """安装必需的依赖包"""
    print("正在安装必需的依赖包...")
    
    required_packages = [
        "accelerate",
        "transformers",
        "torch",
        "bitsandbytes"
    ]
    
    for package in required_packages:
        try:
            print(f"检查 {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "show", package], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"安装 {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                print(f"✅ {package} 安装成功")
            else:
                print(f"✅ {package} 已安装")
        except subprocess.CalledProcessError as e:
            print(f"❌ 安装 {package} 失败: {e}")

def fix_model_file():
    """修复模型文件中的问题"""
    model_path = r"C:\Users\82251\PycharmProjects\ThickModelProject\experiment_word\test_model.py"
    
    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在: {model_path}")
        return False
    
    print(f"正在修复模型文件: {model_path}")
    
    # 读取文件内容
    with open(model_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复torch_dtype废弃警告
    content = content.replace('torch_dtype=torch.float16,', 'dtype=torch.float16,')
    
    # 修复device_map问题（添加accelerate支持）
    if 'device_map="auto"' in content:
        print("✅ 已包含device_map配置")
    
    # 写回文件
    with open(model_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 模型文件修复完成")
    return True

def test_chinese_response():
    """测试中文回答功能"""
    print("\n" + "="*50)
    print("开始测试中文回答功能")
    print("="*50)
    
    try:
        # 导入修复后的模块
        sys.path.append(r"C:\Users\82251\PycharmProjects\ThickModelProject\experiment_word")
        from test_model import DeepSeekChatBot
        
        # 创建机器人实例
        bot = DeepSeekChatBot()
        
        # 检查模型路径是否存在
        if not os.path.exists(bot.model_path):
            print(f"❌ 模型路径不存在: {bot.model_path}")
            print("请检查模型路径是否正确")
            return False
        
        print("正在加载模型...")
        if not bot.load_model():
            print("❌ 模型加载失败")
            return False
        
        # 测试中文回答
        test_questions = [
            "你是谁？",
            "你好",
            "请用中文回答"
        ]
        
        for question in test_questions:
            print(f"\n{'='*30}")
            print(f"测试问题: {question}")
            print(f"{'='*30}")
            
            print("思考中...")
            answer = bot.ask(question)
            print(f"回答: {answer}")
            
            # 检查中文含量
            import re
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', answer)
            english_chars = re.findall(r'[a-zA-Z]', answer)
            
            print(f"中文字符: {len(chinese_chars)}, 英文字符: {len(english_chars)}")
            
            if len(chinese_chars) > 0:
                print("✅ 中文回答成功")
            else:
                print("❌ 未检测到中文")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 完整修复方案 ===\n")
    
    # 1. 安装依赖
    install_dependencies()
    
    # 2. 修复模型文件
    if fix_model_file():
        # 3. 测试功能
        test_chinese_response()
    else:
        print("❌ 文件修复失败")

if __name__ == "__main__":
    main()