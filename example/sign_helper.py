from playwright.sync_api import sync_playwright
import time


class SignHelper:
    def __init__(self, cookie_value=None, stealth_js_path="tests/stealth.min.js"):
        """
        初始化签名助手
        :param cookie_value: a1 cookie的值，如果为None则会自动从浏览器获取
        :param stealth_js_path: stealth.js文件路径
        """
        self.cookie_value = cookie_value
        self.stealth_js_path = stealth_js_path
        self.playwright = None
        self.browser_context = None
        self.context_page = None
        self._setup_browser()

    def _setup_browser(self):
        """初始化浏览器环境"""
        self.playwright = sync_playwright().start()
        chromium = self.playwright.chromium
        browser = chromium.launch(headless=True)
        self.browser_context = browser.new_context()
        self.browser_context.add_init_script(path=self.stealth_js_path)
        self.context_page = self.browser_context.new_page()
        
        # 访问小红书首页
        self.context_page.goto("https://www.xiaohongshu.com")
        time.sleep(2)
        
        if self.cookie_value is None:
            # 如果没有提供cookie，从浏览器获取
            self.context_page.reload()
            time.sleep(1)
            cookies = self.browser_context.cookies()
            for cookie in cookies:
                if cookie["name"] == "a1":
                    self.cookie_value = cookie["value"]
                    print(f"从浏览器获取到 a1 值: {self.cookie_value}")
                    break
            if not self.cookie_value:
                raise Exception("未能从浏览器获取到 a1 cookie")
        else:
            # 如果提供了cookie，直接设置
            self.browser_context.add_cookies([{
                "name": "a1",
                "value": self.cookie_value,
                "domain": ".xiaohongshu.com",
                "path": "/"
            }])
            self.context_page.reload()
            time.sleep(1)

    def sign(self, uri, data):
        """
        生成签名
        :param uri: 请求路径
        :param data: 请求数据
        :return: 包含x-s和x-t的字典
        """
        encrypt_params = self.context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
        return {
            "x-s": encrypt_params["X-s"],
            "x-t": str(encrypt_params["X-t"])
        }

    def get_cookie_value(self):
        """
        获取当前使用的cookie值
        :return: a1 cookie的值
        """
        return self.cookie_value

    def close(self):
        """关闭浏览器和playwright"""
        if self.context_page:
            self.context_page.close()
        if self.browser_context:
            self.browser_context.close()
        if self.playwright:
            self.playwright.stop() 