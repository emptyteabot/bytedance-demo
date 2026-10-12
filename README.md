# Cross-Border Commerce Risk Operations Demo

A runnable Streamlit portfolio prototype for cross-border commerce operations. It demonstrates how logistics risk, seller-health signals, review analysis and advertising-budget controls can be brought into one decision interface.

**Demo:** [bytedance-demo.streamlit.app](https://bytedance-demo.streamlit.app)

## Modules

- Seller-performance monitoring and threshold-based alerts.
- Port and logistics-delay visualization.
- ROAS and spend-velocity budget rules.
- LLM-assisted review classification with a local fallback path.
- Filterable operations dashboard built with Streamlit and Plotly.

## Data scope

The dashboard uses synthetic data generated with Faker and statistical distributions. Metrics shown in the interface demonstrate product behavior; they are not production business results.

## Run locally

```bash
git clone https://github.com/emptyteabot/bytedance-demo.git
cd bytedance-demo
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Documentation

- `PROJECT_SUMMARY.md` — scope and design rationale.
- `DEPLOYMENT.md` and `DEPLOYMENT_GUIDE.md` — deployment paths.
- `生产级扩展路线图.md` — changes required for production data, storage and monitoring.
- `演示视频脚本.md` — reviewer walkthrough.

## Stack

`Python` · `Streamlit` · `Plotly` · `Faker` · `DeepSeek-compatible API`
