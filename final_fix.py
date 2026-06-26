#!/usr/bin/env python3

import json
import hashlib
import os
import subprocess
from pathlib import Path

def fix_tokenizer_hash():
    """Fix the tokenizer hash issue by updating the convert_hf_to_gguf.py script."""
    
    # Path to the convert_hf_to_gguf.py script
    convert_script = Path("C:/msys64/home/82251/llama.cpp/convert_hf_to_gguf.py")
    
    if not convert_script.exists():
        print(f"ERROR: convert_hf_to_gguf.py not found at {convert_script}")
        return False
    
    # Read the current script
    with open(convert_script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the hash checking section and add our new hash correctly
    target_pattern = '        if chkhsh == "cdf5f35325780597efd76153d4d1c16778f766173908894c04afc20108536267":'
    replacement = '''        if chkhsh == "cdf5f35325780597efd76153d4d1c16778f766173908894c04afc20108536267":
            res = "glm4"
        if chkhsh == "b0d03e997351c41b4ba8013dc400510737f9a9029a417c7c148516323dca908c":  # DeepSeek-R1-Distill-Qwen-7B-Developer
            res = "qwen2"'''
    
    # Update the content
    if target_pattern in content:
        print("Found existing hash section, adding DeepSeek hash...")
        updated_content = content.replace(target_pattern, replacement)
        
        # Write the updated content
        with open(convert_script, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("SUCCESS: Updated convert_hf_to_gguf.py with DeepSeek tokenizer hash")
        return True
    else:
        print("ERROR: Could not find hash section in convert_hf_to_gguf.py")
        return False

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
        
        # Save vocabulary - limit to maximum allowed size
        vocab = tokenizer.get_vocab()
        vocab_size = min(len(vocab), 125000)  # Limit to SentencePiece max
        
        print(f"Original vocab size: {len(vocab)}, using: {vocab_size}")
        
        # Get the most common tokens
        sorted_tokens = sorted(vocab.items(), key=lambda x: x[1])[:vocab_size]
        
        with open(temp_dir / "vocab.txt", "w", encoding="utf-8") as f:
            for token, idx in sorted_tokens:
                if isinstance(token, str):
                    f.write(f"{token}\n")
        
        # Train sentencepiece model with correct parameters
        spm.SentencePieceTrainer.train(
            input=str(temp_dir / "vocab.txt"),
            model_prefix=str(temp_dir / "tokenizer"),
            vocab_size=vocab_size,
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
            hard_vocab_limit=True,
            use_all_vocab=False
        )
        
        # Copy the created tokenizer.model to the main model directory
        source_model = temp_dir / "tokenizer.model"
        target_model = model_path / "tokenizer.model"
        
        if source_model.exists():
            import shutil
            shutil.copy2(source_model, target_model)
            print(f"SUCCESS: Created tokenizer.model at: {target_model}")
            
            # Clean up
            import shutil
            shutil.rmtree(temp_dir)
            
            return True
        else:
            print("FAILED: Failed to create tokenizer.model")
            return False
            
    except Exception as e:
        print(f"ERROR creating tokenizer.model: {e}")
        return False

def run_conversion_with_fix():
    """Run the conversion with our fixes."""
    
    model_path = Path("D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B-Developer/DeepSeek-R1-Distill-Qwen-7b-Developer")
    output_path = model_path / "DeepSeek-R1-Distill-Qwen-7B-Developer-fixed.F16.gguf"
    
    # Convert paths to strings for subprocess
    model_str = str(model_path)
    output_str = str(output_path)
    
    # Build command with correct parameters
    cmd = [
        "python", "convert_hf_to_gguf.py",
        model_str,
        "--outtype", "f16",
        "--outfile", output_str,
        "--verbose",
        "--vocab-only"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        # Run conversion
        result = subprocess.run(
            cmd,
            cwd="C:/msys64/home/82251/llama.cpp",
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
            print("SUCCESS: Conversion completed!")
            
            # Check output file
            if output_path.exists():
                size_gb = output_path.stat().st_size / (1024**3)
                print(f"Output file size: {size_gb:.2f} GB")
                return True
            else:
                print("ERROR: Output file not found")
                return False
        else:
            print("FAILED: Conversion failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("ERROR: Conversion timeout")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("DeepSeek-R1-Distill-Qwen-7B-Developer GGUF Conversion Fix")
    print("=" * 60)
    
    # Step 1: Fix tokenizer hash
    print("\nStep 1: Fixing tokenizer hash...")
    hash_fixed = fix_tokenizer_hash()
    
    # Step 2: Create tokenizer.model if needed
    print("\nStep 2: Creating tokenizer.model...")
    tokenizer_model_path = Path("D:/AI/Models/DeepSeek-R1-Distill-Qwen-7B-Developer/DeepSeek-R1-Distill-Qwen-7b-Developertokenizer.model")
    if not tokenizer_model_path.exists():
        create_simple_tokenizer_model()
    else:
        print("SUCCESS: tokenizer.model already exists")
    
    # Step 3: Run conversion
    print("\nStep 3: Running conversion...")
    success = run_conversion_with_fix()
    
    if success:
        print("\nConversion completed successfully!")
    else:
        print("\nConversion failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())