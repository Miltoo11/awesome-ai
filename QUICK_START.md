# 🚀 快速开始指南 - 5分钟部署

## 📦 你需要的文件
- ✅ `international_logistics_reddit_monitor.json` - 工作流文件
- ✅ `WORKFLOW_SETUP_GUIDE.md` - 完整文档

---

## ⚡ 3步快速部署

### 步骤 1：准备 API 密钥（5分钟）

#### a. OpenAI API Key
1. 访问：https://platform.openai.com/api-keys
2. 点击 "Create new secret key"
3. 复制保存 `sk-...`

#### b. Google Sheets
1. 创建新的 Google Sheets
2. 第一行填入表头（复制下面这行）：
```
post_id	link	platform	subreddit	score	upvote_ratio	num_comments	days_ago	post_date	title	content	author	sentiment	sentiment_score	pain_points	user_needs	competitor_mentions	urgency_level	topic_category	business_opportunity	conversion_potential	seo_keywords	chinese_summary	english_summary	linkedin_idea	twitter_idea	facebook_idea	instagram_idea	tiktok_idea	youtube_title	blog_title	hot_score	trend	engagement_rate	extracted_at	top_comments
```
3. Sheet 名称改为：`Reddit Logistics Monitor`
4. 复制 URL 中的 Sheet ID（`/d/` 和 `/edit` 之间的部分）

---

### 步骤 2：导入 n8n 工作流（2分钟）

1. 打开 n8n（如果没有，访问 https://n8n.io 注册免费账号）
2. 点击右上角 "+" → "Import from File"
3. 选择 `international_logistics_reddit_monitor.json`
4. 点击 "Import"

---

### 步骤 3：配置凭证（3分钟）

#### a. 添加 OpenAI Credentials
1. 点击左侧 "Credentials" → "Add Credential"
2. 搜索 "OpenAI"
3. 粘贴你的 API Key
4. 保存

#### b. 添加 Google Sheets OAuth
1. Credentials → "Add Credential" → "Google Sheets OAuth2 API"
2. 点击 "Connect my account"
3. 授权你的 Google 账号
4. 保存

#### c. 设置环境变量
在工作流中找到 "Configuration" 节点，点击后：
- 将 `{{ $env.GOOGLE_SHEET_ID }}` 替换为你的实际 Sheet ID
- 或在 n8n 设置中添加环境变量 `GOOGLE_SHEET_ID`

---

## 🎯 测试运行（1分钟）

1. 点击工作流中的 "Manual Trigger" 节点
2. 点击右上角 "Test Workflow"
3. 等待执行完成（约1-2分钟）
4. 检查 Google Sheets 是否有新数据

---

## ✅ 成功标志

如果看到以下情况，说明成功了：
- ✅ 工作流所有节点都是绿色（成功）
- ✅ Google Sheets 中出现了新的数据行
- ✅ 数据包含：标题、情感分析、中文摘要等

---

## 🔄 启用自动运行

1. 点击工作流右上角的 "Inactive" 切换按钮
2. 变成 "Active"（绿色）
3. 现在工作流会每24小时自动运行！

---

## 📧 可选：配置通知

### Email 通知（Gmail 示例）

1. 进入 Gmail → 设置 → 启用"两步验证"
2. 生成"应用专用密码"：https://myaccount.google.com/apppasswords
3. 在 n8n 添加 SMTP Credential：
   - Host: `smtp.gmail.com`
   - Port: `587`
   - User: `your-email@gmail.com`
   - Password: `应用专用密码`

### Telegram 通知

1. 与 @BotFather 对话，发送 `/newbot`
2. 按提示创建机器人，获取 Token
3. 与 @userinfobot 对话，获取你的 Chat ID
4. 在 n8n 添加 Telegram Credential

---

## 🎨 自定义关键词

找到 "Configuration" 节点，修改：

```javascript
// 修改监控的关键词
keywords: [
  "Amazon FBA",
  "shipping delays",
  "customs clearance",
  "China factory",
  "你的关键词"  // 添加这里
]

// 修改监控的 subreddits
subreddits: [
  "FulfillmentByAmazon",
  "Entrepreneur",
  "smallbusiness",
  "你的subreddit"  // 添加这里
]
```

---

## 📊 查看结果

### Google Sheets 中你会看到：

| 列名 | 示例数据 |
|------|---------|
| title | "Customs delays from China to USA?" |
| sentiment | negative |
| pain_points | "customs clearance delays; high duties; unpredictable costs" |
| chinese_summary | "一位亚马逊FBA卖家遇到从中国发货到美国的海关延误问题..." |
| business_opportunity | "Offer customs consulting and pre-clearance services" |
| linkedin_idea | "How to avoid costly customs delays when importing from China..." |

---

## ❓ 常见问题

**Q: 为什么没有抓到数据？**
A: 检查关键词是否在过去24小时内有相关帖子。尝试扩大关键词范围。

**Q: OpenAI API 错误？**
A: 确认 API Key 正确，账户有余额，有 GPT-4 权限。

**Q: Google Sheets 写入失败？**
A: 确认 Sheet 名称是 `Reddit Logistics Monitor`，表头正确。

**Q: 数据是中文还是英文？**
A: 两者都有！`chinese_summary` 是中文，`english_summary` 是英文。

---

## 🎉 下一步

- 📖 阅读完整文档：`WORKFLOW_SETUP_GUIDE.md`
- 🎨 自定义分析维度和提示词
- 📧 配置紧急通知
- 📊 创建数据分析仪表板

---

## 💡 专业提示

1. **每天检查数据**：早上打开 Google Sheets 查看昨天的发现
2. **筛选高价值内容**：按 `conversion_potential` 降序排序
3. **内容创作灵感**：使用 `linkedin_idea` 和 `blog_title` 列
4. **竞争分析**：关注 `competitor_mentions` 列
5. **趋势追踪**：关注 `trend = hot` 或 `viral` 的帖子

---

**需要帮助？查看完整文档或联系支持！**

版本：1.0 | 更新：2025-10-26
