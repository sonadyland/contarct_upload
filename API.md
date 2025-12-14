# 合同上传服务接口文档

- 基础地址：`http://localhost:18013`
- 内容类型：`application/json`
- 认证：无
- 说明：默认合同仅允许一个处于激活状态；上传默认合同会自动停用其他默认合同。

## 1. 上传订单合同（创建/覆盖）

- 方法：`POST`
- 路径：`/contracts`
- 描述：按订单号上传合同 JSON。订单号已存在时覆盖其合同内容；不存在时创建新合同。
- 请求体：
```json
{
  "order_no": "ORD-001",
  "content": { "title": "contract v1", "amount": 100 }
}
```
- 成功响应：
```json
{
  "data": {
    "id": 1,
    "order_no": "ORD-001",
    "content": { "title": "contract v1", "amount": 100 },
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  "message": "创建成功"
}
```
- 覆盖响应：
```json
{
  "data": {
    "id": 1,
    "order_no": "ORD-001",
    "content": { "title": "contract v2", "amount": 200 },
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:05:00"
  },
  "message": "覆盖成功"
}
```
- 状态码：`200`

示例（curl）：
```bash
curl -X POST "http://localhost:18013/contracts" \
  -H "Content-Type: application/json" \
  -d '{
        "order_no": "ORD-001",
        "content": { "title": "contract v2", "amount": 200 }
      }'
```

## 2. 获取订单合同

- 方法：`GET`
- 路径：`/contracts/{order_no}`
- 描述：按订单号获取合同。
- 路径参数：
  - `order_no`：字符串，订单号
- 成功响应：
```json
{
  "id": 1,
  "order_no": "ORD-001",
  "content": { "title": "contract v2", "amount": 200 },
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:05:00"
}
```
- 失败响应（未找到）：
```json
{
  "detail": "Contract not found"
}
```
- 状态码：`200` / `404`

示例（curl）：
```bash
curl "http://localhost:18013/contracts/ORD-001"
```

## 3. 上传并激活默认合同（唯一激活）

- 方法：`POST`
- 路径：`/default`
- 描述：上传默认合同并将其设为激活；其他默认合同自动设置为非激活。
- 请求体：
```json
{
  "content": { "title": "default", "version": 1 }
}
```
- 成功响应：
```json
{
  "id": 2,
  "content": { "title": "default", "version": 1 },
  "is_active": true,
  "created_at": "2025-01-01T00:10:00"
}
```
- 状态码：`200`

示例（curl）：
```bash
curl -X POST "http://localhost:18013/default" \
  -H "Content-Type: application/json" \
  -d '{ "content": { "title": "default", "version": 1 } }'
```

## 4. 获取当前激活的默认合同

- 方法：`GET`
- 路径：`/default`
- 描述：获取当前激活的默认合同。
- 成功响应：
```json
{
  "id": 2,
  "content": { "title": "default", "version": 1 },
  "is_active": true,
  "created_at": "2025-01-01T00:10:00"
}
```
- 失败响应（未找到）：
```json
{
  "detail": "Default contract not found"
}
```
- 状态码：`200` / `404`

示例（curl）：
```bash
curl "http://localhost:18013/default"
```

## 错误响应汇总

- `404 Contract not found`：按订单号查询结果不存在
- `404 Default contract not found`：当前没有激活的默认合同

## 部署说明

- 本地运行：`uvicorn app.main:app --host 0.0.0.0 --port 18013`
- Docker：`docker build -t contract-upload . && docker run -d -p 18013:18013 contract-upload`
- Docker Compose：`docker compose up -d`

> 通过 `http://localhost:18013/docs` 可使用自动生成的交互式文档进行调试。