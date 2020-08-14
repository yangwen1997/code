import asyncio
from pyppeteer import launch



class GX(object):
    def __init__(self):
        pass

    async def init(self):
        # 启动pyppeteer
        browser = await launch({'headless': False, 'args': ['--no-sandbox'], 'dumpio': True})
        # 启动新的浏览器页面
        page = await browser.newPage()
        # 添加User
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36')
        # 设置浏览器宽高
        await page.setViewport(viewport={"width": 1866, "height": 938})
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                         '{ webdriver:{ get: () => false } }) }')
        return page

    async def run(self):
        page = await self.init()

        await page.goto(url="http://dn4.gxzjt.gov.cn:1141/WebInfo/Person/Person.aspx")
        text = await page.content()
        print(text)

async def spider():
    st = GX()
    await st.run()

loop = asyncio.get_event_loop()
loop.run_until_complete(spider())