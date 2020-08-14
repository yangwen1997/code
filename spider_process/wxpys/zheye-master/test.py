from zheye import zheye
z = zheye()
positions = z.Recognize(r'E:\code\spider\spider_process\wxpys\zheye-master\a.jpg')

print(positions)


# url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
# input_text: {"img_size":[200,44],"input_points":[[56.5,30],[102.5,25]]}