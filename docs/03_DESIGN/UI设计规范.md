# UI/UX 设计规范

## 设计原则

### 核心理念
- **效率优先**: 减少操作步骤，提升运维效率
- **信息清晰**: 数据可视化，关键信息突出
- **一致性**: 统一的交互模式和视觉语言
- **容错性**: 防止误操作，提供撤销机制
- **响应式**: 适配多种设备和屏幕尺寸

### 设计目标
1. 降低学习成本，新用户快速上手
2. 提高操作效率，减少重复劳动
3. 增强数据可读性，辅助决策
4. 保证系统稳定性，避免误操作

---

## 色彩系统

### 主色调
```css
/* 品牌主色 */
--primary: #10A37F;           /* 主要操作、强调元素 */
--primary-hover: #0D8A6B;     /* 悬停状态 */
--primary-active: #0A6F56;    /* 激活状态 */
--primary-light: #E6F7F3;     /* 浅色背景 */
--primary-dark: #085D47;      /* 深色变体 */
```

### 功能色
```css
/* 状态色 */
--success: #52C41A;           /* 成功、正常 */
--warning: #FAAD14;           /* 警告、待处理 */
--error: #F5222D;             /* 错误、危险 */
--info: #1890FF;              /* 信息、提示 */

/* 中性色 */
--text-primary: #1F2937;      /* 主要文本 */
--text-secondary: #6B7280;    /* 次要文本 */
--text-disabled: #9CA3AF;     /* 禁用文本 */
--border: #E5E7EB;            /* 边框 */
--divider: #F3F4F6;           /* 分割线 */
--background: #FFFFFF;        /* 背景 */
--background-secondary: #F9FAFB; /* 次要背景 */
```

### 数据可视化色板
```css
/* 图表配色 */
--chart-1: #10A37F;
--chart-2: #1890FF;
--chart-3: #FAAD14;
--chart-4: #F5222D;
--chart-5: #722ED1;
--chart-6: #13C2C2;
--chart-7: #52C41A;
--chart-8: #EB2F96;
```

---

## 字体系统

### 字体家族
```css
/* 中文优先 */
--font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
               'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei',
               'Helvetica Neue', Helvetica, Arial, sans-serif;

/* 等宽字体（代码、日志） */
--font-mono: 'SF Mono', 'Consolas', 'Monaco', 'Courier New', monospace;
```

### 字号规范
```css
--font-size-xs: 12px;         /* 辅助信息 */
--font-size-sm: 14px;         /* 正文、表格 */
--font-size-base: 16px;       /* 基础文本 */
--font-size-lg: 18px;         /* 小标题 */
--font-size-xl: 20px;         /* 卡片标题 */
--font-size-2xl: 24px;        /* 页面标题 */
--font-size-3xl: 30px;        /* 大标题 */
```

### 字重规范
```css
--font-weight-normal: 400;    /* 正文 */
--font-weight-medium: 500;    /* 强调 */
--font-weight-semibold: 600;  /* 标题 */
--font-weight-bold: 700;      /* 重要标题 */
```

### 行高规范
```css
--line-height-tight: 1.25;    /* 标题 */
--line-height-normal: 1.5;    /* 正文 */
--line-height-relaxed: 1.75;  /* 长文本 */
```

---

## 组件库

### 按钮 (Button)

#### 类型
```jsx
/* 主要按钮 - 主要操作 */
<button className="btn-primary">
  确认部署
</button>

/* 次要按钮 - 次要操作 */
<button className="btn-secondary">
  取消
</button>

/* 危险按钮 - 危险操作 */
<button className="btn-danger">
  删除服务
</button>

/* 文本按钮 - 轻量操作 */
<button className="btn-text">
  查看详情
</button>
```

#### 尺寸
```css
/* 小按钮 */
.btn-sm {
  height: 28px;
  padding: 0 12px;
  font-size: 14px;
}

/* 默认按钮 */
.btn {
  height: 36px;
  padding: 0 16px;
  font-size: 14px;
}

/* 大按钮 */
.btn-lg {
  height: 44px;
  padding: 0 24px;
  font-size: 16px;
}
```

#### 状态
- **默认**: 正常可点击
- **悬停**: 背景色加深 10%
- **激活**: 背景色加深 20%
- **禁用**: 透明度 50%，不可点击
- **加载**: 显示加载图标，禁用点击

---

### 卡片 (Card)

#### 基础卡片
```jsx
<div className="card">
  <div className="card-header">
    <h3>服务器状态</h3>
    <button className="btn-text">刷新</button>
  </div>
  <div className="card-body">
    {/* 内容区域 */}
  </div>
  <div className="card-footer">
    <span className="text-secondary">最后更新: 2分钟前</span>
  </div>
</div>
```

#### 样式规范
```css
.card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F3F4F6;
}

.card-body {
  padding: 16px 0;
}

.card-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #F3F4F6;
}
```

---

### 表格 (Table)

#### 基础表格
```jsx
<table className="table">
  <thead>
    <tr>
      <th>服务名称</th>
      <th>状态</th>
      <th>CPU</th>
      <th>内存</th>
      <th>操作</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>api-gateway</td>
      <td><span className="badge-success">运行中</span></td>
      <td>45%</td>
      <td>2.3GB</td>
      <td>
        <button className="btn-text">重启</button>
      </td>
    </tr>
  </tbody>
</table>
```

#### 样式规范
```css
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table thead {
  background: #F9FAFB;
  border-bottom: 2px solid #E5E7EB;
}

.table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #6B7280;
}

.table td {
  padding: 12px 16px;
  border-bottom: 1px solid #F3F4F6;
}

.table tbody tr:hover {
  background: #F9FAFB;
}
```

#### 状态徽章
```css
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.badge-success {
  background: #E6F7F3;
  color: #085D47;
}

.badge-warning {
  background: #FFF7E6;
  color: #AD6800;
}

.badge-error {
  background: #FFF1F0;
  color: #A8071A;
}
```

---

### 图表 (Chart)

#### 设计原则
- 使用清晰的图例和标签
- 数据点可交互（悬停显示详情）
- 支持时间范围选择
- 提供数据导出功能

#### 折线图 (Line Chart)
```jsx
// 用于趋势分析：CPU、内存、流量等
<LineChart
  data={cpuData}
  xAxis="时间"
  yAxis="使用率 (%)"
  color="#10A37F"
  smooth={true}
/>
```

#### 柱状图 (Bar Chart)
```jsx
// 用于对比分析：服务请求量、错误统计等
<BarChart
  data={requestData}
  xAxis="服务名称"
  yAxis="请求数"
  color="#1890FF"
/>
```

#### 饼图 (Pie Chart)
```jsx
// 用于占比分析：资源分布、状态分布等
<PieChart
  data={statusData}
  colors={['#52C41A', '#FAAD14', '#F5222D']}
  showPercentage={true}
/>
```

#### 热力图 (Heatmap)
```jsx
// 用于时间分布：请求热力、错误分布等
<Heatmap
  data={trafficData}
  colorRange={['#E6F7F3', '#10A37F', '#085D47']}
/>
```

---

## 交互规范

### 反馈机制

#### 加载状态
```jsx
/* 按钮加载 */
<button className="btn-primary" disabled>
  <Spinner size="sm" />
  部署中...
</button>

/* 页面加载 */
<div className="loading-overlay">
  <Spinner size="lg" />
  <p>正在加载数据...</p>
</div>

/* 骨架屏 */
<Skeleton rows={5} />
```

#### 消息提示
```jsx
/* 成功提示 */
toast.success('部署成功！');

/* 错误提示 */
toast.error('部署失败，请检查配置');

/* 警告提示 */
toast.warning('服务器负载过高');

/* 信息提示 */
toast.info('新版本可用');
```

#### 确认对话框
```jsx
/* 危险操作确认 */
<Modal
  title="确认删除"
  type="danger"
  onConfirm={handleDelete}
>
  <p>确定要删除服务 <strong>api-gateway</strong> 吗？</p>
  <p className="text-error">此操作不可撤销！</p>
</Modal>
```

### 操作规范

#### 点击区域
- 最小点击区域: 44x44px (移动端)
- 桌面端按钮: 36px 高度
- 图标按钮: 32x32px 最小

#### 悬停效果
- 按钮: 背景色变化 + 光标变化
- 链接: 颜色变化 + 下划线
- 卡片: 阴影加深 + 轻微上移

#### 动画时长
```css
--transition-fast: 150ms;     /* 按钮、链接 */
--transition-base: 250ms;     /* 卡片、模态框 */
--transition-slow: 350ms;     /* 页面切换 */
```

---

## 响应式设计

### 断点规范
```css
/* 移动端 */
@media (max-width: 640px) {
  --breakpoint: 'mobile';
}

/* 平板 */
@media (min-width: 641px) and (max-width: 1024px) {
  --breakpoint: 'tablet';
}

/* 桌面端 */
@media (min-width: 1025px) {
  --breakpoint: 'desktop';
}

/* 大屏 */
@media (min-width: 1440px) {
  --breakpoint: 'wide';
}
```

### 布局适配

#### 移动端 (< 640px)
- 单列布局
- 侧边栏折叠为抽屉
- 表格横向滚动或卡片化
- 图表简化显示

#### 平板 (641px - 1024px)
- 两列布局
- 侧边栏可折叠
- 表格正常显示
- 图表完整显示

#### 桌面端 (> 1025px)
- 三列布局
- 侧边栏固定
- 表格完整功能
- 图表交互增强

### 组件适配示例
```css
/* 卡片网格 */
.card-grid {
  display: grid;
  gap: 16px;
}

/* 移动端: 1列 */
@media (max-width: 640px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}

/* 平板: 2列 */
@media (min-width: 641px) and (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 桌面端: 3列 */
@media (min-width: 1025px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## 暗色模式

### 色彩映射
```css
/* 暗色主题 */
[data-theme="dark"] {
  /* 主色调 */
  --primary: #10A37F;
  --primary-hover: #13BF8F;
  --primary-light: #0A3D2F;

  /* 背景色 */
  --background: #111827;
  --background-secondary: #1F2937;

  /* 文本色 */
  --text-primary: #F9FAFB;
  --text-secondary: #D1D5DB;
  --text-disabled: #6B7280;

  /* 边框色 */
  --border: #374151;
  --divider: #2D3748;

  /* 卡片 */
  --card-bg: #1F2937;
  --card-border: #374151;
  --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}
```

### 切换机制
```jsx
/* 主题切换器 */
<button onClick={toggleTheme} className="theme-toggle">
  {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
</button>

/* 自动检测系统主题 */
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
```

### 图表适配
```jsx
/* 暗色模式下的图表配色 */
const chartTheme = {
  dark: {
    backgroundColor: '#1F2937',
    textColor: '#F9FAFB',
    gridColor: '#374151',
    tooltipBg: '#111827',
  }
};
```

### 注意事项
- 保持足够的对比度 (WCAG AA 标准)
- 图标和图表需要适配
- 避免纯黑背景，使用深灰色
- 减少高亮度元素，降低眼睛疲劳

---

## 可访问性 (Accessibility)

### 键盘导航
- 所有交互元素支持 Tab 键导航
- 焦点状态清晰可见
- 支持快捷键操作

### 语义化 HTML
```html
<nav aria-label="主导航">
  <button aria-label="关闭对话框">×</button>
  <table role="grid" aria-label="服务器列表">
</nav>
```

### 颜色对比度
- 正文文本: 至少 4.5:1
- 大文本 (18px+): 至少 3:1
- 交互元素: 至少 3:1

---

## 设计资源

### Figma 组件库
- 按钮组件
- 表单组件
- 卡片组件
- 图表模板
- 图标库

### 图标系统
- 使用 Heroicons 或 Lucide Icons
- 统一尺寸: 16px, 20px, 24px
- 统一描边: 1.5px

### 间距系统
```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-2xl: 48px;
```

---

## 更新日志

- **2026-02-16**: 初始版本发布
