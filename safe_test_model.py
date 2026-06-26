#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全版本的中文AI助手 - 针对内存优化
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import warnings
import re

warnings.filterwarnings("ignore")

class SafeDeepSeekChatBot:
    def __init__(self, model_path="D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B/DeepSeek-R1-Distill-Qwen-7b"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.max_length = 256  # 减少最大长度
        self.max_new_tokens = 128  # 减少新生成token数

        # 4bit 量化 - 更安全的配置
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

    def load_model(self):
        """安全加载模型"""
        try:
            print("正在安全加载模型...")
            
            # 检查GPU内存
            if torch.cuda.is_available():
                total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                available_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"GPU总内存: {total_memory:.1f} GB")
                print(f"可用内存: {available_memory:.1f} GB")
                
                if available_memory < 8:  # 内存小于8GB
                    print("⚠️ GPU内存不足，尝试使用CPU...")
                    torch.cuda.set_per_process_memory_fraction(0.5)  # 限制内存使用
            
            # 加载tokenizer
            print("正在加载tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.padding_side = "left"

            # 安全加载模型
            print("正在加载模型权重...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                quantization_config=self.bnb_config,
                trust_remote_code=True,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                use_cache=False,
            )
            
            self.model.eval()
            print("✅ 模型加载成功！")
            return True

        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            print("尝试使用CPU模式...")
            return self.load_cpu_mode()

    def load_cpu_mode(self):
        """CPU模式加载"""
        try:
            print("尝试CPU模式加载...")
            
            self.bnb_config = BitsAndBytesConfig(
                load_in_4bit=False,  # CPU模式下不使用4bit
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
        """清洁输出并确保中文回答"""
        # 清洗乱码和标签
        text = re.sub(r'[ĠĊ]+', ' ', text)
        text = re.sub(r'</?think>|[<>|]+', ' ', text)
        text = re.sub(r'^[\W\d\s]*', '', text)
        
        # 检查中文字符数量
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        english_chars = re.findall(r'[a-zA-Z]', text)
        
        # 如果中文字符太少，返回标准中文回答
        if len(chinese_chars) < 3:
            if "你是谁" in text or "你是" in text:
                return "我是中文AI助手，很高兴为您服务！"
            else:
                return "抱歉，我必须用中文回答您的问题。"
        
        return text.strip()

    def ask(self, question):
        """询问问题"""
        try:
            text = question.strip()
            if not text:
                return "请输入问题"

            # 生成中文提示词
            prompt = f"【系统角色设定】你是一个专业的中文AI助手，只能使用中文进行交流。严格禁止使用任何英文内容。如果用户用中文提问，你必须用中文回答。【用户问题】{text}【必须用中文回答】"

            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
                padding="longest",
            ).to("cuda" if torch.cuda.is_available() else "cpu")

            # 生成回答
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

            # 解码回答
            response = self.tokenizer.decode(
                outputs[0][len(inputs["input_ids"][0]):],
                skip_special_tokens=True
            )

            return self.clean_output(response)

        except Exception as e:
            print(f"错误详情：{e}")
            return "抱歉，回答过程中出现错误，请重试。"

def test_safe_version():
    """测试安全版本"""
    print("=" * 50)
    print("安全版本中文AI助手测试")
    print("=" * 50)
    
    bot = SafeDeepSeekChatBot()
    
    if not bot.load_model():
        print("❌ 模型加载失败，无法继续测试")
        return
    
    # 测试问题
    test_questions = ["你是谁？", "你好"]
    
    for question in test_questions:
        print(f"\n{'='*30}")
        print(f"问题: {question}")
        print(f"{'='*30}")
        
        print("思考中...")
        answer = bot.ask(question)
        print(f"回答: {answer}")

if __name__ == "__main__":
    test_safe_version()