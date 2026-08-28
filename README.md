# 一个追求高命中率、轻量的广告规则集
## 介绍  
- 只支持Mihomo
- 只有mrs格式
- 只适用于移动端  

## 下载  
| 规则名         | 作用   | 链接                                                                                                      |
| ----------- | ---- | ------------------------------------------------------------------------------------------------------- |
| adblock.mrs | 拦截广告 | [Github](https://raw.githubusercontent.com/meazenlvy/adblock-ruleset-for-mihomo/main/rules/adblock.mrs) |

## 使用方法  
1. 将下列代码复制到配置文件的rule-provider中
   ```
  adblock-domain:
    type: http
    interval: 86400
    behavior: domain
    format: mrs
    url: "https://raw.githubusercontent.com/meazenlvy/adblock-ruleset-for-mihomo/main/rules/adblock.mrs"
   ```
2. 启用规则
    - 在DNS配置中启用：
      ```
        nameserver-policy:
          "rule-set:adblock-domain":
          - "rcode://name_error"
      ```
    - 在分流规则中启用
      ```
        - RULE-SET,adblock-domain,BLOCK
      ```

## 待办清单  
- [x] 域名树
- [x] 进一步去重
- [ ] 增加隐私规则
- [ ] 增加安全规则
- [ ] 增加放行规则
- [ ] 分离配置文件
