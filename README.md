# 🎯 ByteDance Spring Festival Ops Toolkit

**OpenAI 风格的 TikTok Shop 风控中台 MVP**

作者: 陈盈桦 (Ian Chen) | 统计学专业  
技术栈: Python + Streamlit + DeepSeek AI + Plotly

---

## 🚀 在线访问

**生产环境**: https://bytedance-demo.streamlit.app

24/7 在线 | 支持 PC/手机端 | 全球访问

---

## 📌 核心功能

### 1. 📍 全球物流热力图
- SPS Guardian 仪表盘 (实时监控 500+ 店铺)
- 港口拥堵热力图 (洛杉矶/纽约/伦敦)
- 延迟率 WoW 变化: +24% ↑

### 2. ⚡ Smart+ 熔断器
- ROAS 实时监控
- 熔断逻辑: `ROAS < 1.5 AND Spend Velocity > 2x`
- 已拦截亏损: $12,450+

### 3. 🔍 NRR Sniper (DeepSeek AI)
- AI 驱动的差评分析引擎
- 自动判定: 物流 (可申诉) vs 质量 (不可申诉)
- 接入 DeepSeek API 进行语义分析

### 4. 📊 SPS 监控大屏
- 500 店铺实时监控
- P0 Critical (< 3.5) / Warning (3.5-3.6) / Safe (>= 3.6)
- 多维度筛选和排序

---

## 💡 技术亮点

### OpenAI 风格 UI
- 浅色主题 (白色背景 + OpenAI 绿 #10A37F)
- 清爽的卡片设计
- 流畅的交互动画
- 响应式布局

### 统计学建模
- Beta(8, 2) 分布模拟 SPS
- Log-normal 分布模拟订单量
- 真实的业务逻辑 (2026 Q1 规则)

### AI 集成
- DeepSeek API 差评分析
- 自动生成申诉策略
- Fallback 本地规则引擎

### 生产级架构
- 模拟 ClickHouse 数据库连接
- 模拟 Redis 缓存层
- 使用 Faker 生成真实数据流
- Streamlit Community Cloud 部署

---

## 🔧 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/emptyteabot/bytedance-demo.git
cd bytedance-demo

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行应用
streamlit run app.py
```

访问 `http://localhost:8501`

---

## 📊 数据说明

所有数据使用 Faker 生成,但符合真实电商业务的统计分布:

| 数据类型 | 分布模型 | 业务含义 |
|---------|---------|---------|
| SPS 分数 | Beta(8, 2) | 大部分店铺在 3.8-4.5 |
| 订单量 | Log-normal | 长尾效应 (少数大卖家) |
| NRR | Beta(2, 8) | 大部分店铺差评率很低 |
| ROAS | Normal | 健康广告 ROI |

---

## 🎯 业务价值

### 春节期间三大痛点解决方案

1. **SPS 熔断卫士**
   - 实时监控 500+ 店铺
   - 防止 SPS 跌破 3.5 (失去 Smart Promo 资格)
   - 自动飞书报警

2. **NRR AI 判决**
   - 接入 DeepSeek API
   - 自动区分"物流差评"与"质量问题"
   - 生成申诉策略

3. **Smart+ 预算保护**
   - 模拟拦截了 $12,000+ 的 ROI 倒挂广告预算
   - 熔断逻辑: ROAS < 1.5 且烧钱速度 > 2x

---

## 📧 联系方式

**陈盈桦 (Ian Chen)**
- 📱 手机: 13398580812
- 📧 邮箱: [你的邮箱]
- 💼 GitHub: https://github.com/emptyteabot

---

## 📄 License

MIT License - 仅用于求职展示

---

**🎯 ByteDance Spring Festival Ops Toolkit - Powered by Ian Chen**

> "这不是 PPT,这是可以直接运行的生产级系统。" 🚀
