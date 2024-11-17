任务管理系统 API 文档
===================

基础信息
-------
- 基础URL: http://localhost:3000/api
- 所有请求和响应均使用 JSON 格式
- 认证方式: Bearer Token (待实现)

任务相关接口
----------

获取任务列表
^^^^^^^^^^
GET /tasks

**响应示例**::

    [
        {
            "id": 1,
            "title": "开发用户认证功能",
            "description": "实现用户登录、注册和权限控制功能",
            "type": "normal",
            "status": "进行中",
            "progress": 60,
            "createdAt": "2024-03-15 10:00:00",
            "completedAt": null
        }
    ]

获取单个任务
^^^^^^^^^^
GET /tasks/:id

**响应示例**::

    {
        "id": 1,
        "title": "开发用户认证功能",
        "description": "实现用户登录、注册和权限控制功能",
        "type": "normal",
        "status": "进行中",
        "progress": 60,
        "createdAt": "2024-03-15 10:00:00",
        "completedAt": null,
        "instances": []
    }

创建任务
^^^^^^^
POST /tasks

**请求参数**::

    {
        "title": "任务标题",
        "description": "任务描述",
        "type": "normal|deploy",
        "instances": []  // 部署任务必填
    }

**响应示例**::

    {
        "id": 1,
        "title": "任务标题",
        "description": "任务描述",
        "type": "normal",
        "status": "待处理",
        "progress": 0,
        "createdAt": "2024-03-20 10:00:00",
        "completedAt": null
    }

更新任务
^^^^^^^
PUT /tasks/:id

**请求参数**::

    {
        "title": "更新的标题",
        "description": "更新的描述",
        "status": "进行中",
        "progress": 50,
        "type": "normal|deploy",
        "instances": []  // 部署任务必填
    }

**响应示例**::

    {
        "id": 1,
        "title": "更新的标题",
        "description": "更新的描述",
        "status": "进行中",
        "progress": 50,
        "type": "normal",
        "instances": [],
        "createdAt": "2024-03-20 10:00:00",
        "completedAt": null
    }

删除任务
^^^^^^^
DELETE /tasks/:id

**响应**::

    204 No Content

搜索任务
^^^^^^^
GET /tasks/search?q=关键词

**响应示例**::

    [
        {
            "id": 1,
            "title": "包含关键词的任务",
            "description": "任务描述",
            "type": "normal",
            "status": "进行中",
            "progress": 50
        }
    ]

任务日志接口
----------

获取任务日志
^^^^^^^^^^
GET /tasks/:id/logs

**响应示例**::

    [
        {
            "timestamp": "2024-03-20T10:00:00.000Z",
            "message": "[INFO] Task-1 - 任务已创建: 开发用户认证功能"
        },
        {
            "timestamp": "2024-03-20T10:01:00.000Z",
            "message": "[INFO] Task-1 - 任务正在运行中，当前进度: 30%"
        },
        {
            "timestamp": "2024-03-20T10:02:00.000Z",
            "message": "[DEBUG] Task-1 - 系统状态正常 (内存: 45%, CPU: 30%)"
        }
    ]

**日志格式说明**:

- timestamp: ISO 8601 格式的时间戳
- message: 日志消息，格式为 "[日志级别] Task-任务ID - 具体消息"
- 日志级别包括: INFO, DEBUG, WARN, ERROR

实例相关接口
----------

获取实例列表
^^^^^^^^^^
GET /instances

**响应示例**::

    [
        {
            "id": 1,
            "name": "生产环境-1",
            "ip": "192.168.1.101",
            "region": "华东-上海",
            "status": "running",
            "specification": "8C16G",
            "cpuType": "Intel Xeon Platinum 8269CY",
            "lastHeartbeat": "2024-03-20 10:30:00"
        }
    ]

获取实例详情
^^^^^^^^^^
GET /instances/:id

**响应示例**::

    {
        "id": 1,
        "name": "生产环境-1",
        "ip": "192.168.1.101",
        "region": "华东-上海",
        "status": "running",
        "specification": "8C16G",
        "cpuType": "Intel Xeon Platinum 8269CY",
        "lastHeartbeat": "2024-03-20 10:30:00"
    }

获取实例状态
^^^^^^^^^^
GET /instances/:id/status

**响应示例**::

    {
        "status": "running",
        "lastHeartbeat": "2024-03-20 10:30:00"
    }

数据模型
-------

任务状态枚举::

    {
        "PENDING": "待处理",
        "IN_PROGRESS": "进行中",
        "COMPLETED": "已完成",
        "FAILED": "失败"
    }

任务类型枚举::

    {
        "NORMAL": "normal",
        "DEPLOY": "deploy"
    }

实例状态枚举::

    {
        "RUNNING": "running",
        "STOPPED": "stopped",
        "MAINTENANCE": "maintenance"
    }

状态码说明
--------
- 200: 请求成功
- 201: 创建成功
- 204: 删除成功
- 400: 请求参数错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器错误

Mock 模式说明
-----------
系统支持 Mock 模式，通过环境变量 REACT_APP_USE_MOCK 控制::

    REACT_APP_USE_MOCK=true  # 使用模拟数据
    REACT_APP_USE_MOCK=false # 使用真实 API

在 Mock 模式下：
- 所有数据都是模拟的，不会真正调用后端 API
- 支持基本的 CRUD 操作
- 任务日志会自动生成并更新
- 实例状态会随机变化
- 支持任务状态和进度的实时更新
- 支持日志的实时刷新和过滤