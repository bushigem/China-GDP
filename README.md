中国省份 GDP 可视化应用
这是一个基于 Streamlit 构建的交互式数据可视化应用，展示中国各省份近十年的 GDP 数据。用户可以选择不同的年份和省份，并通过多种图表类型（柱状图、热力图、气泡图等）进行可视化分析。

功能介绍
多种图表可视化：支持柱状图、热力图、散点图和气泡图。
动态数据筛选：用户可以按年份和省份筛选数据，实时更新图表。
统计分析：计算并展示平均 GDP、中位数 GDP 以及标准差。
PDF 报告导出：支持导出当前筛选数据的 PDF 报告。
用户反馈：包含简单的用户反馈表单。
背景美化：应用使用了自定义背景图，界面美观。
目录结构
bash
复制代码
streamlit/
├── app.py                        # 主应用文件
├── scripts/
│   └── china_gdp_all_provinces_10_years.csv  # 数据文件
├── utils.py                      # 工具函数文件（如果有）
├── requirements.txt              # 依赖库列表
├── README.md                     # 项目说明文件
└── .gitignore                    # Git 忽略文件
环境配置与安装
1. 克隆项目
使用 Git 克隆项目到本地：

bash
复制代码
git clone https://github.com/your_username/your_repository.git
cd your_repository
2. 创建虚拟环境
建议使用虚拟环境来安装依赖，避免影响系统环境：

bash
复制代码
python -m venv .venv
source .venv/bin/activate   # Windows 用户使用 .venv\Scripts\activate
3. 安装依赖库
使用 requirements.txt 文件安装项目所需依赖库：

bash
复制代码
pip install -r requirements.txt
运行应用
在终端中使用以下命令启动 Streamlit 应用：

bash
复制代码
streamlit run app.py
启动后，你可以在浏览器中访问应用，默认地址为 http://localhost:8501。

数据文件
应用使用的 GDP 数据存储在 scripts/china_gdp_all_provinces_10_years.csv 文件中。数据包含以下列：

Province：省份名称
Year：年份（2013-2022）
GDP：GDP 值（亿元）
Latitude：纬度
Longitude：经度
常见问题
无法找到 CSV 文件

请确保 china_gdp_all_provinces_10_years.csv 文件在 scripts/ 文件夹下。
安装依赖时出错

请检查 Python 环境是否正确配置，并确保使用虚拟环境。
网页无法访问

检查终端中是否显示应用启动成功的提示，并确保没有被防火墙或安全软件拦截。
如何贡献
欢迎任何形式的贡献！如果你发现了 bug 或有新的功能建议，请提交 Issue 或 Pull Request。

贡献步骤：
Fork 仓库
创建新的分支 (git checkout -b feature/your-feature)
提交更改 (git commit -m 'Add some feature')
推送到分支 (git push origin feature/your-feature)
提交 Pull Request
许可证
本项目使用 MIT 许可证。

联系方式
如果你有任何问题或建议，请联系我：

GitHub: bushigem
Email: 3391086181@qq.com
