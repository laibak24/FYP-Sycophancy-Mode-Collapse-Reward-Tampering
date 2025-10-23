"""
HuggingFace Model Loader for Open-Source LLMs
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

class HFModelLoader:
    def __init__(self):
        """Initialize HuggingFace model loader"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✓ Using device: {self.device}")
        
        self.models = {}
        self.tokenizers = {}
    
    def load_model(self, model_name, cache_dir="/content/FYP-Sycophancy-Mode-Collapse-Reward-Tampering/flatterers-dilemma/models"):
        """Load a model from HuggingFace"""
        if model_name in self.models:
            print(f"✓ {model_name} already loaded")
            return self.models[model_name], self.tokenizers[model_name]
        
        print(f"Loading {model_name}...")
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=cache_dir
            )
            
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            if self.device == "cpu":
                model = model.to(self.device)
            
            self.models[model_name] = model
            self.tokenizers[model_name] = tokenizer
            
            print(f"✓ Successfully loaded {model_name}")
            return model, tokenizer
            
        except Exception as e:
            print(f"✗ Error loading {model_name}: {e}")
            return None, None
    
    def generate_response(self, model_name, prompt, max_length=200, temperature=0.7):
        """Generate response from a loaded model"""
        model, tokenizer = self.load_model(model_name)
        
        if model is None:
            return None
        
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response[len(prompt):].strip()
        
        return response
    
    def unload_model(self, model_name):
        """Unload a model to free up memory"""
        if model_name in self.models:
            del self.models[model_name]
            del self.tokenizers[model_name]
            torch.cuda.empty_cache()
            print(f"✓ Unloaded {model_name}")
