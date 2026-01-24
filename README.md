# SeleniumBase Test Case Provider

#### 介绍
本项目提供自动化测试用例，通过 GitHub Actions 运行脚本，将测试用例写入数据库，为自动化测试平台提供测试用例数据支持。

项目基于 SeleniumBase 测试框架，使用 pytest 进行测试管理，并为每个测试用例标记了归属人、优先级和用例说明，方便测试平台识别和管理。

#### 测试用例标记
每个测试用例包含以下标记信息：
- `@pytest.mark.owner('caijinwei')` - 测试用例归属人
- `@pytest.mark.priority('P0/P1/P2')` - 测试用例优先级（P0: 关键测试，P1: 标准测试，P2: 辅助/边缘测试）
- `@pytest.mark.description('...')` - 测试用例说明

#### 软件架构
- 基于 SeleniumBase 测试框架
- 使用 pytest 进行测试管理和标记
- 通过 GitHub Actions 自动化流程
- 支持 CI/CD 集成
- 测试用例数据化并入库到测试平台


#### 安装教程

1.  安装依赖：`pip install -r requirements.txt`
2.  配置数据库连接信息（根据实际环境配置）
3.  运行测试：`pytest examples/` 或使用 `python examples/test_xxx.py` 单独运行

#### 使用说明

1.  **开发测试用例**：在 `examples/` 目录下创建或修改测试文件，确保每个测试方法包含 owner、priority、description 标记
2.  **本地验证**：使用 pytest 运行测试验证功能是否正常
3.  **提交代码**：提交代码后会自动触发 GitHub Actions
4.  **数据同步**：GitHub Action 脚本会自动解析测试用例并写入数据库
5.  **平台集成**：自动化测试平台从数据库读取测试用例数据进行执行

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 目录结构

```
├── examples/           # 测试用例目录（50+ 测试文件）
├── scripts/           # GitHub Actions 相关脚本
├── reports/           # 测试报告目录
├── requirements.txt   # 项目依赖
├── pytest.ini        # pytest 配置文件
├── environment.yml    # Conda 环境配置
├── Dockerfile         # Docker 镜像构建文件
├── Jenkinsfile        # Jenkins CI 配置
└── README.md          # 项目说明文档
```

#### 测试用例统计

- 测试用例数量：50+ 个
- 覆盖场景：登录测试、表单操作、拖拽、截图、多因素认证、数据驱动测试等
- 优先级分布：P0（关键测试）、P1（标准测试）、P2（辅助测试）

#### CI/CD 流程

1. 代码提交到仓库
2. 触发 GitHub Actions
3. 解析测试用例标记信息
4. 将测试用例数据写入数据库
5. 自动化测试平台读取并执行测试用例

#### 特性

- 支持多平台运行（Windows/Linux/macOS）
- 支持多种浏览器（Chrome、Firefox、Edge、Safari）
- 支持无头模式和可视化模式
- 支持测试截图和视频录制
- 支持数据驱动测试（pytest parametrize）
- 支持测试重试和失败处理
