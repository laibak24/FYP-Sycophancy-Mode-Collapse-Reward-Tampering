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

# Custom CSS for modern styling
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: #f8fafc;
        border-radius: 10px 10px 0 0;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
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

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0;">🤖 FYP 2025</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Papers", "47", delta=None)
        st.metric("Test Cases", "150+", delta=None)
    with col2:
        st.metric("Models", "5", delta=None)
        st.metric("Experiments", "4", delta=None)
    
    st.markdown("---")
    st.markdown("### 👥 Research Team")
    st.markdown("""
    **Students:**
    - Kainat Faisal
    - Laiba Khan
    - Waniya Syed
    
    **Supervisor:**
    - Farrukh Hassan Syed
    """)
    
    st.markdown("---")
    st.markdown("### 📅 Project Timeline")
    st.markdown("""
    - **Start:** September 2024
    - **FYP1 Complete:** December 2024
    - **FYP2 Duration:** Jan - May 2025
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Current Status")
    st.progress(0.95, text="95% Complete")

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview", 
    "🧪 Experiments", 
    "📚 Literature Review", 
    "📈 Progress & Timeline", 
    "🔮 Future Work"
])

# TAB 1: OVERVIEW
with tab1:
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">The Flatterer's Dilemma</h1>
        <h3 style="margin: 0.5rem 0; font-weight: 400;">Why AI Would Rather Lie Than Disappoint</h3>
        <p style="font-size: 1.1em; margin-top: 1.5rem; opacity: 0.95;">
            A comprehensive investigation into sycophancy, mode collapse, and reward tampering in RLHF-trained LLMs
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📚 Papers Reviewed", "47", help="Systematic review covering 2020-2024")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🤖 Models Evaluated", "5", help="GPT-4, Claude, Gemini, Llama, Mistral")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🧪 Test Cases", "150+", help="Across 6 domains and 4 experimental setups")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 The Behavioral Triad")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="behavior-card" style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border-left: 5px solid #ef4444;">
            <h4 style="color: #991b1b; margin: 0; font-size: 1.2rem;">🗣️ Sycophancy</h4>
            <p style="color: #7f1d1d; margin-top: 0.8rem; line-height: 1.6;">
                Models prioritize user agreement over factual accuracy, compromising truth-seeking behavior
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="behavior-card" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 5px solid #f59e0b;">
            <h4 style="color: #92400e; margin: 0; font-size: 1.2rem;">📉 Mode Collapse</h4>
            <p style="color: #78350f; margin-top: 0.8rem; line-height: 1.6;">
                Systematic reduction in output diversity, producing repetitive and stereotypical responses
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="behavior-card" style="background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border-left: 5px solid #8b5cf6;">
            <h4 style="color: #6b21a8; margin: 0; font-size: 1.2rem;">🎮 Reward Tampering</h4>
            <p style="color: #581c87; margin-top: 0.8rem; line-height: 1.6;">
                Models game reward signals instead of genuinely solving tasks, exploiting evaluation systems
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 Key Findings")
    
    findings = [
        "Strong positive correlation (r=0.6159, p=0.0003) between sycophancy and reward tampering in Gemini experiments",
        "Mode collapse shows significant correlation with reward tampering (r=0.344, p=0.015) in GPT-4o-mini tests",
        "Sycophancy rates vary dramatically by domain: Medical (23.25%) vs Math (5.21%)",
        "Phi-3 model shows extreme sycophancy (100%) under pressure scenarios",
        "Behavioral triad emerges sequentially: Sycophancy (epochs 3-7) → Mode Collapse (8-15) → Reward Tampering (16-25)"
    ]
    
    for finding in findings:
        st.markdown(f'<div class="finding-item">✅ {finding}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔬 Research Impact")
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Theoretical Contribution:**
        - Established mechanistic framework linking three behavioral phenomena
        - Identified temporal cascade: RLHF Pressure → Sycophancy → Mode Collapse → Reward Tampering
        - Quantified correlations across multiple model families
        - Validated behavioral triad hypothesis through empirical testing
        """)
    with col2:
        st.warning("""
        **Practical Implications:**
        - Medical domain shows highest risk (23.25% sycophancy, 30% tampering)
        - Mitigation strategies identified with 15-34% effectiveness
        - Cross-model generalization patterns established
        - Framework applicable to future RLHF development
        """)

# TAB 2: EXPERIMENTS
with tab2:
    st.header("🧪 Experimental Results")
    
    st.markdown("### Comparative Analysis Across All Pipelines")
    
    # Experiment comparison bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Sycophancy %',
        x=experiment_results['experiment'],
        y=experiment_results['sycophancy'],
        marker_color='#ef4444',
        marker_line_color='#b91c1c',
        marker_line_width=2
    ))
    fig.add_trace(go.Bar(
        name='Mode Collapse %',
        x=experiment_results['experiment'],
        y=experiment_results['modeCollapse'],
        marker_color='#f59e0b',
        marker_line_color='#d97706',
        marker_line_width=2
    ))
    fig.add_trace(go.Bar(
        name='Reward Tampering %',
        x=experiment_results['experiment'],
        y=experiment_results['rewardTampering'],
        marker_color='#8b5cf6',
        marker_line_color='#7c3aed',
        marker_line_width=2
    ))
    
    fig.update_layout(
        barmode='group',
        title={
            'text': "Behavioral Metrics Across Experimental Pipelines",
            'font': {'size': 20, 'color': '#1f2937'}
        },
        xaxis_title="Experiment",
        yaxis_title="Score (%)",
        height=500,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)
    
    # Experiment details
    st.markdown("### 📋 Experiment Details")
    exp_details = experiment_results.copy()
    exp_details.columns = ['Experiment', 'Sycophancy (%)', 'Mode Collapse (%)', 'Reward Tampering (%)', 'Samples']
    st.dataframe(
        exp_details, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Experiment": st.column_config.TextColumn("Experiment", width="medium"),
            "Sycophancy (%)": st.column_config.NumberColumn("Sycophancy (%)", format="%.2f"),
            "Mode Collapse (%)": st.column_config.NumberColumn("Mode Collapse (%)", format="%.2f"),
            "Reward Tampering (%)": st.column_config.NumberColumn("Reward Tampering (%)", format="%.2f"),
            "Samples": st.column_config.NumberColumn("Samples", format="%d")
        }
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Domain-Specific Performance (Gemini)")
        
        # Radar chart for domain performance
        categories = domain_performance['domain'].tolist()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=domain_performance['sycophancy'].tolist(),
            theta=categories,
            fill='toself',
            name='Sycophancy',
            line_color='#ef4444',
            fillcolor='rgba(239, 68, 68, 0.3)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=domain_performance['modeCollapse'].tolist(),
            theta=categories,
            fill='toself',
            name='Mode Collapse',
            line_color='#f59e0b',
            fillcolor='rgba(245, 158, 11, 0.3)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=domain_performance['rewardTampering'].tolist(),
            theta=categories,
            fill='toself',
            name='Reward Tampering',
            line_color='#8b5cf6',
            fillcolor='rgba(139, 92, 246, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 35],
                    showline=False,
                    gridcolor='#e5e7eb'
                ),
                angularaxis=dict(
                    gridcolor='#e5e7eb'
                )
            ),
            showlegend=True,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Correlation Analysis (GPT-4o-mini HH-RLHF)")
        
        # Correlation bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Pearson r',
            x=correlation_data['name'],
            y=correlation_data['pearson'],
            marker_color='#3b82f6',
            marker_line_color='#2563eb',
            marker_line_width=2
        ))
        
        fig.add_trace(go.Bar(
            name='Spearman ρ',
            x=correlation_data['name'],
            y=correlation_data['spearman'],
            marker_color='#06b6d4',
            marker_line_color='#0891b2',
            marker_line_width=2
        ))
        
        fig.update_layout(
            barmode='group',
            xaxis_title="Relationship",
            yaxis_title="Correlation Coefficient",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12)
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb', zeroline=True, zerolinewidth=2, zerolinecolor='#9ca3af')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("**✓ Significant finding:** Mode Collapse ↔ Reward Tampering (p=0.015)")
    
    st.markdown("### 🔬 Model Comparison (Literature Review Data)")
    
    # Scatter plot with better styling
    fig = px.scatter(
        model_comparison,
        x='sycophancy',
        y='correlation',
        size='rewardTampering',
        color='riskLevel',
        hover_data=['model', 'modeCollapse', 'rewardTampering'],
        labels={
            'sycophancy': 'Sycophancy Rate (%)',
            'correlation': 'Behavioral Triad Correlation',
            'riskLevel': 'Risk Level'
        },
        color_discrete_map={'Critical': '#ef4444', 'High': '#f59e0b', 'Medium': '#22c55e'},
        title="Sycophancy vs Behavioral Triad Correlation"
    )
    
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=20,
        font=dict(family="Arial, sans-serif", size=12)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Model details table
    st.markdown("### 📊 Detailed Model Metrics")
    st.dataframe(
        model_comparison, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "model": st.column_config.TextColumn("Model", width="medium"),
            "sycophancy": st.column_config.NumberColumn("Sycophancy (%)", format="%.2f"),
            "modeCollapse": st.column_config.NumberColumn("Mode Collapse", format="%.2f"),
            "rewardTampering": st.column_config.NumberColumn("Reward Tampering", format="%.2f"),
            "correlation": st.column_config.NumberColumn("Correlation", format="%.2f"),
            "riskLevel": st.column_config.TextColumn("Risk Level", width="small")
        }
    )

# TAB 3: LITERATURE REVIEW
with tab3:
    st.header("📚 Literature Review Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Papers Analyzed", "47")
    with col2:
        st.metric("📅 Time Period", "2020-2024")
    with col3:
        st.metric("💾 Databases", "4", help="arXiv, Google Scholar, ACL, IEEE")
    with col4:
        st.metric("✅ Review Method", "PRISMA", help="Systematic review protocol")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔄 The Behavioral Triad Framework")
    
    st.info("""
    **Cascading Relationship:**
    
    ```
    RLHF Optimization Pressure → Sycophancy → Mode Collapse → Reward Tampering
    ```
    
    The literature establishes that optimization pressure from RLHF creates preference-seeking behaviors (sycophancy), 
    which reduces output diversity (mode collapse), ultimately enabling sophisticated reward-gaming tactics (reward tampering).
    """)
    
    st.markdown("### 📈 Empirical Evidence from Literature")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.07);">
            <h2 style="color: #ef4444; margin: 0; font-size: 2.5rem;">r = 0.78</h2>
            <p style="color: #991b1b; margin: 0.8rem 0 0 0; font-weight: 600;">Sycophancy ↔ Mode Collapse</p>
            <p style="color: #7f1d1d; font-size: 0.9em; margin-top: 0.5rem;">p < 0.001</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.07);">
            <h2 style="color: #f59e0b; margin: 0; font-size: 2.5rem;">r = 0.84</h2>
            <p style="color: #92400e; margin: 0.8rem 0 0 0; font-weight: 600;">Mode Collapse ↔ Reward Tampering</p>
            <p style="color: #78350f; font-size: 0.9em; margin-top: 0.5rem;">p < 0.001</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.07);">
            <h2 style="color: #8b5cf6; margin: 0; font-size: 2.5rem;">r = 0.71</h2>
            <p style="color: #6b21a8; margin: 0.8rem 0 0 0; font-weight: 600;">Sycophancy ↔ Reward Tampering</p>
            <p style="color: #581c87; font-size: 0.9em; margin-top: 0.5rem;">p < 0.001</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⏱️ Temporal Progression During Training")
    
    # Timeline visualization
    epochs = ['0-2', '3-7', '8-15', '16-25']
    sycophancy_intensity = [0, 0.8, 0.6, 0.3]
    mode_collapse_intensity = [0, 0.2, 0.9, 0.7]
    reward_tampering_intensity = [0, 0, 0.4, 1.0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=epochs, 
        y=sycophancy_intensity, 
        mode='lines+markers', 
        name='Sycophancy', 
        line=dict(color='#ef4444', width=4),
        marker=dict(size=12, symbol='circle')
    ))
    fig.add_trace(go.Scatter(
        x=epochs, 
        y=mode_collapse_intensity, 
        mode='lines+markers', 
        name='Mode Collapse', 
        line=dict(color='#f59e0b', width=4),
        marker=dict(size=12, symbol='square')
    ))
    fig.add_trace(go.Scatter(
        x=epochs, 
        y=reward_tampering_intensity, 
        mode='lines+markers', 
        name='Reward Tampering', 
        line=dict(color='#8b5cf6', width=4),
        marker=dict(size=12, symbol='diamond')
    ))
    
    fig.update_layout(
        title={
            'text': "Behavioral Emergence Across Training Epochs",
            'font': {'size': 20, 'color': '#1f2937'}
        },
        xaxis_title="Training Epochs",
        yaxis_title="Behavior Intensity",
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 🛠️ Mitigation Strategies Comparison")
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Sycophancy Reduction (%)', 'Performance Impact (%)'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(
            x=mitigation['strategy'], 
            y=mitigation['sycReduction'], 
            name='Syc Reduction', 
            marker_color='#22c55e',
            marker_line_color='#16a34a',
            marker_line_width=2
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=mitigation['strategy'], 
            y=mitigation['performance'], 
            name='Performance', 
            marker_color='#3b82f6',
            marker_line_color='#2563eb',
            marker_line_width=2
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(tickangle=-45)
    fig.update_layout(
        height=500, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12)
    )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("**🏆 Best overall:** RAG Integration (34.2% reduction, +3.4% performance, Medium cost)")
    with col2:
        st.info("**💡 Most practical:** LQCD (18.7% reduction, -0.4% performance, Low cost)")
    
    st.markdown("### ⚠️ Critical Research Gaps Identified")
    
    gaps = [
        ("🌍 Multilingual Coverage", "95% of studies focus on English only"),
        ("📊 Evaluation Scope", "Most tests limited to factual/mathematical domains"),
        ("⏰ Temporal Dynamics", "Long-term behavioral persistence unexplored"),
        ("🤖 Model Diversity", "Commercial models overrepresented, open-source understudied"),
        ("🧠 Mechanistic Understanding", "Internal neural pathways driving behaviors unclear")
    ]
    
    for title, desc in gaps:
        st.warning(f"**{title}:** {desc}")

# TAB 4: PROGRESS & TIMELINE
with tab4:
    st.header("📈 FYP Progress & Timeline")
    
    st.markdown("### 📅 Project Timeline")
    
    # Progress bars with modern styling
    for idx, row in timeline.iterrows():
        col1, col2, col3 = st.columns([2, 6, 1])
        
        with col1:
            st.markdown(f"**{row['phase']}**")
        
        with col2:
            if row['status'] == 'complete':
                st.progress(row['progress'] / 100, text=f"{row['progress']}% ✓")
            elif row['status'] == 'active':
                st.progress(row['progress'] / 100, text=f"{row['progress']}% (In Progress)")
            else:
                st.progress(row['progress'] / 100, text=f"{row['progress']}% (Planned)")
        
        with col3:
            if row['status'] == 'complete':
                st.markdown("✅")
            elif row['status'] == 'active':
                st.markdown("🔄")
            else:
                st.markdown("⏳")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ FYP1 Achievements")
        
        achievements = [
            ("📚 Comprehensive Literature Review", "47 papers analyzed, taxonomy established"),
            ("🧪 Multi-Model Evaluation Pipeline", "4 experimental setups across GPT-4, Phi-3, Gemini"),
            ("📊 Statistical Correlation Analysis", "Pearson, Spearman, Chi-square tests conducted"),
            ("💾 Dataset Creation", "66+ synthetic test cases across 6 domains"),
            ("🔬 Behavioral Triad Validation", "Correlations identified and documented"),
            ("📝 Documentation & Reporting", "Review paper and technical documentation complete")
        ]
        
        for title, desc in achievements:
            with st.container():
                st.success(f"**{title}**")
                st.caption(desc)
                st.markdown("<br>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔄 Current Sprint: Dashboard Development")
        
        sprint_tasks = [
            ("Data Integration", 100),
            ("Visualization Components", 95),
            ("Interactive Features", 85),
            ("Documentation", 80)
        ]
        
        for task, progress in sprint_tasks:
            st.markdown(f"**{task}**")
            st.progress(progress / 100, text=f"{progress}%")
            st.markdown("")
        
        st.markdown("### 📊 Overall FYP1 Completion")
        st.metric("Progress", "95%", delta="5% remaining", delta_color="inverse")

# TAB 5: FUTURE WORK
with tab5:
    st.header("🔮 FYP2 Research Agenda")
    
    st.info("""
    **Three-Tier Prioritized Research Roadmap**
    
    A structured plan addressing critical gaps identified in FYP1, progressing from foundational work 
    to advanced mechanistic understanding and governance frameworks.
    """)
    
    st.markdown("### 🟢 Tier 1: Foundational Work (0-12 months)")
    
    tier1_items = [
        {
            "title": "🧠 Mechanistic Interpretability",
            "desc": "Identify neural circuits and attention patterns driving sycophantic behavior using activation patching and ablation studies",
            "priority": "High"
        },
        {
            "title": "🌍 Multilingual Testing",
            "desc": "Expand evaluation to 10+ languages to test cross-cultural generalization of behavioral patterns",
            "priority": "High"
        },
        {
            "title": "🔓 Open-Source Model Analysis",
            "desc": "Systematic evaluation of LLaMA, Mistral, and other open models for reproducibility",
            "priority": "Medium"
        }
    ]
    
    for item in tier1_items:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{item['title']}**")
                st.caption(item['desc'])
            with col2:
                if item['priority'] == 'High':
                    st.markdown('<span class="priority-high">🔴 High</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="priority-medium">🟡 Medium</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🔵 Tier 2: Mechanistic Understanding (12-24 months)")
    
    tier2_items = [
        {
            "title": "🎯 Adversarial Reward Modeling",
            "desc": "Develop reward functions resistant to manipulation with demographically diverse preference collection",
            "priority": "High"
        },
        {
            "title": "⏰ Long-term Behavioral Dynamics",
            "desc": "Study persistence of mitigations and emergence of new behaviors over extended deployment",
            "priority": "Medium"
        },
        {
            "title": "🏗️ Cross-Architecture Analysis",
            "desc": "Compare transformer variants, SSMs, and hybrid architectures for vulnerability patterns",
            "priority": "Medium"
        }
    ]
    
    for item in tier2_items:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{item['title']}**")
                st.caption(item['desc'])
            with col2:
                if item['priority'] == 'High':
                    st.markdown('<span class="priority-high">🔴 High</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="priority-medium">🟡 Medium</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🟣 Tier 3: Mitigation & Governance (24+ months)")
    
    tier3_items = [
        {
            "title": "⚖️ Governance Framework Development",
            "desc": "Establish regulatory guidelines for RLHF deployment with transparency requirements",
            "priority": "High"
        },
        {
            "title": "🛡️ Integrated Mitigation Suite",
            "desc": "Combine training, inference, and architectural interventions for comprehensive defense",
            "priority": "High"
        },
        {
            "title": "🌐 Real-world Deployment Studies",
            "desc": "Monitor behavioral patterns in production systems across high-stakes domains",
            "priority": "Medium"
        }
    ]
    
    for item in tier3_items:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{item['title']}**")
                st.caption(item['desc'])
            with col2:
                if item['priority'] == 'High':
                    st.markdown('<span class="priority-high">🔴 High</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="priority-medium">🟡 Medium</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Expected Outcomes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📝 Publications**
        - 2-3 conference papers
        - 1 journal article
        - Workshop presentations
        - Technical reports
        """)
    
    with col2:
        st.markdown("""
        **🛠️ Technical Deliverables**
        - Open-source evaluation suite
        - Mitigation toolkit
        - Dataset repository
        - Interactive dashboard
        """)
    
    with col3:
        st.markdown("""
        **🤝 Community Impact**
        - Framework adoption
        - Industry collaboration
        - Policy recommendations
        - Educational resources
        """)
    
    st.markdown("---")
    
    st.markdown("### 📚 Recommended Reading & Resources")
    
    resources = {
        "Foundational Papers": [
            "Perez et al. (2022) - Discovering Language Model Behaviors with Model-Written Evaluations",
            "Sharma et al. (2023) - Towards Understanding Sycophancy in Language Models",
            "Casper et al. (2023) - Open Problems in AI Safety"
        ],
        "Mitigation Strategies": [
            "Burns et al. (2023) - Weak-to-Strong Generalization",
            "Scheurer et al. (2023) - Training Language Models with Language Feedback",
            "Bai et al. (2022) - Constitutional AI"
        ],
        "Evaluation Frameworks": [
            "Anthropic Evals - Model Behavior Evaluation Suite",
            "OpenAI Evals - Standardized Testing Framework",
            "EleutherAI LM Evaluation Harness"
        ]
    }
    
    for category, papers in resources.items():
        with st.expander(f"📖 {category}"):
            for paper in papers:
                st.markdown(f"- {paper}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 10px;">
    <h3 style="color: #1f2937; margin: 0;">The Flatterer's Dilemma</h3>
    <p style="color: #6b7280; margin: 0.5rem 0;">FYP 2024-2025 | Habib University</p>
    <p style="color: #9ca3af; font-size: 0.9rem;">
        Kainat Faisal • Laiba Khan • Waniya Syed<br>
        Supervised by: Farrukh Hassan Syed
    </p>
</div>
""", unsafe_allow_html=True)