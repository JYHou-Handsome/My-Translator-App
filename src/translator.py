import hashlib
import time
import random
import requests


LAN_MAP_YOUDAO = {
    "auto": "auto",
    "zh": "zh-CHS",
    "en": "en",
    "ja": "ja",
    "ko": "ko",
    "fr": "fr",
    "de": "de",
    "es": "es",
    "pt": "pt",
    "ru": "ru",
}

YOUDAO_ERROR_CODES = {
    "101": "缺少必填参数",
    "102": "不支持的语言类型",
    "103": "翻译文本过长",
    "108": "应用ID无效",
    "110": "无相关服务的有效实例",
    "111": "开发者账号无效",
    "112": "请求服务无效",
    "113": "查询为空",
    "202": "签名检验失败",
    "203": "访问IP地址不在可访问IP列表",
    "205": "请求的接口与选择的接入方式不一致",
    "206": "翻译服务已到期",
    "207": "翻译结果被系统过滤",
    "301": "辞典查询失败",
    "302": "翻译查询失败",
    "303": "请求超过配额",
    "401": "账户已经被封禁",
    "411": "访问频率受限",
    "412": "长请求过于频繁",
}

MAX_TEXT_LENGTH = 2000


class YoudaoTranslator:
    def __init__(self, app_key: str = "", app_secret: str = ""):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://openapi.youdao.com/api"
        self.timeout = 30

    def translate(self, text: str, source: str = "auto", target: str = "zh") -> tuple[bool, str]:
        if not self.app_key or not self.app_secret:
            return False, "请先在设置中配置有道翻译 API 密钥"

        if not text or not text.strip():
            return False, "翻译文本不能为空"

        text = text.strip()
        if len(text) > MAX_TEXT_LENGTH:
            return False, f"翻译文本过长（最大{MAX_TEXT_LENGTH}字符，当前{len(text)}字符）"

        src = LAN_MAP_YOUDAO.get(source, source)
        tgt = LAN_MAP_YOUDAO.get(target, target)

        try:
            salt = str(random.randint(10000, 99999))
            curtime = str(int(time.time()))
            sign_str = self.app_key + self._truncate(text) + salt + curtime + self.app_secret
            sign = hashlib.sha256(sign_str.encode("utf-8")).hexdigest()

            resp = requests.post(
                self.base_url,
                data={
                    "q": text,
                    "from": src,
                    "to": tgt,
                    "appKey": self.app_key,
                    "salt": salt,
                    "sign": sign,
                    "signType": "v3",
                    "curtime": curtime,
                },
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()

            error_code = data.get("errorCode", "")
            if error_code == "0":
                translation = "".join(data.get("translation", []))
                return True, translation

            error_msg = YOUDAO_ERROR_CODES.get(error_code, "未知错误")
            return False, f"翻译失败 [{error_code}]: {error_msg}"

        except requests.Timeout:
            return False, "翻译请求超时，请检查网络连接"
        except requests.ConnectionError:
            return False, "网络连接失败，请检查网络"
        except requests.RequestException as e:
            return False, f"翻译请求失败: {e}"
        except Exception as e:
            return False, f"翻译异常: {e}"

    def test_connection(self) -> tuple[bool, str]:
        if not self.app_key or not self.app_secret:
            return False, "请先填写 App Key 和 App Secret"
        return self.translate("hello", source="en", target="zh")

    @staticmethod
    def _truncate(q: str) -> str:
        if q is None:
            return ""
        size = len(q)
        return q if size <= 20 else q[:10] + str(size) + q[-10:]
