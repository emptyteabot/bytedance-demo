# 🚀 Streamlit Community Cloud 部署指南

## ✅ 已完成

1. ✅ 创建 OpenAI 风格的 app.py
2. ✅ 配置 .streamlit/config.toml (浅色主题)
3. ✅ 创建 requirements.txt
4. ✅ 推送到 GitHub: https://github.com/emptyteabot/bytedance-demo

## 📋 部署步骤

### 1. 访问 Streamlit Community Cloud

打开浏览器访问: https://share.streamlit.io/

### 2. 登录 GitHub 账号

点击 "Sign in with GitHub" 使用你的 GitHub 账号登录

### 3. 创建新应用

1. 点击 "New app" 按钮
2. 选择仓库: `emptyteabot/bytedance-demo`
3. 选择分支: `main`
4. 主文件路径: `app.py`
5. App URL (可选): 自定义域名前缀,例如 `bytedance-ops-toolkit`

### 4. 配置 Secrets (重要!)

在 "Advanced settings" 中,点击 "Secrets",粘贴以下内容:

```toml
# DeepSeek API Configuration
DEEPSEEK_API_KEY = "sk-d86589fb80f248cea3f4a843eaebce5a"

# Database Configuration (Simulated)
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 8123
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

### 5. 部署

点击 "Deploy!" 按钮,等待 2-3 分钟

### 6. 访问应用

部署成功后,你会获得一个 URL,格式如下:
```
https://bytedance-ops-toolkit.streamlit.app
```

## 🎯 应用特性

### OpenAI 风格设计
- ✅ 白色背景 (#FFFFFF)
- ✅ 次级背景 (#F7F7F8)
- ✅ OpenAI 绿色主题 (#10A37F)
- ✅ 清爽的卡片设计
- ✅ 柔和阴影效果

### 系统状态显示
- ✅ 已连接 ClickHouse
- ✅ 已连接 Redis
- ✅ 已连接 DeepSeek API

### 4 个核心模块
1. **📍 物流热力图** - 全球港口拥堵监控
2. **⚡ Smart+ 熔断器** - ROAS 实时监控
3. **🔍 NRR Sniper** - AI 差评分析引擎
4. **📊 SPS 监控** - 店铺实时监控大屏

### 数据模拟
- 使用 Faker 生成 500 家店铺数据
- 模拟春节物流危机场景
- 实时 ROAS 熔断演示
- AI 差评分类 (物流/质量/服务)

## 🔧 本地测试

在部署前,可以本地测试:

```bash
cd "C:/Users/陈盈桦/Desktop/ByteDance_SpringFestival_Ops_Toolkit_Ian"
streamlit run app.py
```

访问: http://localhost:8501

## 📝 注意事项

1. **Secrets 配置**: 必须在 Streamlit Cloud 中配置 secrets,否则应用无法访问 API
2. **依赖版本**: requirements.txt 中的版本已锁定,确保兼容性
3. **数据刷新**: 应用使用 @st.cache_data 缓存,60秒自动刷新
4. **性能优化**: 500 家店铺数据量适中,响应速度快

## 🎉 完成!

部署成功后,你将拥有一个:
- 🎨 顶级 OpenAI 风格的 UI
- 📊 4 个核心风控模块
- 🚀 一键部署到云端
- 🌐 全球访问 (无需 VPN)

GitHub 仓库: https://github.com/emptyteabot/bytedance-demo
