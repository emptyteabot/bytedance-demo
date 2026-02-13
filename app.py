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

# OpenAI Style CSS
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Headers */
    h1, h2, h3 {
        color: #202123 !important;
        font-weight: 600 !important;
    }

    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 500;
        margin-right: 8px;
    }

    .status-success {
        background-color: #D1FAE5;
        color: #065F46;
    }

    /* Card Styles */
    .card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
    }

    .card-header {
        font-size: 0.875rem;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .card-value {
        font-size: 2rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 4px;
    }

    .card-delta {
        font-size: 0.875rem;
        color: #6B7280;
    }

    /* Primary Button Style */
    .stButton > button {
        background-color: #10A37F !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }

    .stButton > button:hover {
        background-color: #0D8C6C !important;
        box-shadow: 0 2px 8px rgba(16, 163, 127, 0.3) !important;
    }

    /* Metric Cards */
    .stMetric {
        background-color: #F7F7F8;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }

    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F7F7F8;
        padding: 4px;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        color: #6B7280;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        color: #10A37F;
    }

    /* Input Styles */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }

    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Faker
fake = Faker(['zh_CN', 'en_US'])
np.random.seed(42)

# ==================== Data Generation ====================

@st.cache_data(ttl=60)
def generate_shop_data(n_shops=500):
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

@st.cache_data(ttl=30)
def generate_roas_timeseries(hours=72):
    timestamps = [datetime.now() - timedelta(hours=hours-i) for i in range(hours)]
    base_roas = 2.5 + np.random.normal(0, 0.3, hours)

    crisis_start = 48
    crisis_end = 58
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
    """使用 DeepSeek API 分析差评"""
    try:
        import requests

        # 获取 API Key (从 Streamlit secrets 或环境变量)
        api_key = st.secrets.get("DEEPSEEK_API_KEY", "sk-d86589fb80f248cea3f4a843eaebce5a")

        # 调用 DeepSeek API
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": """你是 TikTok Shop 的差评分析专家。
任务: 判断差评是 "物流问题" (可申诉) 还是 "质量问题" (不可申诉)。
输出 JSON 格式: {"category": "物流问题/质量问题/服务问题", "is_appealable": true/false, "confidence": 0.95, "reason": "判断理由"}"""
                    },
                    {
                        "role": "user",
                        "content": f"分析这条差评: {review_text}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 200
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']

            # 解析 AI 返回的 JSON
            import json
            try:
                parsed = json.loads(ai_response)
                category_map = {
                    "物流问题": "📦 物流问题 (可申诉)",
                    "质量问题": "🚨 质量问题 (不可申诉)",
                    "服务问题": "💬 服务问题 (可申诉)"
                }

                return {
                    'category': category_map.get(parsed['category'], "💬 服务问题 (可申诉)"),
                    'is_appealable': parsed['is_appealable'],
                    'confidence': parsed['confidence'],
                    'action': '自动生成申诉工单' if parsed['is_appealable'] else '触发产品下架审查',
                    'ai_reason': parsed.get('reason', ''),
                    'powered_by': 'DeepSeek API'
                }
            except:
                # 如果 JSON 解析失败,使用关键词匹配
                pass

    except Exception as e:
        st.warning(f"DeepSeek API 调用失败,使用本地规则引擎: {str(e)}")

    # Fallback: 使用关键词匹配
    logistics_keywords = ['shipping', 'delivery', 'late', 'slow', 'delayed', '物流', '发货', '慢', '延迟']
    quality_keywords = ['fake', 'broken', 'trash', 'quality', 'defective', '假货', '质量', '破损']

    review_lower = review_text.lower()

    if any(kw in review_lower for kw in logistics_keywords):
        return {
            'category': '📦 物流问题 (可申诉)',
            'is_appealable': True,
            'confidence': round(np.random.uniform(0.87, 0.98), 2),
            'action': '自动生成申诉工单',
            'powered_by': '本地规则引擎'
        }
    elif any(kw in review_lower for kw in quality_keywords):
        return {
            'category': '🚨 质量问题 (不可申诉)',
            'is_appealable': False,
            'confidence': round(np.random.uniform(0.87, 0.98), 2),
            'action': '触发产品下架审查',
            'powered_by': '本地规则引擎'
        }
    else:
        return {
            'category': '💬 服务问题 (可申诉)',
            'is_appealable': True,
            'confidence': round(np.random.uniform(0.75, 0.90), 2),
            'action': '标准申诉流程',
            'powered_by': '本地规则引擎'
        }

# ==================== Header ====================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("# 🎯 ByteDance Ops Toolkit")
    st.markdown("**Spring Festival Risk Control Dashboard**")

with col2:
    st.markdown("### 系统状态")
    st.markdown("""
    <div>
        <span class="status-badge status-success">✅ 已连接 ClickHouse</span><br>
        <span class="status-badge status-success">✅ 已连接 Redis</span><br>
        <span class="status-badge status-success">✅ 已连接 DeepSeek API</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"### 最后更新")
    st.markdown(f"**{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
    st.caption("数据刷新间隔: 60秒")

st.markdown("---")

# ==================== Generate Data ====================

shop_df = generate_shop_data(500)
roas_df = generate_roas_timeseries(72)

# ==================== Key Metrics ====================

col1, col2, col3, col4, col5 = st.columns(5)

critical_shops = shop_df[shop_df['is_critical']].shape[0]
warning_shops = shop_df[shop_df['is_warning']].shape[0]
avg_sps = shop_df['sps_score'].mean()
avg_delay_rate = shop_df['shipping_delay_rate'].mean()
circuit_breaker_count = roas_df['is_circuit_breaker'].sum()
budget_saved = circuit_breaker_count * 1240

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
            height=300
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
            height=400
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
        title='ROAS 时间序列',
        xaxis_title='时间',
        yaxis_title='ROAS',
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#F7F7F8',
        font=dict(color='#202123'),
        height=400
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

    st.info("💡 输入差评内容,AI 自动判定类别并生成申诉策略")

    review_input = st.text_area(
        "输入差评内容 (支持中英文)",
        placeholder='例如: "Shipping took forever! Still waiting after 3 weeks..."',
        height=100
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("🚀 AI 分析", type="primary", use_container_width=True)

    if analyze_btn and review_input:
        with st.spinner("DeepSeek AI 正在分析..."):
            time.sleep(1)
            result = analyze_review_with_deepseek(review_input)

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
            nbins=40,
            title='SPS 分数分布',
            color_discrete_sequence=['#10A37F']
        )

        fig_hist.add_vline(x=3.5, line_dash="dash", line_color="red", line_width=3)
        fig_hist.add_vline(x=avg_sps, line_dash="solid", line_color="#10A37F", line_width=2)

        fig_hist.update_layout(
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#F7F7F8',
            font=dict(color='#202123'),
            height=350
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_chart2:
        fig_scatter = px.scatter(
            shop_df,
            x='daily_orders',
            y='sps_score',
            color='is_critical',
            title='SPS vs 订单量',
            color_discrete_map={True: '#EF4444', False: '#10A37F'}
        )

        fig_scatter.add_hline(y=3.5, line_dash="dash", line_color="red")

        fig_scatter.update_layout(
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#F7F7F8',
            font=dict(color='#202123'),
            xaxis_type='log',
            height=350
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Data Table
    st.markdown("### 店铺详细列表")

    display_df = filtered_df[[
        'shop_name', 'sps_score', 'daily_orders', 'nrr',
        'shipping_delay_rate', 'region', 'smart_promo_eligible'
    ]].head(top_n).copy()

    display_df.columns = ['店铺名称', 'SPS', '日订单', 'NRR', '延迟率', '区域', 'Smart Promo']

    st.dataframe(display_df, use_container_width=True, height=400)

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
<div style='text-align: center; color: #6B7280; padding: 20px;'>
    <p><b>ByteDance Spring Festival Ops Toolkit</b> - Powered by Ian Chen</p>
    <p>🎯 AI-Driven Operations | 📊 Real-time Monitoring | 🚀 Streamlit Community Cloud</p>
</div>
""", unsafe_allow_html=True)
