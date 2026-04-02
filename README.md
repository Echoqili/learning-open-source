# Learning Open Source

这是一个用于学习开源项目的仓库，目前收集了优秀的开源技能库。

## 当前内容

### 1. Product Manager Skills (来自 deanpeters/Product-Manager-Skills)

47个经过实战检验的PM技能 + 6个命令工作流，帮助产品经理和AI代理以专业水平执行产品管理工作。

**技能分类：**
- Component Skills (21) - PM工件模板
- Interactive Skills (20) - 自适应引导式发现
- Workflow Skills (6) - 完整端到端PM流程

**主要框架来源：**
- Teresa Torres - Continuous Discovery, OST
- Geoffrey Moore - Positioning
- Jeff Patton - User Story Mapping
- Mike Cohn - User Stories
- Amazon - Working Backwards

**快速使用：**
```bash
./scripts/run-pm.sh skill prioritization-advisor "12个需求，1个sprint"
./scripts/run-pm.sh command discover "减少 onboarding 流失"
```

---

### 2. DDD 六边形架构技能包 (来自 fuzhengwei/xfg-ddd-skills)

一套完整的 DDD 六边形架构工程搭建与开发解决方案，从项目创建、分层设计、代码规范到 DevOps 部署，覆盖工程全生命周期。

**架构分层：**
```
Trigger → API → Case → Domain ← Infrastructure
```

**目录结构：**
- `domain/` - 领域层：Entity、Aggregate、VO、Domain Service
- `case/` - 编排层：跨域业务编排
- `infrastructure/` - 基础设施层：Repository实现、DAO、Gateway
- `trigger/` - 触发层：Controller、MQ Listener、Job

**核心技能：**
- DDD 项目自动创建脚本
- 实体/聚合根/值对象设计规范
- Repository/Port-Adapter 模式
- 策略模式/责任链模式落地指南
- Docker/Docker-Compose 部署模板

**环境要求：**
- JDK 17+
- Maven 3.8.x

**快速使用：**
```bash
bash scripts/create-ddd-project.sh
```

---

*学习开源项目，记录成长轨迹*
