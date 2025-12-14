# 合同上传服务 (FastAPI + SQLite)

- 端口：`18013`
- 功能：
  - 保存订单合同（订单号唯一、合同 JSON、创建/更新时间）
  - 保存默认合同（仅允许一个激活）
  - 接口：
    - `POST /contracts` 上传订单号与合同 JSON（存在则更新）
    - `GET /contracts/{order_no}` 按订单号获取合同
    - `POST /default` 上传并激活默认合同（自动停用其他）
    - `GET /default` 获取当前激活默认合同

## 本地启动（不使用 Docker）

```powershell
cd d:\Program\Pythons\Project\contract_upload
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 18013
```

打开 `http://localhost:18013/docs` 调试接口。

## Docker 构建与运行

```powershell
cd d:\Program\Pythons\Project\contract_upload
docker build -t contract-upload .
docker run -d -p 18013:18013 --name contract-upload contract-upload
```

打开 `http://localhost:18013/docs`。

## 使用 Docker Compose 运行（推荐）

- `docker-compose.yml` 已包含：
  - 端口映射 `18013:18013`
  - 持久化卷 `contract_data:/app/data`
  - 环境变量 `DATABASE_URL=sqlite:////app/data/contracts.db`

```powershell
cd d:\Program\Pythons\Project\contract_upload
# Docker Compose V2
docker compose up -d
# 如为旧版 Docker Compose
# docker-compose up -d
```

- 查看日志：
```powershell
docker compose logs -f
```
- 停止：
```powershell
docker compose down
```

## 示例请求

- 上传默认合同
```json
{
  "content": { "title": "default", "version": 1 }
}
```
- 上传订单合同
```json
{
  "order_no": "ORD-001",
  "content": { "title": "contract for ORD-001", "amount": 1000 }
}
```

## 说明

- 默认合同仅能激活一个，上传新默认合同时自动将其他默认合同设为非激活。
- SQLite 数据文件位置：容器内 `/app/data/contracts.db`（通过 Compose 的卷持久化）。