# WeChat_Cookie
用来维护微信公众号cookie，相对于传统的CookiePool新增了webdriver可以在linux上运行的虚拟屏幕。针对微信公众号登录的特点—每次登录都需要扫码验证，我们将每次获取到的二维码保存到/erweima这个路径下，公众号爬虫还有一个反爬机制是每个cookie的请求不能频繁，所以我们对每个保存到库里的cookie做了计分器，每次获取只拿到使用次数最少的一次。但我们建议每个cookie请求间隔不少于2分钟。