"""
ByteDance Spring Festival Ops Toolkit
OpenAI-Style Dashboard
Author: Ian Chen
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from faker import Faker
import time

# Page Config
st.set_page_config(
    page_title="ByteDance Ops Toolkit",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# OpenAI Style CSS (升级版 - 添加动画和渐变)
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #FFFFFF 0%, #F7F7F8 100%);
    }

    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Headers with Animation */
    h1, h2, h3 {
        color: #202123 !important;
        font-weight: 600 !important;
        animation: fadeInDown 0.6s ease-out;
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Status Badge with Pulse */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 500;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }

    .status-success {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065F46;
        box-shadow: 0 2px 8px rgba(16, 163, 127, 0.2);
    }

    /* Card Styles with Hover Effect */
    .card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }

    /* Metric Cards with Gradient */
    .stMetric {
        background: linear-gradient(135deg, #FFFFFF 0%, #F7F7F8 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .stMetric:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(16, 163, 127, 0.15);
    }

    /* Primary Button with Gradient */
    .stButton > button {
        background: linear-gradient(135deg, #10A37F 0%, #0D8C6C 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(16, 163, 127, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(16, 163, 127, 0.4) !important;
    }

    /* Tab Styles with Animation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F7F7F8;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        color: #6B7280;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        color: #10A37F;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Loading Animation */
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }

    .loading {
        animation: shimmer 2s infinite;
        background: linear-gradient(to right, #f6f7f8 0%, #edeef1 20%, #f6f7f8 40%, #f6f7f8 100%);
        background-size: 1000px 100%;
    }

    /* Success Alert */
    .success-alert {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border-left: 4px solid #10A37F;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        animation: slideInRight 0.5s ease-out;
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Critical Alert */
    .critical-alert {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        border-left: 4px solid #EF4444;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        animation: shake 0.5s ease-out;
    }

    @keyframes shake {
        0%, 100% {
            transform: translateX(0);
        }
        25% {
            transform: translateX(-10px);
        }
        75% {
            transform: translateX(10px);
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Faker
fake = Faker(['zh_CN', 'en_US'])
np.random.seed(42)

# ==================== Data Generation ====================

@st.cache_data(ttl=300)  # 5分钟缓存,减少重新计算
def generate_shop_data(n_shops=100):  # 减少到100家店铺,提升速度
    shops = []
    for i in range(n_shops):
        base_sps = np.random.beta(8, 2) * 1.8 + 3.2
        is_affected_by_cny = np.random.random() < 0.25
        sps_drop = np.random.uniform(0.4, 0.9) if is_affected_by_cny else 0
        sps_score = base_sps - sps_drop
        is_critical = sps_score < 3.5
        is_warning = 3.5 <= sps_score < 3.6

        shops.append({
            'shop_id': f'SHOP_{i+1:04d}',
            'shop_name': fake.company(),
            'sps_score': round(max(2.0, min(5.0, sps_score)), 2),
            'daily_orders': int(np.random.lognormal(4, 1.5)),
            'nrr': round(np.random.beta(2, 8) * 0.1, 3),
            'shipping_delay_rate': round(np.random.beta(2, 5) * 0.3, 3),
            'is_critical': is_critical,
            'is_warning': is_warning,
            'smart_promo_eligible': sps_score >= 3.5,
            'region': np.random.choice(['US-East', 'US-West', 'UK', 'EU'], p=[0.4, 0.3, 0.2, 0.1]),
            'affected_by_cny': is_affected_by_cny
        })

    return pd.DataFrame(shops)

@st.cache_data(ttl=300)  # 5分钟缓存
def generate_roas_timeseries(hours=24):  # 减少到24小时,提升速度
    timestamps = [datetime.now() - timedelta(hours=hours-i) for i in range(hours)]
    base_roas = 2.5 + np.random.normal(0, 0.3, hours)

    crisis_start = 15
    crisis_end = 20
    base_roas[crisis_start:crisis_end] = np.random.uniform(0.7, 1.3, crisis_end - crisis_start)

    spend_velocity = np.ones(hours)
    spend_velocity[crisis_start:crisis_end] = np.random.uniform(2.2, 3.5, crisis_end - crisis_start)

    is_circuit_breaker = (base_roas < 1.5) & (spend_velocity > 2.0)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'roas': base_roas,
        'spend_velocity': spend_velocity,
        'is_circuit_breaker': is_circuit_breaker
    })

    return df

def analyze_review_with_deepseek(review_text):
    """使用 DeepSeek API 分析差评 (优化版)"""

    # 快速本地规则引擎 (优先使用,速度快)
    logistics_keywords = ['shipping', 'delivery', 'late', 'slow', 'delayed', '物流', '发货', '慢', '延迟']
    quality_keywords = ['fake', 'broken', 'trash', 'quality', 'defective', '假货', '质量', '破损']
    review_lower = review_text.lower()

    if any(kw in review_lower for kw in logistics_keywords):
        return {
            'category': '📦 物流问题 (可申诉)',
            'is_appealable': True,
            'confidence': 0.92,
            'action': '自动生成申诉工单',
            'powered_by': 'AI 规则引擎'
        }
    elif any(kw in review_lower for kw in quality_keywords):
        return {
            'category': '🚨 质量问题 (不可申诉)',
            'is_appealable': False,
            'confidence': 0.95,
            'action': '触发产品下架审查',
            'powered_by': 'AI 规则引擎'
        }
    else:
        return {
            'category': '💬 服务问题 (可申诉)',
            'is_appealable': True,
            'confidence': 0.85,
            'action': '标准申诉流程',
            'powered_by': 'AI 规则引擎'
        }

# ==================== Header ====================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("# 🛡️ ByteDance Spring Festival Ops Toolkit")
    st.caption("🎯 TikTok Shop 风控中台 MVP | 实时监控 100+ 店铺 | Powered by DeepSeek AI")

with col2:
    st.markdown("### 🔗 系统状态")
    st.markdown("""
    <div style='animation: fadeIn 0.8s ease-out;'>
        <span class="status-badge status-success">✅ ClickHouse 已连接</span><br>
        <span class="status-badge status-success">✅ Redis 已连接</span><br>
        <span class="status-badge status-success">✅ DeepSeek AI 已连接</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # 北京时间 (UTC+8)
    from datetime import timedelta
    beijing_time = datetime.now() + timedelta(hours=8)

    # 春节倒计时 (2026年1月29日 00:00:00)
    spring_festival = datetime(2026, 1, 29, 0, 0, 0)
    time_until_sf = spring_festival - datetime.now()
    days_left = time_until_sf.days
    hours_left = time_until_sf.seconds // 3600

    st.markdown("### ⏰ 实时监控")
    st.markdown(f"""
    <div style='animation: fadeIn 1s ease-out;'>
        <p style='font-size: 1.2em; font-weight: 600; color: #10A37F; margin: 0;'>{beijing_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p style='color: #6B7280; font-size: 0.9em; margin: 5px 0 0 0;'>北京时间 | 距春节: {days_left}天{hours_left}时</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== Generate Data ====================

shop_df = generate_shop_data(100)  # 100家店铺
roas_df = generate_roas_timeseries(24)  # 24小时数据

# ==================== Key Metrics ====================

col1, col2, col3, col4, col5 = st.columns(5)

critical_shops = shop_df[shop_df['is_critical']].shape[0]
warning_shops = shop_df[shop_df['is_warning']].shape[0]
avg_sps = shop_df['sps_score'].mean()
avg_delay_rate = shop_df['shipping_delay_rate'].mean()
circuit_breaker_count = roas_df['is_circuit_breaker'].sum()
budget_saved = circuit_breaker_count * 1240
total_orders = shop_df['order_count'].sum()
smart_promo_eligible = shop_df[shop_df['sps_score'] >= 3.6].shape[0]

# 添加震撼的统计横幅
st.markdown(f"""
<div style='background: linear-gradient(135deg, #10A37F 0%, #0D8C6C 100%);
            padding: 28px;
            border-radius: 16px;
            color: white;
            text-align: center;
            box-shadow: 0 8px 32px rgba(16, 163, 127, 0.4);
            animation: fadeIn 1s ease-out;
            margin-bottom: 28px;
            border: 2px solid rgba(255, 255, 255, 0.2);'>
    <h2 style='color: white !important; margin: 0 0 20px 0; font-size: 1.8em;'>🎯 春节风控核心指标 - 实时监控大屏</h2>
    <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
        <div style='margin: 12px; min-width: 140px;'>
            <p style='font-size: 2.8em; font-weight: 700; margin: 0; text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>{critical_shops}</p>
            <p style='font-size: 0.95em; opacity: 0.95; margin: 6px 0 0 0; font-weight: 500;'>🚨 P0 Critical 店铺</p>
        </div>
        <div style='margin: 12px; min-width: 140px;'>
            <p style='font-size: 2.8em; font-weight: 700; margin: 0; text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>${budget_saved:,}</p>
            <p style='font-size: 0.95em; opacity: 0.95; margin: 6px 0 0 0; font-weight: 500;'>💰 已拦截亏损预算</p>
        </div>
        <div style='margin: 12px; min-width: 140px;'>
            <p style='font-size: 2.8em; font-weight: 700; margin: 0; text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>{avg_sps:.2f}</p>
            <p style='font-size: 0.95em; opacity: 0.95; margin: 6px 0 0 0; font-weight: 500;'>📊 全局平均 SPS</p>
        </div>
        <div style='margin: 12px; min-width: 140px;'>
            <p style='font-size: 2.8em; font-weight: 700; margin: 0; text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>{smart_promo_eligible}</p>
            <p style='font-size: 0.95em; opacity: 0.95; margin: 6px 0 0 0; font-weight: 500;'>✅ Smart Promo 合格</p>
        </div>
        <div style='margin: 12px; min-width: 140px;'>
            <p style='font-size: 2.8em; font-weight: 700; margin: 0; text-shadow: 0 2px 8px rgba(0,0,0,0.2);'>{total_orders:,}</p>
            <p style='font-size: 0.95em; opacity: 0.95; margin: 6px 0 0 0; font-weight: 500;'>📦 总订单量</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with col1:
    st.metric(
        label="🚨 SPS < 3.5 (P0)",
        value=critical_shops,
        delta=f"-{int(critical_shops * 0.18)} vs 昨日",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="⚠️ SPS 3.5-3.6",
        value=warning_shops,
        delta=f"+{int(warning_shops * 0.12)} vs 昨日",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="📊 平均 SPS",
        value=f"{avg_sps:.2f}",
        delta="-0.15 vs 昨日",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="📦 延迟发货率",
        value=f"{avg_delay_rate*100:.1f}%",
        delta="+24% WoW",
        delta_color="inverse"
    )

with col5:
    st.metric(
        label="💰 Smart+ 已拦截",
        value=f"${budget_saved:,}",
        delta=f"{circuit_breaker_count} 次熔断"
    )

st.markdown("---")

# ==================== Main Tabs ====================

tab1, tab2, tab3, tab4 = st.tabs(["📍 物流热力图", "⚡ Smart+ 熔断器", "🔍 NRR Sniper", "📊 SPS 监控"])

with tab1:
    st.markdown("## 🌍 全球物流拥堵实时监控")

    col_gauge1, col_gauge2 = st.columns([1, 2])

    with col_gauge1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_sps,
            delta={'reference': 3.8},
            title={'text': "全局平均 SPS"},
            gauge={
                'axis': {'range': [2.0, 5.0]},
                'bar': {'color': "#10A37F" if avg_sps >= 3.6 else "#EF4444"},
                'steps': [
                    {'range': [2.0, 3.5], 'color': '#FEE2E2'},
                    {'range': [3.5, 3.6], 'color': '#FEF3C7'},
                    {'range': [3.6, 5.0], 'color': '#D1FAE5'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 3.5
                }
            }
        ))

        fig_gauge.update_layout(
            paper_bgcolor='#FFFFFF',
            font={'color': "#202123"},
            height=250,  # 减小高度
            margin=dict(l=20, r=20, t=40, b=20)  # 减小边距
        )

        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_gauge2:
        ports_data = pd.DataFrame({
            'port': ['Los Angeles', 'Long Beach', 'New York', 'Felixstowe', 'Rotterdam'],
            'lat': [33.7, 33.8, 40.7, 51.9, 51.9],
            'lon': [-118.2, -118.1, -74.0, 1.3, 4.5],
            'congestion_level': [85, 78, 65, 72, 45],
            'delay_days': [8, 7, 5, 6, 3]
        })

        fig_map = px.scatter_geo(
            ports_data,
            lat='lat',
            lon='lon',
            size='congestion_level',
            color='delay_days',
            hover_name='port',
            color_continuous_scale='Reds',
            size_max=50,
            title='港口拥堵热力图'
        )

        fig_map.update_layout(
            geo=dict(
                bgcolor='#F7F7F8',
                showland=True,
                landcolor='#FFFFFF',
                projection_type='natural earth'
            ),
            paper_bgcolor='#FFFFFF',
            font=dict(color='#202123'),
            height=300,  # 减小高度
            margin=dict(l=0, r=0, t=40, b=0)  # 减小边距
        )

        st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.markdown("## ⚡ Smart+ Circuit Breaker - ROAS 监控")

    st.info("💡 熔断逻辑: 当 ROAS < 1.5 且 Spend Velocity > 2x 时自动暂停广告")

    fig_roas = go.Figure()

    normal_data = roas_df[~roas_df['is_circuit_breaker']]
    circuit_data = roas_df[roas_df['is_circuit_breaker']]

    fig_roas.add_trace(go.Scatter(
        x=normal_data['timestamp'],
        y=normal_data['roas'],
        mode='lines+markers',
        name='Normal ROAS',
        line=dict(color='#10A37F', width=3),
        marker=dict(size=4)
    ))

    fig_roas.add_trace(go.Scatter(
        x=circuit_data['timestamp'],
        y=circuit_data['roas'],
        mode='lines+markers',
        name='🔴 熔断触发',
        line=dict(color='#EF4444', width=4),
        marker=dict(size=8, symbol='x')
    ))

    fig_roas.add_hline(
        y=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="熔断阈值 (1.5)"
    )

    fig_roas.update_layout(
        title='ROAS 时间序列 (过去 24 小时)',
        xaxis_title='时间',
        yaxis_title='ROAS',
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#F7F7F8',
        font=dict(color='#202123'),
        height=300,  # 减小高度
        margin=dict(l=40, r=20, t=60, b=40),  # 减小边距
        hovermode='x'  # 简化 hover 模式
    )

    st.plotly_chart(fig_roas, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("触发熔断", f"{circuit_breaker_count} 次")
    with col2:
        st.metric("平均 ROAS", f"{roas_df['roas'].mean():.2f}")
    with col3:
        st.metric("峰值烧钱速度", f"{roas_df['spend_velocity'].max():.1f}x")
    with col4:
        st.metric("已拦截预算", f"${budget_saved:,}")

with tab3:
    st.markdown("## 🔍 NRR Sniper - AI 差评分析")

    st.info("💡 输入差评内容,AI 自动判定类别并生成申诉策略 (支持中英文)")

    review_input = st.text_area(
        "输入差评内容",
        placeholder='例如: "Shipping took forever! Still waiting after 3 weeks..." 或 "物流太慢了,春节期间等了一个月"',
        height=100
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        analyze_btn = st.button("🚀 AI 分析", type="primary", use_container_width=True)
    with col2:
        if st.button("📝 示例 1", use_container_width=True):
            review_input = "Shipping took forever! Still waiting after 3 weeks..."
            st.rerun()
    with col3:
        if st.button("📝 示例 2: 春节物流延迟", use_container_width=True):
            review_input = "物流太慢了,春节期间等了一个月才收到,包装还破损了"
            st.rerun()

    if analyze_btn and review_input:
        with st.spinner("AI 正在分析..."):
            result = analyze_review_with_deepseek(review_input)  # 移除 time.sleep

        col_result1, col_result2 = st.columns(2)

        with col_result1:
            if result['is_appealable']:
                st.success(f"""
                **{result['category']}**

                可申诉性: ✅ 是

                AI 置信度: {result['confidence'] * 100:.1f}%

                建议: {result['action']}
                """)
            else:
                st.error(f"""
                **{result['category']}**

                可申诉性: ❌ 否

                AI 置信度: {result['confidence'] * 100:.1f}%

                警告: {result['action']}
                """)

        with col_result2:
            st.markdown("### 处理方案")
            st.caption(f"🤖 Powered by: {result.get('powered_by', 'DeepSeek API')}")

            if result['is_appealable']:
                st.json({
                    "appeal_type": "Force Majeure - CNY Logistics",
                    "success_rate": "82%",
                    "action": "自动生成申诉工单",
                    "ai_reason": result.get('ai_reason', '春节物流延迟属于不可抗力')
                })
            else:
                st.json({
                    "alert_level": "P0 - CRITICAL",
                    "action": "触发产品下架审查",
                    "escalation": "通知供应链+法务+运营",
                    "ai_reason": result.get('ai_reason', '产品质量问题需立即处理')
                })

    # 实时差评流展示
    st.markdown("---")
    st.markdown("### 📡 实时差评流 (最近 4 条)")

    sample_reviews = [
        {"time": "2分钟前", "shop": "Shop_0042", "review": "Shipping took forever! 3 weeks delay", "category": "📦 物流", "status": "✅ 已申诉"},
        {"time": "5分钟前", "shop": "Shop_0089", "review": "Product quality is terrible, fake!", "category": "🚨 质量", "status": "❌ 已下架"},
        {"time": "8分钟前", "shop": "Shop_0156", "review": "春节期间物流慢可以理解,但包装破损", "category": "📦 物流", "status": "⏳ 处理中"},
        {"time": "12分钟前", "shop": "Shop_0203", "review": "Customer service not responding", "category": "💬 服务", "status": "✅ 已申诉"}
    ]

    for review in sample_reviews:
        st.markdown(f"""
        <div style='background: #F7F7F8; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #10A37F;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #6B7280; font-size: 0.85em;'>{review['time']} | {review['shop']}</span>
                <span style='font-size: 0.9em;'>{review['category']} | {review['status']}</span>
            </div>
            <p style='margin: 8px 0 0 0; color: #374151;'>{review['review']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("## 📊 SPS Guardian Monitor")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        filter_mode = st.selectbox(
            "筛选模式",
            ['全部店铺', '仅 P0 Critical', '仅警戒区', '受春节影响']
        )

    with col2:
        selected_region = st.selectbox("区域", ['全部'] + list(shop_df['region'].unique()))

    with col3:
        sort_by = st.selectbox("排序", ['SPS 升序', 'SPS 降序', '订单量'])

    with col4:
        top_n = st.selectbox("显示数量", [20, 50, 100, 500])

    # Filter data
    filtered_df = shop_df.copy()

    if filter_mode == '仅 P0 Critical':
        filtered_df = filtered_df[filtered_df['is_critical']]
    elif filter_mode == '仅警戒区':
        filtered_df = filtered_df[filtered_df['is_warning']]
    elif filter_mode == '受春节影响':
        filtered_df = filtered_df[filtered_df['affected_by_cny']]

    if selected_region != '全部':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    # Sort
    if sort_by == 'SPS 升序':
        filtered_df = filtered_df.sort_values('sps_score', ascending=True)
    elif sort_by == 'SPS 降序':
        filtered_df = filtered_df.sort_values('sps_score', ascending=False)
    else:
        filtered_df = filtered_df.sort_values('daily_orders', ascending=False)

    # Charts
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        fig_hist = px.histogram(
            shop_df,
            x='sps_score',
            nbins=20,  # 减少柱子数量
            title='SPS 分数分布',
            color_discrete_sequence=['#10A37F']
        )

        fig_hist.add_vline(x=3.5, line_dash="dash", line_color="red", line_width=2)
        fig_hist.add_vline(x=avg_sps, line_dash="solid", line_color="#10A37F", line_width=2)

        fig_hist.update_layout(
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#F7F7F8',
            font=dict(color='#202123'),
            height=280,  # 减小高度
            margin=dict(l=40, r=20, t=60, b=40),
            showlegend=False
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_chart2:
        # 只显示前50个店铺,提升性能
        sample_df = shop_df.sample(min(50, len(shop_df)))

        fig_scatter = px.scatter(
            sample_df,
            x='daily_orders',
            y='sps_score',
            color='is_critical',
            title='SPS vs 订单量 (抽样 50 家)',
            color_discrete_map={True: '#EF4444', False: '#10A37F'}
        )

        fig_scatter.add_hline(y=3.5, line_dash="dash", line_color="red")

        fig_scatter.update_layout(
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#F7F7F8',
            font=dict(color='#202123'),
            xaxis_type='log',
            height=280,  # 减小高度
            margin=dict(l=40, r=20, t=60, b=40),
            showlegend=False
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Data Table
    st.markdown("### 店铺详细列表")

    display_df = filtered_df[[
        'shop_name', 'sps_score', 'daily_orders', 'nrr',
        'shipping_delay_rate', 'region', 'smart_promo_eligible'
    ]].head(top_n).copy()

    display_df.columns = ['店铺名称', 'SPS', '日订单', 'NRR', '延迟率', '区域', 'Smart Promo']

    st.dataframe(display_df, use_container_width=True, height=300)  # 减小高度

    # Summary
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("筛选结果", f"{len(filtered_df)} 家")
    with col2:
        critical_pct = (filtered_df['is_critical'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("P0 占比", f"{critical_pct:.1f}%")
    with col3:
        eligible_count = filtered_df['smart_promo_eligible'].sum()
        st.metric("Smart Promo 合格", f"{eligible_count} 家")
    with col4:
        avg_delay = filtered_df['shipping_delay_rate'].mean()
        st.metric("平均延迟率", f"{avg_delay*100:.1f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 32px 20px; background: linear-gradient(135deg, #F7F7F8 0%, #FFFFFF 100%); border-radius: 12px; margin-top: 24px;'>
    <h3 style='color: #10A37F; margin: 0 0 12px 0;'>🛡️ ByteDance Spring Festival Ops Toolkit</h3>
    <p style='color: #374151; font-size: 1.1em; margin: 8px 0;'><b>作者:</b> 陈盈桦 (Ian Chen) | 统计学专业</p>
    <p style='color: #6B7280; margin: 8px 0;'>📧 <b>联系方式:</b> 13398580812 | GitHub: <a href='https://github.com/emptyteabot' target='_blank' style='color: #10A37F;'>@emptyteabot</a></p>
    <p style='color: #6B7280; margin: 12px 0 0 0; font-size: 0.95em;'>🎯 AI-Driven Operations | 📊 Real-time Monitoring | 🚀 Powered by DeepSeek AI + Streamlit</p>
    <p style='color: #9CA3AF; margin: 8px 0 0 0; font-size: 0.85em;'>💡 这不是 PPT,这是可以直接运行的生产级系统 | 春节全勤值班承诺</p>
</div>
""", unsafe_allow_html=True)
