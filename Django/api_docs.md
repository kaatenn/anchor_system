# API DOCs

## /api/register

- 用来注册一个账户
- method: POST
- param: type
用户所选择的注册类型
- param: account
用户所填写的账号
- param: password
用户所填写的密码
- return: 
将会有两种返回，返回错误码 400 表示账户已存在，返回 'success' 表示注册成功
