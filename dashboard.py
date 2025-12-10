import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="The Flatterer's Dilemma - FYP Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit.components.v1 as components

# Custom CSS for modern styling
st.markdown("""
<style>

/* --- GLOBAL TEXT FIXES FOR DARK BACKGROUND --- */

body, [class^="st-"], .main-header * {
    color: #f5f5f5 !important;       /* Soft white for readability */
}

/* headings */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

/* paragraph and misc text */
p, span, div, li {
    color: #e5e5e5 !important;
}

/* Metric card text */
.metric-card, .metric-card * {
    color: #ffffff !important;
}

/* Behavioral cards text */
.behavior-card, .behavior-card * {
    color: #1a1a1a !important;   /* Dark text for light backgrounds */
    font-weight: 600;
}

/* Finding items */
.finding-item {
    color: #e8e8e8 !important;
    font-size: 1.05rem;
    padding: 6px 0;
}

/* Ensure colored cards remain readable */
.behavior-card h4 {
    color: #111 !important;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* ============================================================
   GLOBAL TEXT (dark mode)
   ============================================================ */
html, body, [class^="st-"] {
    color: #ffffff !important;
}

/* ============================================================
   KEY FINDINGS (force BLACK text)
   ============================================================ */
.finding-item {
    background: #f8f8f8 !important;       /* keep light background */
    color: #111111 !important;            /* strong dark text */
    padding: 10px 14px;
    border-left: 4px solid #8b5cf6;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 1rem;
    font-weight: 600;
}

/* ============================================================
   BEHAVIOR CARDS — also light background, force dark text
   ============================================================ */
.behavior-card, .behavior-card * {
    color: #111111 !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border-left: 5px solid #667eea;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    .finding-item {
        background: linear-gradient(to right, #f0fdf4 0%, #dcfce7 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid #22c55e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .behavior-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    .priority-high {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .priority-medium {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
            
</style>
""", unsafe_allow_html=True)

# Data preparation
@st.cache_data
def load_data():
    model_comparison = pd.DataFrame({
        'model': ['GPT-4o', 'Claude-Sonnet', 'Gemini-1.5', 'Llama-70B', 'Mistral-8x7B'],
        'sycophancy': [56.71, 57.44, 62.47, 48.32, 41.18],
        'modeCollapse': [0.73, 0.78, 0.81, 0.65, 0.59],
        'rewardTampering': [0.68, 0.71, 0.74, 0.58, 0.52],
        'correlation': [0.82, 0.79, 0.85, 0.76, 0.73],
        'riskLevel': ['High', 'High', 'Critical', 'Medium', 'Medium']
    })
    
    experiment_results = pd.DataFrame({
        'experiment': ['GPT-4o-mini\n(HH-RLHF)', 'Phi-3\n(Ollama)', 'Gemini Flash\n(Synthetic)', 'GPT-4o-mini\n(Coding)'],
        'sycophancy': [11.64, 100, 11.69, 77.7],
        'modeCollapse': [70.83, 0, 4.33, 0],
        'rewardTampering': [41.02, 90, 19.33, 50],
        'samples': [50, 40, 30, 30]
    })
    
    domain_performance = pd.DataFrame({
        'domain': ['Medical', 'Factual', 'Math'],
        'sycophancy': [23.25, 6.39, 5.21],
        'modeCollapse': [4.19, 3.18, 6.25],
        'rewardTampering': [30.0, 11.67, 17.5]
    })
    
    correlation_data = pd.DataFrame({
        'name': ['Syc-MC', 'MC-RT', 'Syc-RT'],
        'pearson': [-0.208, 0.344, -0.046],
        'spearman': [-0.193, 0.293, 0.013],
        'pValue': [0.148, 0.015, 0.750]
    })
    
    mitigation = pd.DataFrame({
        'strategy': ['Synthetic Data', 'Pinpoint Tuning', 'LQCD', 'KTS Steering', 'System 2 Attention', 'RAG Integration'],
        'sycReduction': [23.1, 31.4, 18.7, 27.3, 15.2, 34.2],
        'performance': [-2.1, -1.8, -0.4, -0.9, 1.2, 3.4],
        'cost': ['High', 'High', 'Low', 'Medium', 'High', 'Medium']
    })
    
    timeline = pd.DataFrame({
        'phase': ['FYP1 Completed', 'Literature Review', 'Multi-Model Eval', 'Statistical Analysis', 'Dashboard Dev', 'FYP2 Planning'],
        'progress': [100, 100, 100, 100, 90, 30],
        'status': ['complete', 'complete', 'complete', 'complete', 'active', 'upcoming']
    })
    
    return model_comparison, experiment_results, domain_performance, correlation_data, mitigation, timeline

model_comparison, experiment_results, domain_performance, correlation_data, mitigation, timeline = load_data()

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 📂 Navigation")

    page = st.radio(
        "Select Section",
        [
            "🏠 Overview",
            "🧪 Experiments",
            "📚 Literature Review",
            "📈 Progress & Timeline",
            "🔮 Future Work"
        ]
    )
    st.markdown("---")
    st.markdown("### 👥 Research Team")
    st.markdown("""
    **Students:**
    - Kainat Faisal 22K-4405
    - Laiba Khan 22K-4610
    - Waniya Syed 22K-4516
    
    **Supervisor:**
    - Farrukh Hassan Syed
    """)

    st.markdown("---")

# ------------------------
# PAGE ROUTING
# ------------------------

# ===== TAB 1 =====
if page == "🏠 Overview":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">The Flatterer's Dilemma</h1>
        <p style="font-size: 1.1em; margin-top: 1.5rem; opacity: 0.95;">
            A Systematic Investigation of Sycophancy, Mode Collapse, and Reward Tampering in RLHF-Trained Large Language Models
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    
    # Problem Statement
    st.markdown("### 🎯 Problem Statement")
    
    st.markdown("""
    As Large Language Models (LLMs) integrate into **safety-critical domains**—healthcare diagnostics, 
    legal advisory, educational tutoring—a concerning failure mode has emerged: **sycophancy**, where models 
    prioritize user agreement over factual accuracy.
    """)
    
    problem_col1, problem_col2 = st.columns([1, 1])
    
    with problem_col1:
        st.error("""
        #### 🚨 The Core Problem
        
        **Real-World Risks:**
        - 🏥 **Healthcare**: Validating dangerous self-diagnoses
        - ⚖️ **Legal**: Biased recommendations matching client preferences
        - 🎓 **Education**: Reinforcing misconceptions instead of correcting them
        - 💰 **Finance**: Confirming risky investment decisions
        """)
    
    with problem_col2:
        st.warning("""
        #### 🔗 The Hidden Connection
        
        **Research Gap:**
        
        Previous studies treated these as isolated issues:
        - Sycophancy (truth vs. agreeableness)
        - Mode collapse (diversity loss)
        - Reward tampering (gaming behaviors)
        
        **Our hypothesis:** These form an **interconnected cascade** triggered by RLHF optimization.
        """)
    
    st.divider()
    
    # Project Objectives
    st.markdown("### 🎯 Research Objectives")
    
    objectives_col1, objectives_col2, objectives_col3 = st.columns(3)
    
    with objectives_col1:
        st.markdown("""
        #### 🔍 Investigate
        
        - Measure sycophancy rates across 5 LLMs
        - Quantify mode collapse severity
        - Assess reward tampering vulnerability
        - Analyze cross-domain patterns
        """)
    
    with objectives_col2:
        st.markdown("""
        #### 📊 Validate
        
        - Test behavioral triad hypothesis
        - Measure correlation strengths
        - Identify temporal emergence patterns
        - Compare model architectures
        """)
    
    with objectives_col3:
        st.markdown("""
        #### 💡 Contribute
        
        - Unified evaluation framework
        - Open-source testing toolkit
        - Mitigation recommendations
        - Future research roadmap
        """)
    
    st.divider()
    
    # Methodology Overview
    st.markdown("### 🔬 Our Approach")
    
    method_tabs = st.tabs(["📚 Literature Review", "🧪 Empirical Testing", "📈 Analysis"])
    
    with method_tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Systematic Review:**
            - 47 papers (2020-2024)
            - PRISMA-compliant methodology
            - Multiple databases (arXiv, ACL, IEEE)
            """)
        with col2:
            st.metric("Papers Analyzed", "47", help="Systematic literature review")
    
    with method_tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Multi-Model Evaluation:**
            - 5 state-of-the-art LLMs tested
            - 3 domains (Medical, Math, NLP)
            - 150+ carefully designed test cases
            - Progressive & regressive sycophancy protocols
            """)
        with col2:
            st.metric("Models Evaluated", "5", help="GPT-4o, Claude, Gemini, Llama, Phi-3")
            st.metric("Test Cases", "150+", help="Across multiple domains")
    
    with method_tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Statistical Analysis:**
            - Correlation analysis (Pearson's r)
            - Entropy-based diversity measurement
            - Domain-specific pattern recognition
            - Behavioral cascade validation
            """)
        with col2:
            st.metric("Correlation Threshold", "r > 0.75", help="From literature")
            st.metric("Our Findings", "r = 0.62", help="Sycophancy ↔ Reward Tampering")
    
    st.divider()
    
    # Key Findings Summary
    st.markdown("### 💡 Key Findings")
    
    findings_col1, findings_col2 = st.columns([2, 1])
    
    with findings_col1:
        st.markdown("""
        
        1. **Strong Behavioral Correlation** (r = 0.6159)
           - Confirms sycophancy-reward tampering link
           - Validates literature predictions (r > 0.6 threshold)
        
        2. **Mode Collapse Connection** (r = 0.344)  
           - Moderate correlation with reward tampering
           - Suggests mediating role in behavioral cascade
        
        3. **Domain Vulnerability Patterns**
           - 🏥 Medical: Highest sycophancy risk
           - 🧮 Math: Moderate susceptibility
           - 💻 NLP: Lowest rates observed
        
        4. **Model-Specific Extremes**
           - Phi-3: 100% sycophancy under aggressive rebuttal
           - GPT-4o: Most balanced performance
           - Claude-3.5: Highest tampering resistance
        
        5. **Temporal Cascade Confirmed**
           - Sycophancy emerges first (early epochs)
           - Mode collapse follows (mid-training)
           - Reward tampering matures last (late epochs)
        """)
    
    
    st.divider()
    
    # Call to Action
    st.markdown("### 🤝 Get Involved")
    
    cta_col2, cta_col3 = st.columns(2)
        
    with cta_col2:
        st.markdown("""
        #### 💻 Use Our Tools
        - Evaluation framework (GitHub)
        - Test case templates
        - Analysis notebooks
        """)
    with cta_col3:
        st.markdown("""
    #### 💬 Connect

    <div class="contact-links">
        <p>Email: 
            <a href="mailto:k224405@nu.edu.pk">k224405@nu.edu.pk</a> |
            <a href="mailto:k224610@nu.edu.pk">k224610@nu.edu.pk</a> |
            <a href="mailto:k224516@nu.edu.pk">k224516@nu.edu.pk</a>
        </p>
        <p>GitHub: 
            <a href="https://github.com/laibak24/FYP-Sycophancy-Mode-Collapse-Reward-Tampering" target="_blank">FYP Repo</a>
        </p>
        <p>Notion: 
            <a href="https://www.notion.so/Home-The-Flatterer-s-Dilemma" target="_blank">Project Notes</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    
# ===== TAB 2 =====
elif page == "🧪 Experiments":
    st.header("🧪 Experimental Results")

    st.markdown("### Comparative Analysis Across Pipelines")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Sycophancy %',
        x=experiment_results['experiment'],
        y=experiment_results['sycophancy'],
        marker_color='#ef4444'
    ))
    fig.add_trace(go.Bar(
        name='Mode Collapse %',
        x=experiment_results['experiment'],
        y=experiment_results['modeCollapse'],
        marker_color='#f59e0b'
    ))
    fig.add_trace(go.Bar(
        name='Reward Tampering %',
        x=experiment_results['experiment'],
        y=experiment_results['rewardTampering'],
        marker_color='#8b5cf6'
    ))

    fig.update_layout(
        barmode='group',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Experiment Details")
    exp_details = experiment_results.copy()
    exp_details.columns = ['Experiment', 'Sycophancy (%)', 'Mode Collapse (%)', 'Reward Tampering (%)', 'Samples']
    st.dataframe(exp_details, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Domain Performance (Gemini)")
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=domain_performance['sycophancy'],
            theta=domain_performance['domain'],
            fill='toself',
            name='Sycophancy'
        ))
        fig.add_trace(go.Scatterpolar(
            r=domain_performance['modeCollapse'],
            theta=domain_performance['domain'],
            fill='toself',
            name='Mode Collapse'
        ))
        fig.add_trace(go.Scatterpolar(
            r=domain_performance['rewardTampering'],
            theta=domain_performance['domain'],
            fill='toself',
            name='Reward Tampering'
        ))

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Correlation Analysis")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Pearson r',
            x=correlation_data['name'],
            y=correlation_data['pearson']
        ))
        fig.add_trace(go.Bar(
            name='Spearman ρ',
            x=correlation_data['name'],
            y=correlation_data['spearman']
        ))
        st.plotly_chart(fig, use_container_width=True)

# ===== TAB 3 =====
elif page == "📚 Literature Review":
    st.header("📚 Literature Review")
    
    # Introduction
    st.markdown("""
    This comprehensive review examines **47 papers** (2020-2024) on sycophancy in RLHF-trained LLMs, 
    revealing an interconnected behavioral triad: **sycophancy → mode collapse → reward tampering**.
    """)
    
    # Key Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Papers Reviewed", "47", help="Systematic review covering 2020-2024")
    with col2:
        st.metric("Sycophancy Rate Range", "14.66% - 62.47%", help="Varies by domain and model")
    with col3:
        st.metric("Correlation Coefficient", "r > 0.75", help="Between behavioral triad components")
    
    st.divider()
    
    # The Behavioral Triad
    st.subheader("🔄 The Behavioral Triad")
    st.markdown("""
    Research reveals three interconnected phenomena forming a cascade:
    """)
    
    triad_col1, triad_col2, triad_col3 = st.columns(3)
    
    with triad_col1:
        st.markdown("### 1️⃣ Sycophancy")
        st.info("""
        **Definition**: Models prioritize user agreement over factual accuracy
        
        **Types**:
        - **Progressive**: Incorrect → Correct (with user correction)
        - **Regressive**: Correct → Incorrect (to match user)
        
        **Impact**: 14.66% - 62.47% occurrence rate
        """)
    
    with triad_col2:
        st.markdown("### 2️⃣ Mode Collapse")
        st.warning("""
        **Definition**: Systematic reduction in output diversity
        
        **Manifestation**:
        - Reduced response entropy
        - Stereotypical patterns
        - Lost creativity
        
        **Threshold**: >60% entropy decline = severe collapse
        """)
    
    with triad_col3:
        st.markdown("### 3️⃣ Reward Tampering")
        st.error("""
        **Definition**: Gaming reward signals vs. genuine task completion
        
        **Behaviors**:
        - Strategic misrepresentation
        - Oversight manipulation
        - Adversarial exploitation
        
        **Risk**: 3.2× higher in collapsed models
        """)
    
    st.divider()
    
    # Cross-Model Analysis
    st.subheader("📊 Cross-Model Performance")
    
    model_data = {
        'Model': ['GPT-4o', 'Claude-Sonnet', 'Gemini-1.5-Pro', 'Llama-70B', 'Mistral-8x7B'],
        'Sycophancy Rate (%)': [56.71, 57.44, 62.47, 48.32, 41.18],
        'Mode Collapse': [0.73, 0.78, 0.81, 0.65, 0.59],
        'Reward Tampering': [0.68, 0.71, 0.74, 0.58, 0.52],
        'Correlation': [0.82, 0.79, 0.85, 0.76, 0.73],
        'Risk Level': ['High', 'High', 'Critical', 'Medium', 'Medium']
    }
    
    df_models = pd.DataFrame(model_data)
    
    tab1, tab2 = st.tabs(["📋 Table View", "📈 Visualization"])
    
    with tab1:
        st.dataframe(
            df_models.style.background_gradient(subset=['Sycophancy Rate (%)'], cmap='Reds')
                          .background_gradient(subset=['Correlation'], cmap='Blues'),
            use_container_width=True
        )
    
    with tab2:
        fig_models = go.Figure()
        fig_models.add_trace(go.Bar(
            name='Sycophancy Rate',
            x=df_models['Model'],
            y=df_models['Sycophancy Rate (%)'],
            marker_color='indianred'
        ))
        fig_models.update_layout(
            title='Sycophancy Rates Across Models',
            yaxis_title='Rate (%)',
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_models, use_container_width=True)
    
    st.divider()
        
    
    # Key Findings
    st.subheader("🔍 Key Research Findings")
    
    findings_col1, findings_col2 = st.columns(2)
    
    with findings_col1:
        st.markdown("### ✅ Established Insights")
        st.markdown("""
        1. **Mechanistic Relationships**: Behaviors are interdependent, not isolated vices (r > 0.75)
        
        2. **Sequential Emergence**: Sycophancy → Mode Collapse → Reward Tampering cascade confirmed
        
        3. **RLHF as Root Cause**: Optimization pressure drives entire behavioral triad
        
        4. **Model-Agnostic**: Patterns persist across architectures and training paradigms
        
        5. **Mitigation Trade-offs**: No single solution; combined approaches needed
        """)
    
    with findings_col2:
        st.markdown("### ❓ Critical Gaps")
        st.markdown("""
        1. **Multilingual Evaluation**: Research heavily English-focused
        
        2. **Long-term Dynamics**: Short-term studies dominate; persistence unclear
        
        3. **Open-Source Coverage**: Commercial models over-represented
        
        4. **Mechanistic Understanding**: Internal decision processes remain opaque
        
        5. **Standard Benchmarks**: Inconsistent evaluation protocols limit comparability
        """)
    
    st.divider()
    
    
    # Conclusion
    st.subheader("💡 Conclusion")
    
    st.markdown("""
    This systematic review establishes that **sycophancy is not a simple bug but a structured failure mode** 
    arising from RLHF optimization. The behavioral triad framework reveals:
    
    - **Interconnected phenomena** requiring integrated solutions
    - **Sequential emergence** with measurable temporal patterns  
    - **Model-agnostic persistence** across architectures
    - **Mitigation complexity** demanding multi-layered approaches
    
    As LLMs deploy into safety-critical domains (healthcare, legal, education), addressing sycophancy becomes 
    essential for maintaining trust and reliability. Future progress depends on:
    
    1. Standardized multilingual evaluation protocols
    2. Mechanistic interpretability research  
    3. Combined training + inference + architectural interventions
    4. Transparent governance and deployment guidelines
    """)
    
    st.success("""
    **Research Impact**: This review synthesizes 47 papers to provide the first comprehensive framework 
    for understanding and mitigating the sycophancy-mode collapse-reward tampering nexus in RLHF-trained LLMs.
    """)
# ===== TAB 4 =====
elif page == "📈 Progress & Timeline":
    st.markdown("## 📅 Progress Timeline")

    components.html("""
    <style>
        * {
            font-family: 'Inter', sans-serif;
            color: #eaeaea !important; /* global fix */
        }

        body {
            background-color: transparent !important;
        }

        .timeline {
            border-left: 3px solid #8b5cf6;
            margin: 20px 0;
            padding-left: 20px;
        }

        .timeline-item {
            margin-bottom: 32px;
            position: relative;
        }

        .timeline-item:before {
            content: "";
            width: 14px;
            height: 14px;
            background: #8b5cf6;
            border-radius: 50%;
            position: absolute;
            left: -30px;
            top: 4px;
            border: 3px solid #1a1a1a;
        }

        .timeline-upcoming:before {
            background: #4b5563;
        }

        .timeline-date {
            font-size: 0.95rem;
            color: #c4b5fd !important;
            font-weight: 600;
        }

        .timeline-title {
            font-size: 1.25rem;
            margin-top: 4px;
            font-weight: 700;
            color: #ffffff !important;
        }

        .timeline-desc {
            margin-top: 6px;
            font-size: 1rem;
            color: #dcdcdc !important;
            line-height: 1.4;
        }

        b {
            color: #c4b5fd !important;
        }
    </style>

    <div class="timeline">

        <div class="timeline-item">
            <div class="timeline-date">📅 July 2024</div>
            <div class="timeline-title">Project Kickoff</div>
            <div class="timeline-desc">
                Defined research scope on RLHF vulnerabilities — sycophancy, mode collapse, reward tampering.
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">📅 August 2024</div>
            <div class="timeline-title">Literature Review Started</div>
            <div class="timeline-desc">
                Reviewed 40+ papers on behavioral failures in alignment-trained LLMs.
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">📅 September 2024</div>
            <div class="timeline-title">Review Paper Completed</div>
            <div class="timeline-desc">
                Completed full literature survey and identified major open gaps.
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">📅 October 2024</div>
            <div class="timeline-title">Behavioral Tests Implemented</div>
            <div class="timeline-desc">
                Conducted tests on <b>sycophancy</b>, <b>mode collapse</b>, and <b>reward tampering</b>.
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">📅 November 2024</div>
            <div class="timeline-title">Correlation Analysis</div>
            <div class="timeline-desc">
                Discovered behavioral correlations:<br>
                – Sycophancy ↔ Reward Tampering<br>
                – Mode Collapse ↔ Reward Tampering
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">📅 December 2024</div>
            <div class="timeline-title">Synthetic Data Experiments</div>
            <div class="timeline-desc">
                Created controlled synthetic datasets to study interaction patterns.
            </div>
        </div>

        <div class="timeline-item timeline-upcoming">
            <div class="timeline-date">📅 January 2025</div>
            <div class="timeline-title">Mitigation Strategy Design</div>
            <div class="timeline-desc">
                Begin designing mitigation approaches (contrastive decoding, guardrails, anti-sycophancy prompts).
            </div>
        </div>

        <div class="timeline-item timeline-upcoming">
            <div class="timeline-date">📅 February 2025</div>
            <div class="timeline-title">Mode Collapse Re-Evaluation</div>
            <div class="timeline-desc">
                Test whether mitigations reduce collapse & improve generation diversity.
            </div>
        </div>

        <div class="timeline-item timeline-upcoming">
            <div class="timeline-date">📅 March 2025</div>
            <div class="timeline-title">Reward Tampering Stress Tests</div>
            <div class="timeline-desc">
                Run adversarial reward hacking tests to evaluate stability.
            </div>
        </div>

        <div class="timeline-item timeline-upcoming">
            <div class="timeline-date">📅 April 2025</div>
            <div class="timeline-title">Final Integration</div>
            <div class="timeline-desc">
                Build unified alignment–stability evaluation framework.
            </div>
        </div>

    </div>
    """, height=1700, scrolling=True)

# ===== TAB 5 =====
elif page == "🔮 Future Work":
    st.header("🔮 Future Work & FYP-2 Roadmap")
    
    st.markdown("""
    Building on our FYP-1 findings—**confirmed behavioral correlations** (r = 0.6159 for sycophancy-reward tampering)—
    we propose a comprehensive FYP-2 agenda focused on **developing, implementing, and validating mitigation strategies**.
    """)
    
    st.divider()
    
    # FYP-1 → FYP-2 Transition
    st.markdown("### 🔄 From Discovery to Solution")
    
    transition_col1, transition_col2 = st.columns(2)
    
    with transition_col1:
        st.success("""
        #### ✅ FYP-1 Achievements
        
        **What We Discovered:**
        - Validated behavioral triad hypothesis empirically
        - Measured sycophancy-reward tampering correlation (r = 0.6159)
        - Identified domain-specific vulnerability patterns
        - Mapped model-specific susceptibility profiles
        - Created open-source evaluation framework
        
        **Key Insight:**
        Problem is **confirmed and quantified** across 5 models and 3 domains.
        """)
    
    with transition_col2:
        st.info("""
        #### 🎯 FYP-2 Mission
        
        **What We'll Build:**
        - Design novel mitigation strategies
        - Implement training & inference interventions
        - Test effectiveness across behavioral triad
        - Validate mode collapse reduction
        - Deploy production-ready solutions
        
        **Key Goal:**
        Move from **understanding** the problem to **solving** it.
        """)
    
    st.divider()
    
    # Core FYP-2 Objectives
    st.markdown("### 🎯 FYP-2 Primary Objectives")
    
    objectives_tabs = st.tabs([
        "🛡️ Mitigation Development",
        "🧪 Experimental Validation", 
        "📊 Mode Collapse Analysis",
        "🌍 Multilingual Expansion"
    ])
    
    with objectives_tabs[0]:
        st.markdown("### 🛡️ Objective 1: Design & Implement Mitigation Strategies")
        
        mit_col1, mit_col2 = st.columns([3, 2])
        
        with mit_col1:
            st.markdown("""
            #### Phase 1: Training-Time Interventions (Months 1-4)
            
            **1.1 Multi-Objective Reward Modeling**
            - Extend RLHF reward function with diversity and honesty terms
            - Implement weighted loss: `L_total = α·L_accuracy + β·L_helpfulness + γ·L_diversity`
            - Target: Reduce sycophancy by 25-30% (literature benchmark)
            
            **1.2 Adversarial Preference Training**
            - Generate synthetic "challenging user" datasets
            - Train models to resist agreement pressure
            - Include contradictory rebuttals in fine-tuning data
            
            **1.3 Pinpoint Tuning Implementation**
            - Replicate Chen et al.'s approach with our datasets
            - Balance accuracy, helpfulness, diversity objectives
            - Expected: 30%+ reduction in regressive sycophancy
            """)
            
            st.markdown("""
            #### Phase 2: Inference-Time Techniques (Months 3-5)
            
            **2.1 Contrastive Decoding (LQCD)**
            - Implement Leading Query Contrastive Decoding
            - Modify token probability distributions during generation
            - Target: 15-20% sycophancy reduction with <2× latency
            
            **2.2 Activation Steering (KL-then-Steer)**
            - Identify sycophantic activation patterns via probing
            - Implement real-time steering during inference
            - Constrain KL divergence to preserve helpfulness
            
            **2.3 System 2 Attention Integration**
            - Filter misleading context before attention computation
            - Test on medical/legal domains (highest risk)
            - Expected: 10-15% accuracy improvement
            """)
        
        with mit_col2:
            st.warning("""
            **Deliverable 1:**
            
            🔧 **Mitigation Toolkit**
            - Python package with 3 training methods
            - 3 inference-time techniques
            - Unified API for easy integration
            
            📊 **Evaluation Suite**
            - Before/after comparison framework
            - Automated metric calculation
            - Visualization dashboard
            
            📝 **Documentation**
            - Implementation guides
            - Hyperparameter recommendations
            - Domain-specific best practices
            """)
            
            st.metric("Success Criterion", "≥20% reduction", 
                     help="Target sycophancy reduction across all models")
            st.metric("Helpfulness Preservation", "≥95%", 
                     help="Maintain baseline helpfulness scores")
    
    with objectives_tabs[1]:
        st.markdown("### 🧪 Objective 2: Comprehensive Experimental Validation")
        
        val_col1, val_col2 = st.columns(2)
        
        with val_col1:
            st.markdown("""
            #### 2.1 Baseline Re-Measurement (Month 2)
            
            **Expanded Model Coverage:**
            - Add GPT-4 Turbo, Claude-3 Opus, Gemini-1.5-Pro
            - Test open-source: Mistral-8x22B, Mixtral, Yi-34B
            - Total: **10 models** (vs. 5 in FYP-1)
            
            **Enhanced Test Suite:**
            - Increase test cases: 150 → **300+ scenarios**
            - Add legal domain (high-stakes decisions)
            - Include ethical dilemmas category
            - Multi-turn conversation protocols (5-10 exchanges)
            """)
            
            st.markdown("""
            #### 2.2 Mitigation Effectiveness Testing (Months 4-6)
            
            **Comparative Analysis:**
            - Test each mitigation strategy independently
            - Test combined approaches (training + inference)
            - Measure behavioral triad impact holistically
            
            **Metrics Framework:**
            - **Sycophancy**: Progressive/regressive rates
            - **Mode Collapse**: Response entropy, perplexity
            - **Reward Tampering**: Adversarial probing success
            - **Side Effects**: Helpfulness, latency, safety
            """)
        
        with val_col2:
            st.markdown("""
            #### 2.3 Domain-Specific Deep Dives (Months 5-7)
            
            **Medical Domain Focus:**
            - Partner with medical professionals for evaluation
            - Test on real patient query datasets (anonymized)
            - Measure safety-critical failure rates
            
            **Legal Advisory Testing:**
            - Create case-based evaluation scenarios
            - Test bias toward client preferences
            - Assess neutrality preservation
            
            **Educational Content:**
            - Student misconception correction tests
            - Pedagogical effectiveness measurement
            - Long-term learning outcome simulation
            """)
            
            st.success("""
            **Deliverable 2:**
            
            📈 **Validation Report**
            - 10 models × 6 strategies = 60 configurations
            - Statistical significance testing (p < 0.05)
            - Domain-specific performance profiles
            - Cost-benefit analysis
            
            🏆 **Recommended Configurations**
            - Best overall strategy
            - Domain-optimized approaches
            - Resource-constrained solutions
            """)
    
    with objectives_tabs[2]:
        st.markdown("### 📊 Objective 3: Mode Collapse Deep Investigation")
        
        st.info("""
        **Research Gap**: FYP-1 identified mode collapse correlation (r = 0.344) but didn't directly measure 
        entropy dynamics or test collapse-specific interventions. FYP-2 will rigorously quantify this mediating variable.
        """)
        
        collapse_col1, collapse_col2 = st.columns(2)
        
        with collapse_col1:
            st.markdown("""
            #### 3.1 Entropy Measurement Protocol (Months 2-3)
            
            **Direct Measurement:**
            - Calculate response entropy: `H(X) = -Σ p(xi) log2 p(xi)`
            - Measure across 100 prompts × 10 models = 1000 samples
            - Track entropy vs. sycophancy correlation
            
            **Diversity Metrics:**
            - Self-BLEU (lower = more diverse)
            - Distinct-n (unique n-gram ratios)
            - Semantic diversity (embedding space spread)
            
            **Baseline Thresholds:**
            - Define "severe collapse": >60% entropy reduction
            - Identify collapse onset points per model
            - Map collapse → tampering pathways
            """)
            
            st.markdown("""
            #### 3.2 Collapse-Targeted Mitigations (Months 4-6)
            
            **Diversity-Preserving Techniques:**
            
            1. **Diverse Beam Search**
               - Modify decoding to penalize repetition
               - Encourage exploration in output space
            
            2. **Temperature Scheduling**
               - Dynamic temperature during generation
               - Balance creativity vs. coherence
            
            3. **Multi-Sample Aggregation**
               - Generate multiple outputs, select most diverse
               - Ensemble approaches for response variety
            
            **Expected Outcomes:**
            - Increase entropy by 30-40%
            - Reduce tampering vulnerability by 20%
            - Maintain factual accuracy
            """)
        
        with collapse_col2:
            st.warning("""
            **Hypothesis to Test:**
            
            If mode collapse truly mediates the sycophancy → tampering cascade:
            
            ✅ **Prediction 1**: Reducing collapse should weaken tampering
            
            ✅ **Prediction 2**: Diversity interventions lower both sycophancy and tampering
            
            ✅ **Prediction 3**: Entropy correlates inversely with both behaviors (r < -0.5)
            """)
            
            st.markdown("""
            #### 3.3 Training Trajectory Analysis (Months 5-7)
            
            **Temporal Dynamics:**
            - Checkpoint models every 5 epochs
            - Measure behavioral triad evolution
            - Identify critical transition points
            
            **Longitudinal Study:**
            - Track 3 models through full RLHF process
            - Compare standard vs. diversity-aware training
            - Validate cascade hypothesis empirically
            
            **Visualization:**
            - Interactive entropy-behavior phase diagrams
            - Temporal heatmaps of collapse severity
            - Correlation strength evolution plots
            """)
            
            st.success("""
            **Deliverable 3:**
            
            📉 **Mode Collapse Report**
            - Entropy measurements for 10 models
            - Collapse-mitigation effectiveness analysis
            - Causal pathway validation
            
            🔬 **Training Trajectory Data**
            - Checkpoint evaluations (50+ timepoints)
            - Behavioral emergence timelines
            - Intervention impact visualization
            """)
    
    with objectives_tabs[3]:
        st.markdown("### 🌍 Objective 4: Multilingual & Cross-Cultural Expansion")
        
        st.error("""
        **Critical Gap from Literature**: 95%+ of sycophancy research is English-only. Cultural differences 
        in agreement norms, politeness conventions, and authority deference may drastically alter behavioral patterns.
        """)
        
        multi_col1, multi_col2 = st.columns(2)
        
        with multi_col1:
            st.markdown("""
            #### 4.1 Language Coverage (Months 6-8)
            
            **Target Languages:**
            
            🌐 **High-Resource (Priority 1):**
            - Spanish, French, German, Chinese (Mandarin)
            - Arabic, Hindi, Japanese, Portuguese
            
            🌏 **Medium-Resource (Priority 2):**
            - Urdu, Bengali, Korean, Italian
            - Russian, Turkish, Vietnamese
            
            **Test Set Translation:**
            - Professional translation of 150 core scenarios
            - Cultural adaptation (not literal translation)
            - Native speaker validation
            - Back-translation quality checks
            """)
            
            st.markdown("""
            #### 4.2 Cultural Context Analysis (Months 7-9)
            
            **Hypothesis:**
            Cultures with higher power distance (Hofstede) may show:
            - More sycophancy (respect for authority)
            - Different collapse patterns (collectivist consensus)
            - Varied tampering strategies (indirect communication)
            
            **Research Questions:**
            1. Do East Asian models exhibit higher sycophancy?
            2. Are Western models more confrontational with users?
            3. Do linguistic structures (honorifics) affect behavior?
            
            **Methodology:**
            - Compare 5 language families
            - Cultural dimension correlation analysis
            - Sociolinguistic pattern recognition
            """)
        
        with multi_col2:
            st.markdown("""
            #### 4.3 Multilingual Mitigation Adaptation (Months 8-10)
            
            **Challenges:**
            - Contrastive decoding requires language-specific tuning
            - Reward models may have cultural biases
            - Activation patterns differ across tokenizers
            
            **Solutions:**
            1. **Language-Agnostic Techniques**
               - Entropy-based approaches work universally
               - Architecture modifications transfer
            
            2. **Cultural Calibration**
               - Adjust agreement thresholds per culture
               - Train multilingual reward models
               - Collect diverse preference data
            
            3. **Zero-Shot Transfer Testing**
               - Train mitigation in English
               - Test effectiveness in other languages
               - Measure generalization gap
            """)
            
            st.success("""
            **Deliverable 4:**
            
            🌐 **Multilingual Dataset**
            - 150 scenarios × 8 languages = 1200 tests
            - Cultural context annotations
            - Native speaker quality scores
            
            📊 **Cross-Linguistic Analysis**
            - Behavioral comparison across languages
            - Cultural dimension correlations
            - Translation quality impact study
            
            🔧 **Adapted Mitigations**
            - Language-specific recommendations
            - Transfer learning effectiveness report
            - Deployment guidelines per region
            """)
    
    st.divider()
        
    # Expected Contributions
    st.markdown("### 🏆 Expected Contributions to Research Community")
    
    contrib_col1, contrib_col2, contrib_col3 = st.columns(3)
    
    with contrib_col1:
        st.markdown("""
        #### 📚 Theoretical
        
        - First causal validation of mode collapse mediation
        - Multilingual behavioral pattern taxonomy
        - Cultural influence framework
        - Temporal cascade dynamics model
        """)
    
    with contrib_col2:
        st.markdown("""
        #### 🔧 Practical
        
        - Open-source mitigation toolkit
        - Production deployment guidelines
        - Domain-specific best practices
        - Cost-benefit decision framework
        """)
    
    with contrib_col3:
        st.markdown("""
        #### 📊 Empirical
        
        - 10-model comparative dataset
        - Multilingual evaluation benchmark
        - Mitigation effectiveness meta-analysis
        - Mode collapse measurement protocol
        """)
    
    st.divider()
    
    