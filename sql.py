import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


if __name__ == '__main__':
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig(sandbox_debug = True)
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016101100658978'
    alipay_client_config.app_private_key ='MIIEpAIBAAKCAQEAwop/Z7k+32Hs8E7nFgYdvr8ScKatcP1i8YOl/BCyCumNjQeyvmfYr71Bd9PMwHC78ACVAz4R0JFmY+/uAfALba7vPrxBM+YJZH4INoKSOrADBEzZbRD0O7YbG7oqgDmg1Tq/dMxYBPq4eRkXBOZ6SvNECxaHwlSgj88iyM0H6OQmbTmu6VlBjHHpGf8HjKgSNk55Y9q0dhHHyvdttvhsoeMpXJ61X0Jjpi6FN/OTb7vGA4Sa6eA1TU+lpOWTR97j98pcAGzSfV6it+Aty7/Ogebsx9+FhkSHrcoKG7WG3OutUTBtsqSvqvUzvc9YjtlreqM6hRBPTevsjFCQYsYJ4wIDAQABAoIBAADFk+PRdFJmjQ4XAguwUoXjNCuGPcHo/2992ja5yjsI2irpEOh4eP+ZfJ0BFhrdV6GIHw84O9HcAc/7r7IKRcFVpFVXYdrW2sqvRVESC4p4EEsAEwy/uHhULJ9bibeggubVqNTJyr+aTwkL9G9siqepd2ej2z4GH+zyIW0ygwmFfGwuCtpyUrkkRd0MSdm+7yOiV9I4+xoD0cY4785HxuxW8Udk0FQVBdfZwtCs0Xc2DkHBh6ANtyMnZh2vPIWmk9NoeVQmagr6Ue7Rt+7SEaK/pF5Zl0O3t49wCDoeEMD8mNcZ9EPZTAR1cV0M9bHB9auayTLxIuV+Pc6H0G6ViMECgYEA4sIbl+eZs1vD2T1B58hrfwaPAttcBSzha7DASJpsI3zYVrRrjxL0IXkmP4H3WGU6W+/OKGN98zjc3KbjrvPppmW+qAJPykWUO8uyQxtYtEhXdylgCuN6cpNJUYeQZ+tmXAx1OukHCP47PPN9cs7ysLeO/rAJpCxJVliIKObRGfkCgYEA26DQRclzkqfSfNaudGjhHnE+B7MHOh7tnQu7DkBnp42LMtF2YH4s2up33OmL2IzyLy998u9m/kUmtDuw8zVWP43P5pQHLjtfKrlSl3Na1ndRUDYrLoRI0vtle2KgUxOjBrwSd+eV5+Zdlc/oy3F5BA1152xToKpcYj4AkHIk2bsCgYB0qvg1fOS4wnMOt5TMI3MjZQV5q9E5nHDSzprv//u5eod4fNWGRHM1Mbb7H+xaH6MaIFTKtP3dgRkpsfgdUMObaGfi22WgJZJx/YjXPB+0ii/uUGxozcd3Yc5sUzp6LUR6AbLjP3fuKZfi8UhPJKj7QUYiRgJ/5IVLFrvfh3p4SQKBgQDOzZgPfmdS+q9aWZOfjXocfikYet0dPy4iqH8UJlT0EnW1/kHnDigSYqFG5KqH1//bqm6AKCjk2Bxfra0q9VgnM9NFnLE+OS2dPy+j6DzqoSNx0e/LN0iTUaD3E6E/WMgzeTgyq2AeIm6QuFrN5iU7SalxpjEAoimnYBaL7M8CLQKBgQDJy1DlGoqBZ4Ic8nng8HGZs593zuA4J2EK+r39q5ZgqwbNtYWDoCxyZqStcQm7784ENcrYgn8C4pbRK2YFiKoq30JiUybnvJHd8L8+40KgD3Y/SY/8D208wUwGppJFvLdotEIKD/rqYaos/gS9RLJkycQoKgieocDyCjo9+hv9Qg=='
    alipay_client_config.alipay_public_key = ' MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwop/Z7k+32Hs8E7nFgYdvr8ScKatcP1i8YOl/BCyCumNjQeyvmfYr71Bd9PMwHC78ACVAz4R0JFmY+/uAfALba7vPrxBM+YJZH4INoKSOrADBEzZbRD0O7YbG7oqgDmg1Tq/dMxYBPq4eRkXBOZ6SvNECxaHwlSgj88iyM0H6OQmbTmu6VlBjHHpGf8HjKgSNk55Y9q0dhHHyvdttvhsoeMpXJ61X0Jjpi6FN/OTb7vGA4Sa6eA1TU+lpOWTR97j98pcAGzSfV6it+Aty7/Ogebsx9+FhkSHrcoKG7WG3OutUTBtsqSvqvUzvc9YjtlreqM6hRBPTevsjFCQYsYJ4wIDAQAB    '
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
    model = AlipayTradePagePayModel()
    import time
    model.out_trade_no = "pay" + str(time.time())
    model.total_amount = 100
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    request = AlipayTradePagePayRequest(biz_model=model)
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


 
 
 
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 50
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088302300165604"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    sub_merchant = SubMerchant()
    sub_merchant.merchant_id = "2088301300153242"
    model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)


    """
    构造唤起支付宝客户端支付时传递的请求串示例：alipay.trade.app.pay
    """
    model = AlipayTradeAppPayModel()
    model.timeout_express = "90m"
    model.total_amount = "9.00"
    model.seller_id = "2088301194649043"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = "Iphone6 16G"
    model.subject = "iphone"
    model.out_trade_no = "201800000001201"
    request = AlipayTradeAppPayRequest(biz_model=model)
    response = client.sdk_execute(request)
    print("alipay.trade.app.pay response:" + response)
    
    

'MIIEpAIBAAKCAQEAwop/Z7k+32Hs8E7nFgYdvr8ScKatcP1i8YOl/BCyCumNjQeyvmfYr71Bd9PMwHC78ACVAz4R0JFmY+/uAfALba7vPrxBM+YJZH4INoKSOrADBEzZbRD0O7YbG7oqgDmg1Tq/dMxYBPq4eRkXBOZ6SvNECxaHwlSgj88iyM0H6OQmbTmu6VlBjHHpGf8HjKgSNk55Y9q0dhHHyvdttvhsoeMpXJ61X0Jjpi6FN/OTb7vGA4Sa6eA1TU+lpOWTR97j98pcAGzSfV6it+Aty7/Ogebsx9+FhkSHrcoKG7WG3OutUTBtsqSvqvUzvc9YjtlreqM6hRBPTevsjFCQYsYJ4wIDAQABAoIBAADFk+PRdFJmjQ4XAguwUoXjNCuGPcHo/2992ja5yjsI2irpEOh4eP+ZfJ0BFhrdV6GIHw84O9HcAc/7r7IKRcFVpFVXYdrW2sqvRVESC4p4EEsAEwy/uHhULJ9bibeggubVqNTJyr+aTwkL9G9siqepd2ej2z4GH+zyIW0ygwmFfGwuCtpyUrkkRd0MSdm+7yOiV9I4+xoD0cY4785HxuxW8Udk0FQVBdfZwtCs0Xc2DkHBh6ANtyMnZh2vPIWmk9NoeVQmagr6Ue7Rt+7SEaK/pF5Zl0O3t49wCDoeEMD8mNcZ9EPZTAR1cV0M9bHB9auayTLxIuV+Pc6H0G6ViMECgYEA4sIbl+eZs1vD2T1B58hrfwaPAttcBSzha7DASJpsI3zYVrRrjxL0IXkmP4H3WGU6W+/OKGN98zjc3KbjrvPppmW+qAJPykWUO8uyQxtYtEhXdylgCuN6cpNJUYeQZ+tmXAx1OukHCP47PPN9cs7ysLeO/rAJpCxJVliIKObRGfkCgYEA26DQRclzkqfSfNaudGjhHnE+B7MHOh7tnQu7DkBnp42LMtF2YH4s2up33OmL2IzyLy998u9m/kUmtDuw8zVWP43P5pQHLjtfKrlSl3Na1ndRUDYrLoRI0vtle2KgUxOjBrwSd+eV5+Zdlc/oy3F5BA1152xToKpcYj4AkHIk2bsCgYB0qvg1fOS4wnMOt5TMI3MjZQV5q9E5nHDSzprv//u5eod4fNWGRHM1Mbb7H+xaH6MaIFTKtP3dgRkpsfgdUMObaGfi22WgJZJx/YjXPB+0ii/uUGxozcd3Yc5sUzp6LUR6AbLjP3fuKZfi8UhPJKj7QUYiRgJ/5IVLFrvfh3p4SQKBgQDOzZgPfmdS+q9aWZOfjXocfikYet0dPy4iqH8UJlT0EnW1/kHnDigSYqFG5KqH1//bqm6AKCjk2Bxfra0q9VgnM9NFnLE+OS2dPy+j6DzqoSNx0e/LN0iTUaD3E6E/WMgzeTgyq2AeIm6QuFrN5iU7SalxpjEAoimnYBaL7M8CLQKBgQDJy1DlGoqBZ4Ic8nng8HGZs593zuA4J2EK+r39q5ZgqwbNtYWDoCxyZqStcQm7784ENcrYgn8C4pbRK2YFiKoq30JiUybnvJHd8L8+40KgD3Y/SY/8D208wUwGppJFvLdotEIKD/rqYaos/gS9RLJkycQoKgieocDyCjo9+hv9Qg=='

' MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwop/Z7k+32Hs8E7nFgYdvr8ScKatcP1i8YOl/BCyCumNjQeyvmfYr71Bd9PMwHC78ACVAz4R0JFmY+/uAfALba7vPrxBM+YJZH4INoKSOrADBEzZbRD0O7YbG7oqgDmg1Tq/dMxYBPq4eRkXBOZ6SvNECxaHwlSgj88iyM0H6OQmbTmu6VlBjHHpGf8HjKgSNk55Y9q0dhHHyvdttvhsoeMpXJ61X0Jjpi6FN/OTb7vGA4Sa6eA1TU+lpOWTR97j98pcAGzSfV6it+Aty7/Ogebsx9+FhkSHrcoKG7WG3OutUTBtsqSvqvUzvc9YjtlreqM6hRBPTevsjFCQYsYJ4wIDAQAB    '