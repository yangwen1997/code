import asyncio
import requests
from pyppeteer.launcher import launch


async def spider(url):
    # 启动pyppeteer
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], 'dumpio': True})
    # 启动新的浏览器页面
    page = await browser.newPage()
    # 添加User
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36')
    # 设置浏览器宽高
    await page.setViewport(viewport={"width": 1366, "height": 938})
    # 访问页面
    await page.goto(url)
    text = await page.content()
    # print(text)
    # await page_evaluate(page)

    cook = await get_cookie(page)
    print(cook)
    await page.close()


async def page_close(browser):
    # 关闭
    for _page in await browser.pages():
        await _page.close()
        await browser.close()


# 获取登录后cookie
async def get_cookie(page):
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies




if __name__ == '__main__':
    # url = 'http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=d508e36c722e8c03a3dceaed38ead56e&s8=02'  # 加入事件循环中，才能被调用
    url = 'http://jg.hbcic.net.cn/web/RyManage/RySearch.aspx?rylx=snry'  # 加入事件循环中，才能被调用
    loop = asyncio.get_event_loop()
    spider = spider(url)
    loop.run_until_complete(spider)
