# 🚀 Streamlit Community Cloud 部署指南

## 📋 部署步骤 (5 分钟完成)

### 1. 访问 Streamlit Cloud
打开浏览器,访问: https://share.streamlit.io/

### 2. 登录 GitHub
点击 "Sign in with GitHub" 使用你的 GitHub 账号登录

### 3. 创建新应用
1. 点击右上角 "New app" 按钮
2. 填写以下信息:
   - **Repository**: `emptyteabot/bytedance-demo`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (可选): 自定义域名,如 `bytedance-ops-toolkit`

### 4. 配置 Secrets (重要!)
1. 点击 "Advanced settings"
2. 在 "Secrets" 文本框中粘贴以下内容:

```toml
# DeepSeek API Configuration
DEEPSEEK_API_KEY = "sk-d86589fb80f248cea3f4a843eaebce5a"

# Database Configuration (模拟)
[database]
clickhouse_host = "clickhouse.bytedance.internal"
clickhouse_port = 9000
redis_host = "redis.bytedance.internal"
redis_port = 6379
```

### 5. 部署!
点击 "Deploy!" 按钮

等待 2-3 分钟,应用会自动构建和部署。

---

## ✅ 部署成功后

你会获得一个公开 URL,类似:
```
https://bytedance-ops-toolkit.streamlit.app
```

或者:
```
https://emptyteabot-bytedance-demo-app-xxxxx.streamlit.app
```

### 测试清单
- [ ] 页面能正常加载
- [ ] 顶部显示 "✅ 已连接 ClickHouse/Redis/DeepSeek API"
- [ ] 4 个 Tab 都能正常切换
- [ ] NRR Sniper 能正常分析差评
- [ ] 图表能正常显示

---

## 🔧 常见问题

### Q1: 部署失败,显示 "ModuleNotFoundError"
**A**: 检查 `requirements.txt` 是否包含所有依赖:
```
streamlit==1.31.0
pandas==2.2.0
numpy==1.26.3
plotly==5.18.0
faker==22.6.0
requests==2.31.0
```

### Q2: DeepSeek API 调用失败
**A**: 检查 Secrets 配置是否正确,确保 API Key 没有多余的空格或引号。

### Q3: 页面加载很慢
**A**: 这是正常的,Streamlit Community Cloud 免费版在冷启动时需要 10-20 秒。

### Q4: 如何更新应用?
**A**: 只需 `git push` 到 GitHub,Streamlit Cloud 会自动重新部署。

### Q5: 如何查看日志?
**A**: 在 Streamlit Cloud 控制台,点击应用名称 → "Manage app" → "Logs"

---

## 📱 分享给 HR

部署成功后,你可以直接在邮件中写:

```
🔗 系统访问地址: https://bytedance-ops-toolkit.streamlit.app

(服务器 24h 在线,支持 PC/手机端访问,模拟了生产环境的 Redis/ClickHouse 延迟)
```

---

## 🎯 自定义域名 (可选)

如果你有自己的域名,可以配置 CNAME:

1. 在 Streamlit Cloud 控制台,点击 "Settings" → "Custom domain"
2. 添加你的域名,如 `ops.ianchendev.com`
3. 在你的 DNS 提供商添加 CNAME 记录:
   ```
   ops.ianchendev.com  CNAME  emptyteabot-bytedance-demo-app-xxxxx.streamlit.app
   ```

---

## 🔒 安全提示

- ✅ Secrets 不会被提交到 GitHub
- ✅ Secrets 只在 Streamlit Cloud 服务器上可见
- ✅ 应用默认是公开的,任何人都可以访问
- ⚠️ 不要在代码中硬编码 API Key

---

## 📊 监控和分析

Streamlit Cloud 提供基础的监控:
- 访问量统计
- 错误日志
- 资源使用情况

访问: https://share.streamlit.io/apps → 选择你的应用 → "Analytics"

---

**部署完成后,记得把 URL 更新到 README.md 中!** 🚀
