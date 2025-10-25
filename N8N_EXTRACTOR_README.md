# N8N Template Extractor

自动化工具，用于从 n8n.io 批量下载工作流模板的 JSON 文件。

## 功能特性

- ✅ 自动访问 20 个 n8n 工作流模板页面
- ✅ 模拟点击 "Use for free" 按钮
- ✅ 提取并保存 JSON 模板到本地
- ✅ 错误处理和重试机制
- ✅ 生成详细的执行报告

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

如果遇到权限问题，可以使用：

```bash
python -m playwright install chromium
```

## 使用方法

### 基本用法

```bash
python extract_n8n_templates.py
```

脚本将：
1. 启动 Chromium 浏览器（非无头模式，可以看到操作过程）
2. 依次访问 20 个模板页面
3. 自动点击按钮并提取 JSON
4. 保存文件到 `n8n_templates/` 目录
5. 生成执行摘要报告

### 输出结构

```
n8n_templates/
├── reddit-ai-digest.json
├── automated-reddit-lead-generation.json
├── monitor-reddit-job-posts.json
├── ...
└── _extraction_summary.json
```

## 模板清单

脚本将提取以下 20 个模板：

### Reddit 直连场景（10个）
1. reddit-ai-digest.json - Reddit AI 摘要
2. automated-reddit-lead-generation.json - 自动化潜在客户生成
3. monitor-reddit-job-posts.json - 监控工作发布
4. generate-startup-ideas.json - 生成创业想法
5. reddit-comment-sentiment.json - 评论情感分析
6. analyze-reddit-content.json - 内容分析
7. reddit-brand-engagement.json - 品牌互动
8. reddit-lead-finder.json - 潜在客户发现
9. analyze-reddit-posts.json - 帖子分析
10. transform-reddit-to-linkedin.json - Reddit 转 LinkedIn

### 多平台监控场景（10个）
11. social-sentiment-dashboard.json - 社交情感仪表板
12. monitor-social-trends.json - 监控社交趋势
13. generate-content-strategy.json - 生成内容策略
14. reddit-x-tech-trend.json - X 和 Reddit 技术趋势
15. monitor-content-trends.json - 监控内容趋势
16. track-regional-sentiment.json - 追踪区域情感
17. discover-social-leads.json - 发现社交潜在客户
18. ai-social-thought-leadership.json - AI 社交思想领导力
19. monitor-brand-x.json - 监控品牌提及
20. monitor-facebook-groups.json - 监控 Facebook 群组

## 执行报告

执行完成后，脚本会显示：

```
======================================================================
EXTRACTION SUMMARY
======================================================================

✓ Successful: 18/20
  - reddit-ai-digest.json
  - automated-reddit-lead-generation.json
  ...

✗ Failed: 2/20
  - some-template.json: Button not found
  - another-template.json: Timeout

======================================================================
Summary saved to: n8n_templates/_extraction_summary.json
```

## 故障排除

### 问题：浏览器无法启动

**解决方案：**
```bash
# 重新安装浏览器
playwright install --force chromium

# 或安装系统依赖
playwright install-deps
```

### 问题：按钮找不到

某些页面可能：
- 加载较慢，需要更长等待时间
- UI 结构变化，需要更新选择器
- 需要登录或特定权限

**解决方案：**
- 查看浏览器窗口中的实际操作
- 手动调整脚本中的 `selectors` 列表
- 增加等待时间 `await asyncio.sleep()`

### 问题：JSON 内容为空

**解决方案：**
- n8n 可能使用不同的复制机制
- 脚本会尝试从页面 `<textarea>` 或 `<pre>` 元素提取
- 如果失败，可能需要使用剪贴板 API（需要额外权限）

## 高级配置

### 修改为无头模式

在 `extract_n8n_templates.py` 中修改：

```python
browser = await p.chromium.launch(headless=True)  # 改为 True
```

### 增加超时时间

```python
await page.goto(url, wait_until="networkidle", timeout=60000)  # 60秒
```

### 添加更多模板

在 `TEMPLATES` 列表中添加：

```python
{"filename": "your-template.json", "url": "https://n8n.io/workflows/..."},
```

## 技术细节

- **浏览器引擎**: Chromium (via Playwright)
- **异步处理**: asyncio + async/await
- **错误处理**: 每个模板独立处理，失败不影响其他
- **选择器策略**: 多重选择器回退机制
- **输出格式**: UTF-8 编码的 JSON 文件

## 注意事项

1. **网络要求**: 需要稳定的网络连接访问 n8n.io
2. **速率限制**: 脚本在请求之间有 2 秒延迟，避免触发限制
3. **浏览器窗口**: 默认显示浏览器窗口，方便调试
4. **文件覆盖**: 重复运行会覆盖已存在的文件

## 许可证

本脚本仅用于教育和个人使用。请遵守 n8n.io 的使用条款。
