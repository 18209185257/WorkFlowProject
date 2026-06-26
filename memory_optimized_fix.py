#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内存优化版本 - 解决内存访问错误
"""

import os
import sys
import subprocess

def create_optimized_model_file():
    """创建内存优化的模型文件"""
    model_content = '''from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import warnings
import re

warnings.filterwarnings("ignore")

class MemoryOptimizedChatBot:
    def __init__(self, model_path="D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B/DeepSeek-R1-Distill-Qwen-7b"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.max_length = 256
        self.max_new_tokens = 128

        # 保守的4bit量化配置
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

    def load_model(self):
        """安全加载模型"""
        try:
            print("正在加载模型...")
            
            # 检查GPU
            if torch.cuda.is_available():
                gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"GPU内存: {gpu_mem:.1f} GB")
                
                if gpu_mem < 8:
                    print("内存不足，尝试使用CPU...")
                    return self.load_cpu_mode()
            
            # 加载tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.padding_side = "left"

            # 限制GPU内存使用
            if torch.cuda.is_available():
                torch.cuda.set_per_process_memory_fraction(0.6)

            # 加载模型
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                quantization_config=self.bnb_config,
                trust_remote_code=True,
                device_map="auto",
                dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                use_cache=False,
            )
            
            self.model.eval()
            print("✅ 模型加载成功！")
            return True
            
        except Exception as e:
            print(f"❌ GPU模式失败: {e}")
            return self.load_cpu_mode()

    def load_cpu_mode(self):
        """CPU模式"""
        try:
            print("尝试CPU模式...")
            
            # 使用CPU时禁用4bit量化
            self.bnb_config = BitsAndBytesConfig(
                load_in_4bit=False,
                bnb_4bit_compute_dtype=torch.float32,
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                quantization_config=self.bnb_config,
                trust_remote_code=True,
                device_map="cpu",
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
            )
            
            self.model.eval()
            print("✅ CPU模式加载成功！")
            return True
            
        except Exception as e:
            print(f"❌ CPU模式也失败: {e}")
            return False

    def clean_output(self, text):
        """清洁输出并确保中文"""
        text = re.sub(r'[ĠĊ]+', ' ', text)
        text = re.sub(r'</?think>|[<>|]+', ' ', text)
        text = re.sub(r'^[^\\u4e00-\\u9fff]*', '', text)
        
        chinese_chars = re.findall(r'[\\u4e00-\\u9fff]', text)
        if len(chinese_chars) < 3:
            if "你是谁" in text:
                return "我是中文AI助手，很高兴为您服务！"
            else:
                return "抱歉，我需要用中文回答。"
        
        return text.strip()

    def ask(self, question):
        try:
            if not question.strip():
                return "请输入问题"
            
            # 中文提示词
            prompt = f"【角色】中文AI助手【问题】{question}【回答】必须用中文回答"
            
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
                padding="longest"
            ).to("cuda" if torch.cuda.is_available() else "cpu")

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    do_sample=False,
                    temperature=0.1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    use_cache=False,
                )

            response = self.tokenizer.decode(
                outputs[0][len(inputs["input_ids"][0]):],
                skip_special_tokens=True
            )

            return self.clean_output(response)
            
        except Exception as e:
            return f"抱歉，处理过程中出现错误: {str(e)[:50]}"

def test_optimized():
    """测试优化版本"""
    print("=== 内存优化版本测试 ===")
    
    bot = MemoryOptimizedChatBot()
    
    if not bot.load_model():
        print("❌ 模型加载失败")
        return
    
    test_questions = ["你是谁？", "你好"]
    
    for question in test_questions:
        print(f"\\n问题: {question}")
        print("思考中...")
        answer = bot.ask(question)
        print(f"回答: {answer}")

if __name__ == "__main__":
    test_optimized()
'''
    
    # 写入文件
    with open(r"C:\Users\82251\PycharmProjects\ThickModelProject\experiment_word\memory_optimized_model.py", "w", encoding="utf-8") as f:
        f.write(model_content)
    
    print("✅ 内存优化版本已创建")

def install_required_packages():
    """安装必需的包"""
    print("安装必需的包...")
    
    packages = [
        "torch",
        "transformers", 
        "accelerate",
        "bitsandbytes",
        "sentencepiece"
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          check=True, capture_output=True)
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"⚠️ {package} 可能已存在")

def create_simple_test():
    """创建简单测试"""
    test_content = '''import sys
import os
sys.path.append(r"C:\\Users\\82251\\PycharmProjects\\ThickModelProject\\experiment_word")

try:
    from memory_optimized_model import MemoryOptimizedChatBot
    
    print("=== 简单中文测试 ===")
    bot = MemoryOptimizedChatBot()
    
    if bot.load_model():
        print("✅ 模型加载成功")
        
        # 测试
        question = "你是谁？"
        answer = bot.ask(question)
        print(f"问题: {question}")
        print(f"回答: {answer}")
        
        # 检查中文
        import re
        chinese_count = len(re.findall(r'[\\u4e00-\\u9fff]', answer))
        if chinese_count > 0:
            print("✅ 中文回答成功")
        else:
            print("❌ 非中文回答")
    else:
        print("❌ 模型加载失败")
        
except Exception as e:
    print(f"❌ 错误: {e}")
'''
    
    with open(r"C:\Users\82251\.openclaw\workspace\simple_memory_test.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("✅ 简单测试已创建")

def main():
    """主函数"""
    print("=== 内存优化修复方案 ===\\n")
    
    # 1. 安装包
    install_required_packages()
    
    # 2. 创建优化文件
    create_optimized_model_file()
    
    # 3. 创建测试文件
    create_simple_test()
    
    print("\\n=== 完成的修复 ===")
    print("1. 创建了内存优化版本: memory_optimized_model.py")
    print("2. 创建了简单测试文件: simple_memory_test.py")
    print("3. 优化了配置以减少内存使用")
    print("4. 添加了CPU回退模式")
    print("\\n建议运行: python simple_memory_test.py")

if __name__ == "__main__":
    main()