# npu-auto-yqtb
使用 GitHub Acition 进行西北工业大学自动疫情填报
参考[nwpu-auto-yqtb](https://github.com/2ndelement/nwpu-auto-yqtb)

## 定时

> 更改 [workflow yaml](.github/workflows/main.yml) 中 cron 项即可填报更改时间
>
> ``` yaml
> schedule:
>    - cron: '0 0,16 * * *' 
>       # 此时间为 'UTF时间', +8h 后为 '北京时间'
>       # 每天00:00, 16:00 执行
> ```
> 由于定时任务由Github调度, 实际执行时间可能延迟1-2h不定
> 更多可见 [github docs onschedule](https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions#onschedule)

- **❗重要❗** 最后点击 `Actions` => 选择工作流 `自动疫情填报`  => `Enable workflow`

- 推荐先手动运行一遍工作流查看是否能正确执行

## 启用消息推送（选用，不需要推送功能可以跳过）

### pushplus微信推送功能

用 [pushplus(推送加)](https://www.pushplus.plus/) 通过公众号推送结果:

- 登录pushplus官网后, 选择一对一推送页面, 按照网站的说明获取你的`token`.
 
- 复制该token，填入config.json


## TODO
将密码、token等信息使用`Secrets`保存

## 声明
- 打卡可能会失败, 建议开启消息推送.
- 本项目仅提供参考, 因使用本项目导致的一切不良后果请使用者自行承担