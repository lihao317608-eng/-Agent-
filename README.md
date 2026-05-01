# AI Content Monetization Agent（生产级完整版）

> 面向小红书/公众号的多 Agent 内容生产系统：登录鉴权、任务入队、异步生成、结果查询、前端控制台、容器化部署。

---

## 1. 最终搭建实操过程（从 0 到可运行）

以下流程按 **Ubuntu / macOS + Docker** 编写，Windows 用户建议使用 WSL2。

### Step 0：准备环境

必须安装：
- Docker 24+
- Docker Compose v2+
- Git

检查命令：

```bash
docker -v
docker compose version
git --version
```

### Step 1：克隆项目

```bash
git clone <your-repo-url>
cd -Agent-
```

### Step 2：配置环境变量

在项目根目录创建 `.env`：

```env
OPENAI_API_KEY=sk-xxxx
```

> 不填 `OPENAI_API_KEY` 也能跑通流程，系统会返回 Mock 输出用于联调。

### Step 3：一键拉起全服务

```bash
bash scripts/deploy.sh
```

该命令会执行：
1. 读取 `.env`
2. `docker compose up -d --build`
3. 输出访问地址

### Step 4：确认容器状态

```bash
docker compose ps
```

期望看到 5 个服务均为 `running`：
- `postgres`
- `redis`
- `backend`
- `worker`
- `frontend`

### Step 5：访问系统

- 前端控制台：http://localhost:3000
- 后端文档：http://localhost:8000/docs

### Step 6：实操联调（推荐）

#### 6.1 注册账号
在 Swagger 执行：`POST /auth/register`

```json
{
  "username": "demo",
  "password": "demo1234"
}
```

返回 `access_token`。

#### 6.2 登录获取 token（可选）
执行：`POST /auth/login`（form-data）
- username: demo
- password: demo1234

#### 6.3 创建内容任务
执行：`POST /tasks`，Header 添加：
`Authorization: Bearer <access_token>`

示例 body：

```json
{
  "topic": "35岁转型副业",
  "platform": "xiaohongshu",
  "count": 5,
  "use_evaluator": true
}
```

#### 6.4 查询任务结果
执行：`GET /tasks/{id}`（同样带 Bearer token）

当 `status=done` 时，返回：
- `trend_output`
- `generated_output`
- `rewritten_output`
- `evaluated_output`

---

## 2. 系统架构

```text
[Frontend Next.js]
      |
      v
[FastAPI API + JWT]
      |
      v
[PostgreSQL] <-> [Celery Worker] <-> [Redis]
                         |
                         v
                 [Multi-Agent Pipeline]
        Trend -> Content -> Rewrite -> Evaluator
```

---

## 3. 目录说明

```text
backend/
  app/
    agents/pipeline.py     # Agent 调用与模型封装
    auth.py                # JWT、密码哈希、鉴权
    main.py                # API 路由
    models.py              # User / ContentTask
    tasks.py               # Celery 异步任务
frontend/
  app/page.tsx             # 控制台页面
  lib/api.ts               # API 调用
scripts/deploy.sh          # 一键部署脚本
docker-compose.yml         # 生产编排
```

---

## 4. 常用运维命令

### 查看日志
```bash
docker compose logs -f backend
docker compose logs -f worker
docker compose logs -f frontend
```

### 重启服务
```bash
docker compose restart backend worker frontend
```

### 停止并清理
```bash
docker compose down
```

### 清理并重建（含镜像）
```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d
```

---

## 5. 生产上线建议（下一步）

1. 把 `JWT_SECRET` 改成强随机字符串。
2. 把 PostgreSQL/Redis 迁移到托管服务。
3. 后端加 API 限流和审计日志。
4. 加 Prompt 模板版本管理与 A/B 测试。
5. 加内容安全过滤与事实校验。
6. 用 Nginx + HTTPS 暴露 `frontend/backend`。

---

## 6. 当前已知限制

- 当前 `register` 未做验证码/邀请机制。
- `worker` 并发策略为默认，未按 CPU/队列优先级精调。
- 前端是最小可用控制台，建议后续补任务列表与分页。


## 7. 无二进制上传说明

仓库已移除 `.pyc` 等二进制缓存文件，只保留源码文本文件，适合在不支持二进制上传的平台提交。

如果你要打包源码，请使用：

```bash
git archive --format=zip -o source-only.zip HEAD
```

该压缩包仅包含 Git 跟踪的源码文件（不会包含运行时缓存）。
