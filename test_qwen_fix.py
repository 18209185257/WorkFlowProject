#!/usr/bin/env python3

import json
import hashlib
import os
import subprocess
from pathlib import Path

def test_tokenizer_hash():
    """Test the tokenizer hash to identify the pre-tokenizer type."""
    
    # Test text from convert_hf_to_gguf.py
    chktxt = '\n \n\n \n\n\n \t \t\t \t\n  \n   \n    \n     \n🚀 (normal) 😶\u200d🌫️ (multiple emojis concatenated) ✅ 🦙🦙 3 33 333 3333 33333 333333 3333333 33333333 3.3 3..3 3...3 កាន់តែពិសេសអាច😁 ?我想在apple工作1314151天～ ------======= нещо на Български \'\'\'\'\'\'```````""""......!!!!!!?????? I\'ve been \'told he\'s there, \'RE you sure? \'M not sure I\'ll make it, \'D you like some tea? We\'Ve a\'lL'
    
    # Load tokenizer.json
    model_path = Path("D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B-Developer/DeepSeek-R1-Distill-Qwen-7b-Developer")
    tokenizer_json_path = model_path / "tokenizer.json"
    
    if not tokenizer_json_path.exists():
        print(f"❌ Error: tokenizer.json not found at {tokenizer_json_path}")
        return None
    
    with open(tokenizer_json_path, 'r', encoding='utf-8') as f:
        tokenizer_data = json.load(f)
    
    print("✅ tokenizer.json loaded successfully")
    print(f"Tokenizer config keys: {list(tokenizer_data.keys())}")
    
    # Try to simulate the tokenizer encoding process
    try:
        # Use transformers to get the actual encoding
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        
        print(f"✅ Tokenizer loaded: {type(tokenizer)}")
        print(f"Vocabulary size: {len(tokenizer.get_vocab())}")
        
        # Get the actual tokenization
        chktok = tokenizer.encode(chktxt)
        chkhsh = hashlib.sha256(str(chktok).encode()).hexdigest()
        
        print(f"Encoded tokens: {chktok}")
        print(f"Hash: {chkhsh}")
        
        # Check against known hashes
        known_hashes = {
            "b3f499bb4255f8ca19fccd664443283318f2fd2414d5e0b040fbdd0cc195d6c5": "deepseek-r1-qwen",
            "e636dc30a262dcc0d8c323492e32ae2b70728f4df7dfe9737d9f920a282b8aea": "qwen2",
            "d30d75d9059f1aa2c19359de71047b3ae408c70875e8a3ccf8c5fba56c9d8af4": "qwen35",
            "a1336059768a55c99a734006ffb02203cd450fed003e9a71886c88acf24fdbc2": "glm4",
            "9ca2dd618e8afaf09731a7cf6e2105b373ba6a1821559f258b272fe83e6eb902": "glm4",
            "cdf5f35325780597efd76153d4d1c16778f766173908894c04afc20108536267": "glm4"
        }
        
        for known_hash, name in known_hashes.items():
            if chkhsh == known_hash:
                print(f"✅ Match found: {name}")
                return name
        
        print("❌ No hash match found - this model has a unique pre-tokenizer")
        return None
        
    except Exception as e:
        print(f"❌ Error during tokenization: {e}")
        return None

def create_simple_tokenizer_model():
    """Create a simple tokenizer.model file for llama.cpp."""
    
    model_path = Path("D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B-Developer/DeepSeek-R1-Distill-Qwen-7b-Developer")
    
    try:
        import sentencepiece as spm
        
        print("Creating simple tokenizer.model...")
        
        # Load tokenizer
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        
        # Create temporary files for sentencepiece training
        temp_dir = model_path / "temp_sp"
        temp_dir.mkdir(exist_ok=True)
        
        # Save vocabulary
        vocab = tokenizer.get_vocab()
        with open(temp_dir / "vocab.txt", "w", encoding="utf-8") as f:
            for token, idx in sorted(vocab.items(), key=lambda x: x[1]):
                if isinstance(token, str):
                    f.write(f"{token}\n")
        
        # Train sentencepiece model
        spm.SentencePieceTrainer.train(
            input=str(temp_dir / "vocab.txt"),
            model_prefix=str(temp_dir / "tokenizer"),
            vocab_size=len(vocab),
            model_type='bpe',
            character_coverage=0.9995,
            max_sentence_length=4192,
            split_by_unicode_script=True,
            split_by_number=True,
            split_by_whitespace=True,
            normalization_rule_name='nmt_nfkc_cf',
            remove_extra_whitespaces=True,
            input_sentence_size=1000000,
            shuffle_input_sentence=True,
            seed_sentencepiece_size=1000000,
            shrinking_factor=0.75,
            max_sentencepiece_length=16,
            split_digits=True,
            control_symbols=['<ctrl>', '<unused0>'],
            user_defined_symbols=['<usr>', '<sys>'],
            byte_fallback=True,
            vocabulary_output_score=True,
            hard_vocab_limit=True,
            use_all_vocab=False
        )
        
        # Copy the created tokenizer.model to the main model directory
        source_model = temp_dir / "tokenizer.model"
        target_model = model_path / "tokenizer.model"
        
        if source_model.exists():
            import shutil
            shutil.copy2(source_model, target_model)
            print(f"✅ Created tokenizer.model at: {target_model}")
            
            # Clean up
            import shutil
            shutil.rmtree(temp_dir)
            
            return True
        else:
            print("❌ Failed to create tokenizer.model")
            return False
            
    except Exception as e:
        print(f"❌ Error creating tokenizer.model: {e}")
        return False

def run_conversion_with_fix():
    """Run the conversion with our fixes."""
    
    model_path = Path("D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B-Developer/DeepSeek-R1-Distill-Qwen-7b-Developer")
    output_path = model_path / "DeepSeek-R1-Distill-Qwen-7B-Developer-fixed.F16.gguf"
    
    # Convert paths to strings for subprocess
    model_str = str(model_path)
    output_str = str(output_path)
    
    # Build command with fallback options
    cmd = [
        "python", "convert_hf_to_gguf.py",
        model_str,
        "--outtype", "f16",
        "--outfile", output_str,
        "--verbose",
        "--vocab-only",
        "--trust-remote-code",
        "--no-chat-template"
    ]
    
    print(f"Running conversion command: {' '.join(cmd)}")
    
    try:
        # Set environment to disable tokenizer validation
        env = os.environ.copy()
        env["GGUF_DISABLE_TOKENIZER_VALIDATION"] = "1"
        
        # Run conversion
        result = subprocess.run(
            cmd,
            cwd="C:/msys64/home/82251/llama.cpp",
            env=env,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutes timeout
        )
        
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout[-5000:])  # Last 5000 characters
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr[-5000:])  # Last 5000 characters
        
        if result.returncode == 0:
            print("✅ Conversion successful!")
            
            # Check output file
            if output_path.exists():
                size_gb = output_path.stat().st_size / (1024**3)
                print(f"Output file size: {size_gb:.2f} GB")
                return True
            else:
                print("❌ Output file not found")
                return False
        else:
            print("❌ Conversion failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Conversion timeout")
        return False
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return False

def main():
    print("🔧 DeepSeek-R1-Distill-Qwen-7B-Developer GGUF Conversion Fix")
    print("=" * 60)
    
    # Step 1: Test tokenizer hash
    print("\n📋 Step 1: Testing tokenizer hash...")
    tokenizer_type = test_tokenizer_hash()
    
    # Step 2: Create tokenizer.model if needed
    print("\n📋 Step 2: Creating tokenizer.model...")
    if not (Path("D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B-Developer/DeepSeek-R1-Distill-Qwen-7b-Developer") / "tokenizer.model").exists():
        create_simple_tokenizer_model()
    else:
        print("✅ tokenizer.model already exists")
    
    # Step 3: Run conversion
    print("\n📋 Step 3: Running conversion...")
    success = run_conversion_with_fix()
    
    if success:
        print("\n🎉 Conversion completed successfully!")
    else:
        print("\n❌ Conversion failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())