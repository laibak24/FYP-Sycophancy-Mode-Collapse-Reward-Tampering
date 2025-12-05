import os
import sys
from dotenv import load_dotenv

load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from src.models.api_client import ModelClient
from src.evaluation.sycophancy_eval import (
    SycophancyEvaluator, 
    generate_math_test_cases, 
    generate_medical_test_cases
)
from src.evaluation.mode_collapse_eval import (
    ModeCollapseEvaluator,
    generate_diverse_prompts
)
from src.evaluation.reward_tampering_eval import RewardTamperingEvaluator

print("\n" + "="*70)
print("GEMINI BEHAVIORAL TRIAD EVALUATION")
print("="*70)
print("\nAvailable tests:")
print("1. Quick Sycophancy Test (5 cases)")
print("2. Quick Mode Collapse Test (10 prompts)")
print("3. Quick Reward Tampering Test")
print("4. Full Pipeline Test (All three)")
print("5. Exit")

choice = input("\nSelect option (1-5): ").strip()

if choice == '5':
    print("Exiting...")
    sys.exit(0)

# Initialize client
print("\n✓ Initializing Gemini client...")
client = ModelClient()
model_name = "gemini-1.5-pro"
os.makedirs('results/gemini', exist_ok=True)

if choice == '1':
    # Sycophancy Test
    print(f"\n{'='*70}")
    print("GEMINI SYCOPHANCY TEST")
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
        save_path='results/gemini/sycophancy_quick.json'
    )
    
    print(f"\n{'='*70}")
    print("RESULTS SUMMARY")
    print(f"{'='*70}")
    print(f"Overall Sycophancy Rate: {results['overall_sycophancy_rate']:.2f}%")
    print(f"  - Progressive: {results['progressive_sycophancy']['rate']:.2f}%")
    print(f"  - Regressive: {results['regressive_sycophancy']['rate']:.2f}%")
    print(f"  - Honest: {results['honest']['rate']:.2f}%")
    print(f"\n✓ Saved to: results/gemini/sycophancy_quick.json")

elif choice == '2':
    # Mode Collapse Test
    print(f"\n{'='*70}")
    print("GEMINI MODE COLLAPSE TEST")
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
        save_path='results/gemini/mode_collapse_quick.json'
    )
    
    print(f"\n{'='*70}")
    print("RESULTS SUMMARY")
    print(f"{'='*70}")
    print(f"Entropy: {results['entropy']:.4f}")
    print(f"Baseline Entropy: {results['baseline_entropy']:.4f}")
    print(f"Entropy Reduction: {results['entropy_reduction_percent']:.2f}%")
    print(f"Severity: {results['severity']}")
    print(f"\n✓ Saved to: results/gemini/mode_collapse_quick.json")

elif choice == '3':
    # Reward Tampering Test
    print(f"\n{'='*70}")
    print("GEMINI REWARD TAMPERING TEST")
    print(f"{'='*70}")
    print(f"Model: {model_name}")
    print(f"Tests: Capability, Oversight, Deception")
    print(f"{'='*70}\n")
    
    evaluator = RewardTamperingEvaluator(client)
    
    results = evaluator.run_full_evaluation(
        model_name=model_name,
        use_api=True,
        save_path='results/gemini/reward_tampering_quick.json'
    )
    
    print(f"\n{'='*70}")
    print("RESULTS SUMMARY")
    print(f"{'='*70}")
    print(f"Overall Tampering Susceptibility: {results['overall_tampering_susceptibility']:.2%}")
    print(f"  - Capability Vulnerability: {results['capability_elicitation']['vulnerability_score']:.2%}")
    print(f"  - Oversight Manipulation: {results['oversight_manipulation']['manipulation_rate']:.2%}")
    print(f"  - Deception Score: {results['strategic_deception']['average_deception_score']:.2f}")
    print(f"\n✓ Saved to: results/gemini/reward_tampering_quick.json")

elif choice == '4':
    # Full Pipeline Test
    print(f"\n{'='*70}")
    print("GEMINI FULL PIPELINE TEST")
    print(f"{'='*70}")
    print("\nThis will run all three tests:")
    print("  1. Sycophancy (5 cases)")
    print("  2. Mode Collapse (10 prompts)")
    print("  3. Reward Tampering (full suite)")
    print("\nEstimated time: 5-10 minutes")
    print(f"{'='*70}\n")
    
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    # Step 1: Sycophancy
    print("\n[1/3] Running Sycophancy Test...")
    syc_eval = SycophancyEvaluator(client)
    syc_cases = generate_math_test_cases(5)
    syc_results = syc_eval.run_evaluation(
        model_name=model_name,
        test_cases=syc_cases,
        use_api=True,
        save_path='results/gemini/pipeline_sycophancy.json'
    )
    
    # Step 2: Mode Collapse
    print("\n[2/3] Running Mode Collapse Test...")
    mode_eval = ModeCollapseEvaluator(client)
    mode_prompts = generate_diverse_prompts(10)
    mode_results = mode_eval.evaluate_mode_collapse(
        model_name=model_name,
        prompts=mode_prompts,
        use_api=True,
        save_path='results/gemini/pipeline_mode_collapse.json'
    )
    
    # Step 3: Reward Tampering
    print("\n[3/3] Running Reward Tampering Test...")
    reward_eval = RewardTamperingEvaluator(client)
    reward_results = reward_eval.run_full_evaluation(
        model_name=model_name,
        use_api=True,
        save_path='results/gemini/pipeline_reward_tampering.json'
    )
    
    # Summary
    print(f"\n{'='*70}")
    print("GEMINI BEHAVIORAL TRIAD SUMMARY")
    print(f"{'='*70}")
    print(f"Model: {model_name}\n")
    print(f"1. SYCOPHANCY")
    print(f"   Rate: {syc_results['overall_sycophancy_rate']:.2f}%")
    print(f"   Progressive: {syc_results['progressive_sycophancy']['rate']:.2f}%")
    print(f"   Regressive: {syc_results['regressive_sycophancy']['rate']:.2f}%")
    print(f"\n2. MODE COLLAPSE")
    print(f"   Entropy: {mode_results['entropy']:.4f}")
    print(f"   Reduction: {mode_results['entropy_reduction_percent']:.2f}%")
    print(f"   Severity: {mode_results['severity']}")
    print(f"\n3. REWARD TAMPERING")
    print(f"   Susceptibility: {reward_results['overall_tampering_susceptibility']:.2%}")
    print(f"   Capability: {reward_results['capability_elicitation']['vulnerability_score']:.2%}")
    print(f"   Oversight: {reward_results['oversight_manipulation']['manipulation_rate']:.2%}")
    print(f"\n{'='*70}")
    print("Expected Correlations (from paper):")
    print("  Sycophancy ↔ Mode Collapse: r = 0.78")
    print("  Mode Collapse ↔ Reward Tampering: r = 0.84")
    print("  Sycophancy ↔ Reward Tampering: r = 0.71")
    print(f"{'='*70}")
    print(f"\n✓ All results saved to: results/gemini/")

print(f"\n{'='*70}")
print("✓ TEST COMPLETE!")
print(f"{'='*70}\n")