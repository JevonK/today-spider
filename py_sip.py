import pjsua as pj

# 初始化PJSUA库
lib = pj.Lib()
lib.init(log_cfg=pj.LogConfig(level=3, console_level=5))

# 创建一个账户配置
acc_cfg = pj.AccountConfig()
acc_cfg.id_uri = "sip:your_username@sipserver.com"
acc_cfg.username = "your_username"
acc_cfg.password = "your_password"
acc_cfg.proxy = ["sip:sipserver.com"]

# 创建拨号配置
dial_cfg = pj.SipTxOption()
dial_cfg.set_no_srv()

# 创建一个UA配置
ua_cfg = pj.UaConfig()
ua_cfg.sip_port = 5060
ua_cfg.allow_concurrent_registration = True

# 创建一个UA
ua = lib.create_ua(ua_cfg)

# 启动PJSUA库
lib.start()

# 创建并添加账户
acc = ua.create_acc(acc_cfg)

# 注册到SIP服务器
acc.set_registration(True)

# 保持程序运行以处理SIP事件
try:
    while True:
        lib.handle_events(100)
except KeyboardInterrupt:
    pass

# 停止PJSUA库
lib.destroy()
