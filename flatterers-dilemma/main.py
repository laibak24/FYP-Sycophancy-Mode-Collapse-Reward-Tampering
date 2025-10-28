import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("="*70)
print("LLM BEHAVIORAL TRIAD EVALUATION")
print("="*70)

# Test imports with proper error handling
print("\n[Step 1] Testing imports...")

ModelClient = None
HFModelLoader = None
SycophancyEvaluator = None
ModeCollapseEvaluator = None
RewardTamperingEvaluator = None
generate_math_test_cases = None
generate_medical_test_cases = None
generate_diverse_prompts = None

# Try importing ModelClient
try:
    from src.models.api_client import ModelClient
    print("✓ ModelClient imported successfully")
except Exception as e:
    print(f"✗ Failed to import ModelClient: {e}")

# Try importing HFModelLoader (may fail due to torch)
try:
    from src.models.hf_loader import HFModelLoader
    print("✓ HFModelLoader imported successfully")
except Exception as e:
    print(f"⚠ HFModelLoader not available (PyTorch issue - this is OK for API-only mode)")
    print(f"  Error: {str(e)[:100]}...")

# Try importing evaluation modules
try:
    from src.evaluation.sycophancy_eval import (
        SycophancyEvaluator, 
        generate_math_test_cases, 
        generate_medical_test_cases
    )
    print("✓ SycophancyEvaluator imported successfully")
except Exception as e:
    print(f"✗ Failed to import SycophancyEvaluator: {e}")

try:
    from src.evaluation.mode_collapse_eval import (
        ModeCollapseEvaluator,
        generate_diverse_prompts
    )
    print("✓ ModeCollapseEvaluator imported successfully")
except Exception as e:
    print(f"✗ Failed to import ModeCollapseEvaluator: {e}")

try:
    from src.evaluation.reward_tampering_eval import RewardTamperingEvaluator
    print("✓ RewardTamperingEvaluator imported successfully")
except Exception as e:
    print(f"✗ Failed to import RewardTamperingEvaluator: {e}")

# Check if .env exists
from dotenv import load_dotenv
load_dotenv()

env_path = os.path.join(current_dir, '.env')
env_exists = os.path.exists(env_path)

if env_exists:
    print("\n✓ .env file found")
    # Check if keys are set
    has_openai = bool(os.getenv('OPENAI_API_KEY')) and os.getenv('OPENAI_API_KEY') != 'your_openai_key_here'
    has_anthropic = bool(os.getenv('ANTHROPIC_API_KEY')) and os.getenv('ANTHROPIC_API_KEY') != 'your_anthropic_key_here'
    has_google = bool(os.getenv('GOOGLE_API_KEY')) and os.getenv('GOOGLE_API_KEY') != 'your_google_key_here'
    
    if has_openai:
        print("  ✓ OpenAI API key configured")
    else:
        print("  ⚠ OpenAI API key not configured")
    
    if has_anthropic:
        print("  ✓ Anthropic API key configured")
    else:
        print("  ⚠ Anthropic API key not configured")
    
    if has_google:
        print("  ✓ Google API key configured")
    else:
        print("  ⚠ Google API key not configured")
else:
    print("\n⚠ .env file not found")
    print("  Creating template .env file...")
    with open(env_path, 'w') as f:
        f.write("# Add your API keys below\n")
        f.write("OPENAI_API_KEY=your_openai_key_here\n")
        f.write("ANTHROPIC_API_KEY=your_anthropic_key_here\n")
        f.write("GOOGLE_API_KEY=your_google_key_here\n")
    print("  ✓ Created .env template")
    print("  Please edit .env and add your API keys")
    has_openai = has_anthropic = has_google = False

print("\n" + "="*70)
print("SETUP STATUS")
print("="*70)

# Check what's available
can_use_api = ModelClient is not None
can_use_hf = HFModelLoader is not None
can_evaluate = all([SycophancyEvaluator, ModeCollapseEvaluator, RewardTamperingEvaluator])
has_test_generators = all([generate_math_test_cases, generate_medical_test_cases, generate_diverse_prompts])

print(f"API Models (GPT, Claude, Gemini): {'✓ Available' if can_use_api else '✗ Not Available'}")
print(f"HuggingFace Models: {'✓ Available' if can_use_hf else '⚠ Not Available (PyTorch issue)'}")
print(f"Evaluation Modules: {'✓ Available' if can_evaluate else '✗ Not Available'}")
print(f"Test Case Generators: {'✓ Available' if has_test_generators else '✗ Not Available'}")

if not can_use_api and not can_use_hf:
    print("\n✗ No model clients available. Please check your setup.")
    sys.exit(1)

if not can_evaluate:
    print("\n✗ Evaluation modules not available. Please check your setup.")
    sys.exit(1)

print("\n" + "="*70)
print("SELECT EVALUATION MODE")
print("="*70)
print("1. Generate Sample Test Cases (No API keys needed)")
print("2. Quick Sycophancy Test - GPT-4 (Requires OpenAI API key)")
print("3. Quick Mode Collapse Test - GPT-4 (Requires OpenAI API key)")
print("4. Quick Reward Tampering Test - GPT-4 (Requires OpenAI API key)")
print("5. Full Single Model Evaluation (Requires API key)")
print("6. Compare Multiple Models (Requires API keys)")
print("7. Check System Requirements")
print("8. Exit")

choice = input("\nSelect option (1-8): ").strip()

if choice == '8':
    print("Exiting...")
    sys.exit(0)

elif choice == '1':
    # Generate sample test cases - NO API NEEDED
    print("\n" + "="*70)
    print("GENERATING SAMPLE TEST CASES")
    print("="*70)
    
    if not has_test_generators:
        print("✗ Test generators not available")
        sys.exit(1)
    
    os.makedirs('sample_data', exist_ok=True)
    
    print("\nGenerating test cases...")
    math_cases = generate_math_test_cases(10)
    medical_cases = generate_medical_test_cases(10)
    diverse_prompts = generate_diverse_prompts(20)
    
    import json
    
    # Save to files
    with open('sample_data/math_cases.json', 'w') as f:
        json.dump(math_cases, f, indent=2)
    print(f"✓ Saved math_cases.json")
    
    with open('sample_data/medical_cases.json', 'w') as f:
        json.dump(medical_cases, f, indent=2)
    print(f"✓ Saved medical_cases.json")
    
    with open('sample_data/diverse_prompts.json', 'w') as f:
        json.dump(diverse_prompts, f, indent=2)
    print(f"✓ Saved diverse_prompts.json")
    
    print(f"\n✓ Generated {len(math_cases)} math test cases")
    print(f"✓ Generated {len(medical_cases)} medical test cases")
    print(f"✓ Generated {len(diverse_prompts)} diverse prompts")
    print(f"\n✓ All files saved to sample_data/ directory")
    
    print("\n" + "="*70)
    print("SAMPLE PREVIEWS")
    print("="*70)
    
    print("\n[Math Test Case Example]")
    print(f"  Question: {math_cases[0]['question']}")
    print(f"  Correct Answer: {math_cases[0]['correct_answer']}")
    print(f"  Incorrect Answer: {math_cases[0]['incorrect_answer']}")
    
    print("\n[Medical Test Case Example]")
    print(f"  Question: {medical_cases[0]['question']}")
    print(f"  Correct Answer: {medical_cases[0]['correct_answer']}")
    print(f"  Incorrect Answer: {medical_cases[0]['incorrect_answer']}")
    
    print("\n[Diverse Prompt Examples]")
    for i in range(min(3, len(diverse_prompts))):
        print(f"  {i+1}. {diverse_prompts[i]}")

elif choice == '7':
    # Check requirements
    print("\n" + "="*70)
    print("CHECKING SYSTEM REQUIREMENTS")
    print("="*70)
    
    required_packages = {
        'Core Dependencies': [
            'numpy', 'pandas', 'matplotlib', 'seaborn', 'tqdm', 'python-dotenv'
        ],
        'API Clients': [
            'openai', 'anthropic', 'google-generativeai'
        ],
        'ML/NLP (Optional for HuggingFace)': [
            'torch', 'transformers'
        ]
    }
    
    for category, packages in required_packages.items():
        print(f"\n{category}:")
        for package in packages:
            try:
                __import__(package.replace('-', '_').replace('.', '_'))
                print(f"  ✓ {package}")
            except ImportError:
                print(f"  ✗ {package} - Install with: pip install {package}")

elif choice in ['2', '3', '4', '5', '6']:
    # Check for API setup
    if not can_use_api:
        print("\n✗ API client not available. Please check your setup.")
        sys.exit(1)
    
    if not has_openai:
        print("\n✗ OpenAI API key not configured in .env file")
        print("  Please edit .env and add: OPENAI_API_KEY=your_actual_key")
        sys.exit(1)
    
    print("\n✓ Initializing API client...")
    try:
        client = ModelClient()
        print("✓ Client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        sys.exit(1)
    
    os.makedirs('results', exist_ok=True)
    model_name = "gpt-4o"
    
    if choice == '2':
        # Sycophancy test
        print(f"\n{'='*70}")
        print("RUNNING QUICK SYCOPHANCY TEST")
        print(f"{'='*70}")
        print(f"Model: {model_name}")
        print(f"Test cases: 5 math problems")
        print(f"{'='*70}\n")
        
        evaluator = SycophancyEvaluator(client)
        test_cases = generate_math_test_cases(5)
        
        results = evaluator.run_evaluation(
            model_name=model_name,
            test_cases=test_cases,
            use_api=True,
            save_path='results/quick_sycophancy_test.json'
        )
        
        print(f"\n✓ Test complete!")
        print(f"✓ Results saved to: results/quick_sycophancy_test.json")
        
    elif choice == '3':
        # Mode collapse test
        print(f"\n{'='*70}")
        print("RUNNING QUICK MODE COLLAPSE TEST")
        print(f"{'='*70}")
        print(f"Model: {model_name}")
        print(f"Prompts: 10 diverse topics")
        print(f"{'='*70}\n")
        
        evaluator = ModeCollapseEvaluator(client)
        prompts = generate_diverse_prompts(10)
        
        results = evaluator.evaluate_mode_collapse(
            model_name=model_name,
            prompts=prompts,
            use_api=True,
            save_path='results/quick_mode_collapse_test.json'
        )
        
        print(f"\n✓ Test complete!")
        print(f"✓ Results saved to: results/quick_mode_collapse_test.json")
        
    elif choice == '4':
        # Reward tampering test
        print(f"\n{'='*70}")
        print("RUNNING QUICK REWARD TAMPERING TEST")
        print(f"{'='*70}")
        print(f"Model: {model_name}")
        print(f"Tests: Capability elicitation, oversight manipulation, strategic deception")
        print(f"{'='*70}\n")
        
        evaluator = RewardTamperingEvaluator(client)
        
        results = evaluator.run_full_evaluation(
            model_name=model_name,
            use_api=True,
            save_path='results/quick_reward_tampering_test.json'
        )
        
        print(f"\n✓ Test complete!")
        print(f"✓ Results saved to: results/quick_reward_tampering_test.json")
        
    elif choice == '5':
        # Full single model evaluation
        print(f"\n{'='*70}")
        print("RUNNING FULL SINGLE MODEL EVALUATION")
        print(f"{'='*70}")
        print(f"Model: {model_name}")
        print(f"This will run all three evaluation types")
        print(f"Estimated time: 5-10 minutes")
        print(f"{'='*70}\n")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            sys.exit(0)
        
        try:
            from src.evaluation.pipeline import EvaluationPipeline
            
            pipeline = EvaluationPipeline(client, results_dir='results/baseline')
            
            results = pipeline.evaluate_single_model(
                model_name=model_name,
                use_api=True,
                num_sycophancy_cases=15,
                num_diversity_prompts=25
            )
            
            print(f"\n✓ Full evaluation complete!")
            print(f"✓ Results saved to: results/baseline/{model_name}/")
            
        except Exception as e:
            print(f"\n✗ Error during evaluation: {e}")
            import traceback
            traceback.print_exc()
    
    elif choice == '6':
        # Multiple models comparison
        print(f"\n{'='*70}")
        print("COMPARE MULTIPLE MODELS")
        print(f"{'='*70}")
        print("\nAvailable models:")
        print("1. GPT-4o (OpenAI)")
        print("2. Claude Sonnet 4 (Anthropic)")
        print("3. Gemini 1.5 Pro (Google)")
        print("\nNote: This requires API keys for all selected models")
        print("Estimated time: 15-30 minutes for all three")
        print(f"{'='*70}\n")
        
        model_selection = input("Enter model numbers to test (e.g., 1,2,3 or 1,2): ").strip()
        
        model_configs = []
        if '1' in model_selection:
            if has_openai:
                model_configs.append({'name': 'gpt-4o', 'use_api': True})
            else:
                print("⚠ Skipping GPT-4o (no API key)")
        
        if '2' in model_selection:
            if has_anthropic:
                model_configs.append({'name': 'claude-sonnet-4-20250514', 'use_api': True})
            else:
                print("⚠ Skipping Claude (no API key)")
        
        if '3' in model_selection:
            if has_google:
                model_configs.append({'name': 'gemini-1.5-pro', 'use_api': True})
            else:
                print("⚠ Skipping Gemini (no API key)")
        
        if not model_configs:
            print("✗ No models available with current API keys")
            sys.exit(1)
        
        print(f"\nWill evaluate {len(model_configs)} model(s)")
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            sys.exit(0)
        
        try:
            from src.evaluation.pipeline import EvaluationPipeline
            
            pipeline = EvaluationPipeline(client, results_dir='results/baseline')
            
            results = pipeline.evaluate_multiple_models(model_configs)
            
            print(f"\n✓ Multi-model evaluation complete!")
            print(f"✓ Comparison table saved to: results/baseline/model_comparison.csv")
            print(f"✓ Comparison plots saved to: results/baseline/comparison_plots.png")
            
        except Exception as e:
            print(f"\n✗ Error during evaluation: {e}")
            import traceback
            traceback.print_exc()

print("\n" + "="*70)
print("✓ DONE!")
print("="*70)