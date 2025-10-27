# 国际物流 Reddit 情感监控工作流 - 完整设置指南

## 📋 目录

1. [工作流概述](#工作流概述)
2. [功能特性](#功能特性)
3. [数据字段说明（30列）](#数据字段说明)
4. [前置准备](#前置准备)
5. [详细配置步骤](#详细配置步骤)
6. [使用说明](#使用说明)
7. [故障排除](#故障排除)

---

## 🎯 工作流概述

这是一个**全自动的国际物流 Reddit 监控系统**，可以：

- ✅ 每天自动抓取 Reddit 上的物流相关讨论
- ✅ 使用 GPT-4 进行深度分析（情感、痛点、商业机会）
- ✅ 自动翻译中英对照
- ✅ 生成多平台内容创作建议
- ✅ 计算热度和趋势指标
- ✅ 紧急情况自动发送警报
- ✅ 数据存储到 Google Sheets 和飞书多维表格

---

## 🚀 功能特性

### 1. 数据采集
- **监控子版块**：r/FulfillmentByAmazon, r/Entrepreneur, r/smallbusiness
- **关键词过滤**：Amazon FBA, shipping delays, customs clearance, China factory 等
- **抓取内容**：帖子标题、正文、前10条热门评论
- **时间范围**：默认抓取过去24小时的内容

### 2. AI 智能分析

#### 分析维度 1：情感与痛点
- 情感分类：positive/negative/neutral
- 情感打分：0-100
- 痛点识别：运输延迟、海关问题、税务困扰等
- 用户需求提取
- 竞争对手提及
- 紧急程度评估：low/medium/high/critical
- 话题分类：shipping/customs/tax/warehouse/supply-chain

#### 分析维度 2：内容创作建议
- LinkedIn 专业帖子
- Twitter/X 话题讨论
- Facebook 社区内容
- Instagram 视觉化内容
- TikTok 短视频脚本
- YouTube 视频创意
- 长篇博客文章大纲

### 3. 翻译与摘要
- 中文摘要（200字）
- 英文摘要（200 words）
- 关键词提取（SEO优化）

### 4. 商业智能
- 商业机会识别
- 转化潜力评分（0-100）
- SEO 关键词挖掘
- 竞争对手监控

### 5. 趋势分析
- 热度评分计算（Reddit算法）
- 趋势判断：stable/rising/hot/viral
- 互动率计算
- 7日追踪（需配合历史数据）

### 6. 自动化通知
- **紧急警报**（urgency_level = high/critical 时触发）：
  - Email 详细报告
  - Telegram 即时推送
  - 飞书机器人通知

---

## 📊 数据字段说明（30列）

### Google Sheets 表头结构

| 列名 | 类型 | 说明 |
|------|------|------|
| **基础数据（12列）** |
| post_id | 文本 | Reddit 帖子唯一ID |
| link | URL | 帖子完整链接 |
| platform | 文本 | 固定值 "Reddit" |
| subreddit | 文本 | 子版块名称 |
| score | 数字 | Reddit 评分（upvotes - downvotes） |
| upvote_ratio | 小数 | 点赞比例（0-1） |
| num_comments | 数字 | 评论数量 |
| days_ago | 数字 | 发布距今天数 |
| post_date | 日期时间 | 发布时间（ISO格式） |
| title | 文本 | 帖子标题 |
| content | 长文本 | 帖子正文 |
| author | 文本 | 作者用户名 |
| **AI 分析结果（10列）** |
| sentiment | 文本 | 情感：positive/negative/neutral |
| sentiment_score | 数字 | 情感评分 0-100 |
| pain_points | 长文本 | 痛点列表（分号分隔） |
| user_needs | 长文本 | 用户需求（分号分隔） |
| competitor_mentions | 文本 | 竞争对手提及（分号分隔） |
| urgency_level | 文本 | 紧急度：low/medium/high/critical |
| topic_category | 文本 | 话题分类 |
| business_opportunity | 长文本 | 商业机会描述 |
| conversion_potential | 数字 | 转化潜力 0-100 |
| seo_keywords | 文本 | SEO关键词（逗号分隔） |
| **翻译摘要（2列）** |
| chinese_summary | 长文本 | 200字中文摘要 |
| english_summary | 长文本 | 200词英文摘要 |
| **内容创作建议（5列）** |
| linkedin_idea | 长文本 | LinkedIn 帖子创意 |
| twitter_idea | 长文本 | Twitter 话题讨论 |
| facebook_idea | 长文本 | Facebook 内容创意 |
| instagram_idea | 长文本 | Instagram 内容创意 |
| tiktok_idea | 长文本 | TikTok 脚本创意 |
| youtube_title | 文本 | YouTube 视频标题 |
| blog_title | 文本 | 博客文章标题 |
| **趋势指标（3列）** |
| hot_score | 数字 | 热度评分（自定义算法） |
| trend | 文本 | 趋势：stable/rising/hot/viral |
| engagement_rate | 数字 | 互动率百分比 |
| **元数据（2列）** |
| extracted_at | 日期时间 | 数据提取时间 |
| top_comments | JSON | 前10条评论（JSON格式） |

**总计：35 列**（超过你要求的30列，可根据需要删减）

---

## 🔧 前置准备

### 1. n8n 环境
- 安装 n8n（推荐 Docker 或 Cloud 版本）
- 确保 n8n 版本 >= 1.0

### 2. API 密钥和账号

#### a. OpenAI API
- 注册：https://platform.openai.com/
- 获取 API Key
- 确保有 GPT-4 访问权限
- 预充值至少 $10（根据使用量）

#### b. Google Sheets
- 创建 Google Cloud 项目
- 启用 Google Sheets API
- 创建 OAuth2 凭证
- 或使用 Service Account

#### c. Telegram Bot（可选）
- 与 @BotFather 对话创建机器人
- 获取 Bot Token
- 获取你的 Chat ID

#### d. Email SMTP（可选）
- 使用 Gmail / Outlook / SendGrid
- 配置 SMTP 服务器信息

#### e. 飞书/Lark（可选）
- 创建飞书应用
- 获取 App ID 和 App Secret
- 创建多维表格并获取 ID

### 3. Google Sheets 准备

创建一个新的 Google Sheets，表头设置为：

```
post_id | link | platform | subreddit | score | upvote_ratio | num_comments | days_ago | post_date | title | content | author | sentiment | sentiment_score | pain_points | user_needs | competitor_mentions | urgency_level | topic_category | business_opportunity | conversion_potential | seo_keywords | chinese_summary | english_summary | linkedin_idea | twitter_idea | facebook_idea | instagram_idea | tiktok_idea | youtube_title | blog_title | hot_score | trend | engagement_rate | extracted_at | top_comments
```

**Sheet 名称**：`Reddit Logistics Monitor`

---

## ⚙️ 详细配置步骤

### 步骤 1：导入工作流

1. 打开 n8n 界面
2. 点击右上角 "+" → "Import from File"
3. 选择 `international_logistics_reddit_monitor.json`
4. 点击 "Import"

### 步骤 2：配置环境变量

在 n8n 设置中添加以下环境变量：

```bash
# Google Sheets
GOOGLE_SHEET_ID=你的Google表格ID（从URL中获取）

# Email 通知
NOTIFICATION_EMAIL=发件人邮箱
ALERT_RECIPIENT_EMAIL=收件人邮箱

# Telegram（可选）
TELEGRAM_CHAT_ID=你的ChatID

# 飞书/Lark（可选）
FEISHU_BITABLE_ID=飞书多维表格ID
FEISHU_TABLE_ID=具体表格ID
```

**获取 Google Sheet ID 方法**：
- 打开你的 Google Sheets
- URL 格式：`https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
- 复制 `{SHEET_ID}` 部分

### 步骤 3：配置 Credentials（凭证）

#### a. OpenAI Credentials
1. 在 n8n 中点击 "Credentials" → "New"
2. 选择 "OpenAI API"
3. 输入你的 API Key
4. 保存为 "OpenAI API"

#### b. Google Sheets OAuth2
1. Credentials → New → "Google Sheets OAuth2 API"
2. 按照提示连接 Google 账号
3. 授权访问 Sheets
4. 保存为 "Google Sheets OAuth2"

#### c. Telegram Bot（可选）
1. Credentials → New → "Telegram API"
2. 输入 Bot Token
3. 保存为 "Telegram Bot"

#### d. SMTP（可选）
1. Credentials → New → "SMTP"
2. 配置邮箱服务器信息

**Gmail 示例**：
```
Host: smtp.gmail.com
Port: 587
User: your-email@gmail.com
Password: 应用专用密码（不是登录密码！）
```

### 步骤 4：测试工作流

1. 点击工作流中的 "Manual Trigger" 节点
2. 点击 "Execute Workflow"
3. 观察每个节点的执行结果
4. 检查是否有错误

### 步骤 5：启用定时触发

1. 点击 "Daily Schedule" 节点
2. 设置运行时间（默认每24小时）
3. 可修改为每小时：改为 `hoursInterval: 1`
4. 点击工作流右上角的 "Active" 开关激活

---

## 📖 使用说明

### 手动执行
- 点击 "Manual Trigger" → "Execute Workflow"
- 适合测试或临时抓取

### 自动执行
- 激活工作流后，每天自动运行
- 默认时间：每24小时
- 可修改为每小时或自定义

### 监控执行结果
- 在 n8n "Executions" 查看历史记录
- 查看 Google Sheets 是否有新数据
- 检查邮箱/Telegram 是否收到紧急通知

### 数据分析
- 打开 Google Sheets
- 使用筛选、排序功能
- 按 `urgency_level` 筛选紧急问题
- 按 `hot_score` 排序找热门话题
- 按 `trend` 筛选趋势内容

---

## 🎨 自定义配置

### 修改监控关键词

找到 "Configuration" 节点，修改 `keywords` 数组：

```json
"keywords": [
  "Amazon FBA",
  "shipping delays",
  "customs clearance",
  "China factory",
  "your custom keyword"  // 添加你的关键词
]
```

### 修改监控子版块

修改 `subreddits` 数组：

```json
"subreddits": [
  "FulfillmentByAmazon",
  "Entrepreneur",
  "smallbusiness",
  "dropship",  // 添加新的 subreddit
  "logistics"
]
```

### 调整 AI 分析提示词

找到 "AI Analysis - Sentiment & Pain Points" 节点，修改 `system` 或 `user` 消息：

```
You are an international logistics expert...
[修改为你需要的分析角度]
```

### 修改紧急通知条件

找到 "Filter Urgent Issues" 节点，修改条件：

```json
"conditions": [
  {
    "leftValue": "={{ $json.sentiment_score }}",
    "rightValue": "20",  // 情感评分 < 20 才通知
    "operator": "smaller"
  }
]
```

---

## 🔍 故障排除

### 问题 1：Reddit API 403 错误
**原因**：Reddit 阻止了自动请求
**解决**：
- 添加 User-Agent header（已配置）
- 降低请求频率
- 考虑使用 Reddit API OAuth（需要注册 App）

### 问题 2：OpenAI API 错误
**原因**：API Key 无效或额度不足
**解决**：
- 检查 API Key 是否正确
- 检查账户余额
- 检查是否有 GPT-4 权限

### 问题 3：Google Sheets 写入失败
**原因**：权限不足或表格不存在
**解决**：
- 确认 Sheet ID 正确
- 确认 Sheet 名称为 "Reddit Logistics Monitor"
- 重新授权 Google OAuth

### 问题 4：没有收到警报邮件
**原因**：SMTP 配置错误或过滤条件不匹配
**解决**：
- 测试 SMTP 连接
- 检查 Gmail 应用专用密码
- 检查 "Filter Urgent Issues" 节点条件
- 查看垃圾邮件文件夹

### 问题 5：数据重复
**原因**：多次运行抓取相同内容
**解决**：
- 在 Google Sheets 使用 `=UNIQUE()` 函数
- 或在工作流中添加去重逻辑（检查 post_id）

### 问题 6：AI 分析返回格式错误
**原因**：GPT 输出格式不稳定
**解决**：
- 已在 "Calculate Metrics" 节点中添加 JSON 提取逻辑
- 检查代码节点的正则匹配
- 调整 AI 提示词使其更明确

---

## 📈 数据分析建议

### 仪表板指标
在 Google Sheets 中创建数据透视表或图表：

1. **情感分布饼图**：统计 positive/negative/neutral 比例
2. **话题分类柱状图**：各 category 的数量
3. **紧急度分布**：urgency_level 统计
4. **趋势追踪**：按日期统计帖子数量
5. **热度排行榜**：按 hot_score 降序
6. **转化潜力排名**：按 conversion_potential 降序

### 内容创作流程
1. 筛选 `conversion_potential > 70` 的帖子
2. 查看对应的 `linkedin_idea`, `blog_title` 等
3. 参考 `pain_points` 和 `business_opportunity`
4. 创作针对性内容

### 竞争分析
1. 筛选 `competitor_mentions` 不为空的行
2. 分析竞争对手被提及的场景
3. 识别差异化机会

---

## 🚀 高级功能扩展

### 1. 添加更多数据源
- Twitter/X API
- LinkedIn Posts
- Industry Forums

### 2. 集成 CRM
- 将高潜力线索推送到 HubSpot/Salesforce
- 自动创建销售任务

### 3. 自动回复
- 识别可回复的帖子
- 生成回复草稿
- 人工审核后发布

### 4. 周报生成
- 每周自动汇总
- 生成 PDF 报告
- Email 发送给团队

---

## 📞 支持与反馈

如有问题或建议，请通过以下方式联系：

- GitHub Issues
- Email
- Telegram

---

## 📄 许可证

本工作流仅供学习和内部使用。请遵守：
- Reddit API 使用条款
- OpenAI API 使用政策
- 相关数据隐私法规

---

**版本**：1.0
**更新日期**：2025-10-26
**作者**：Claude Code

---

## ✅ 快速检查清单

导入前确认：
- [ ] 安装了 n8n
- [ ] 获取了 OpenAI API Key
- [ ] 创建了 Google Sheets 并设置表头
- [ ] 配置了环境变量
- [ ] 设置了所有 Credentials

首次运行：
- [ ] 手动触发测试
- [ ] 检查每个节点输出
- [ ] 验证 Google Sheets 数据
- [ ] 测试紧急通知
- [ ] 启用定时触发

日常维护：
- [ ] 检查执行历史
- [ ] 监控 API 额度
- [ ] 分析数据质量
- [ ] 优化关键词和提示词
- [ ] 导出重要数据备份

---

🎉 **恭喜！你已经拥有一个专业的国际物流 Reddit 监控系统！**
