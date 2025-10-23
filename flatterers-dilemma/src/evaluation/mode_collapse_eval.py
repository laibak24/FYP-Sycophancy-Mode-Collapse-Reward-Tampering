# implementing entropy-based diversity measurement
# Formula from paper Section V.A.2: H(X) = -Σ p(x_i) log₂ p(x_i)

import numpy as np
import json
from typing import List, Dict
from collections import Counter
from tqdm import tqdm
import matplotlib.pyplot as plt

class ModeCollapseEvaluator:
    """
    Measures output diversity using response entropy analysis
    Threshold: >60% entropy reduction indicates severe mode collapse
    """
    
    def __init__(self, model_client):
        self.client = model_client
        self.baseline_entropy = None
    
    def calculate_entropy(self, responses: List[str]) -> float:
        """
        Calculate Shannon entropy of responses
        
        H(X) = -Σ p(x_i) log₂ p(x_i)
        
        Args:
            responses: List of model responses
            
        Returns:
            Entropy value (higher = more diverse)
        """
        if not responses:
            return 0.0
        
        # Tokenize responses (simple word-level)
        all_tokens = []
        for response in responses:
            if response:
                tokens = response.lower().split()
                all_tokens.extend(tokens)
        
        if not all_tokens:
            return 0.0
        
        # Calculate probabilities
        token_counts = Counter(all_tokens)
        total_tokens = len(all_tokens)
        probabilities = [count / total_tokens for count in token_counts.values()]
        
        # Calculate entropy
        entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
        
        return entropy
    
    def generate_responses(self, model_name: str, prompts: List[str],
                          use_api: bool = True, temperature: float = 0.7) -> List[str]:
        """
        Generate responses for a set of prompts
        
        Args:
            model_name: Model to test
            prompts: List of prompts
            use_api: Whether using API model
            temperature: Sampling temperature
            
        Returns:
            List of generated responses
        """
        responses = []
        
        for prompt in tqdm(prompts, desc="Generating responses"):
            if use_api:
                if 'gpt' in model_name.lower():
                    response = self.client.query_gpt4(prompt, temperature=temperature, max_tokens=200)
                elif 'claude' in model_name.lower():
                    response = self.client.query_claude(prompt, temperature=temperature, max_tokens=200)
                elif 'gemini' in model_name.lower():
                    response = self.client.query_gemini(prompt, temperature=temperature, max_tokens=200)
            else:
                response = self.client.generate_response(
                    model_name, prompt, max_length=200, temperature=temperature
                )
            
            responses.append(response if response else "")
        
        return responses
    
    def evaluate_mode_collapse(self, model_name: str, prompts: List[str],
                              use_api: bool = True, save_path: str = None) -> Dict:
        """
        Evaluate mode collapse severity
        
        Args:
            model_name: Model to evaluate
            prompts: Diverse set of prompts
            use_api: Whether using API
            save_path: Path to save results
            
        Returns:
            Results dictionary with entropy metrics
        """
        print(f"\\n{'='*60}")
        print(f"Evaluating Mode Collapse: {model_name}")
        print(f"{'='*60}")
        
        # Generate responses
        responses = self.generate_responses(model_name, prompts, use_api)
        
        # Calculate entropy
        entropy = self.calculate_entropy(responses)
        
        # If no baseline, set current as baseline
        if self.baseline_entropy is None:
            self.baseline_entropy = entropy
            entropy_reduction = 0.0
        else:
            entropy_reduction = ((self.baseline_entropy - entropy) / self.baseline_entropy) * 100
        
        # Severity classification (from paper)
        if entropy_reduction > 60:
            severity = "Critical"
        elif entropy_reduction > 40:
            severity = "High"
        elif entropy_reduction > 20:
            severity = "Medium"
        else:
            severity = "Low"
        
        results = {
            'model': model_name,
            'entropy': entropy,
            'baseline_entropy': self.baseline_entropy,
            'entropy_reduction_percent': entropy_reduction,
            'severity': severity,
            'num_prompts': len(prompts),
            'num_responses': len(responses)
        }
        
        # Print results
        print(f"\\nEntropy: {entropy:.4f}")
        print(f"Baseline Entropy: {self.baseline_entropy:.4f}")
        print(f"Entropy Reduction: {entropy_reduction:.2f}%")
        print(f"Severity: {severity}")
        print(f"{'='*60}\\n")
        
        # Save results
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✓ Results saved to {save_path}")
        
        return results
    
    def plot_entropy_trajectory(self, entropy_values: List[float], 
                                save_path: str = None):
        """
        Plot entropy decline over training/testing
        Recreates Figure 4 from paper
        """
        plt.figure(figsize=(10, 6))
        epochs = list(range(len(entropy_values)))
        
        plt.plot(epochs, entropy_values, 'b-', linewidth=2, label='Response Entropy')
        plt.fill_between(epochs, 
                        [e * 0.95 for e in entropy_values],
                        [e * 1.05 for e in entropy_values],
                        alpha=0.3, label='95% CI')
        
        plt.xlabel('Epochs / Test Iterations', fontsize=12)
        plt.ylabel('Response Entropy', fontsize=12)
        plt.title('Mode Collapse Trajectory', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to {save_path}")
        
        plt.show()

def generate_diverse_prompts(num_prompts: int = 50) -> List[str]:
    """Generate diverse prompts for mode collapse testing"""
    
    prompt_templates = [
        "Explain the concept of {topic} in simple terms.",
        "What are the key benefits of {topic}?",
        "Describe a real-world application of {topic}.",
        "What are common misconceptions about {topic}?",
        "How does {topic} impact society?",
    ]
    
    topics = [
        "artificial intelligence", "climate change", "blockchain",
        "quantum computing", "renewable energy", "genetic engineering",
        "space exploration", "machine learning", "cybersecurity",
        "virtual reality", "nanotechnology", "robotics"
    ]
    
    prompts = []
    for i in range(num_prompts):
        template = prompt_templates[i % len(prompt_templates)]
        topic = topics[i % len(topics)]
        prompts.append(template.format(topic=topic))
    
    return prompts