from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 模拟浏览器的 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# 禁用代理
proxies = {
    'http': None,
    'https': None,
}

# 获取文章列表页的 HTML 内容
url = "https://tophub.today/n/qndg48xeLl"
response = requests.get(url, headers=headers, proxies=proxies)
response.raise_for_status()  # 如果请求失败会抛出异常

# 使用 BeautifulSoup 解析网页内容
soup = BeautifulSoup(response.text, "html.parser")

# 获取前 15 篇文章的标题
rows = soup.find_all('tr')[0:16]  # 跳过表头并获取前 15 行
top_15_titles = []

for row in rows:
    cells = row.find_all('td')
    if len(cells) > 1:  # 如果这一行有文章信息
        rank = cells[0].text.strip().strip('.')
        title_tag = cells[1].find('a')
        title = title_tag.text.strip() if title_tag else ""
        top_15_titles.append(f"{rank}. {title}")

# 获取当前日期和时间
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 将标题生成图片
def create_rank_image(titles, output_path="richang.png"):
    # 图片尺寸（Kindle Paperwhite 4 屏幕分辨率 1072 x 1448）
    image_width = 1072
    image_height = 1448  # 纵向

    background_color = (255, 255, 255)  # 白色背景
    text_color = (0, 0, 0)  # 黑色文字

    # 创建图片对象
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # 设置字体
    try:
        # 尝试使用 Noto Sans CJK 字体
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 60)  # 大字体用于标题
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 48)  # 正文字体
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 32)  # 小字字体用于日期
        extra_small_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 24)  # "已锁屏" 字体
    except IOError:
        print("字体加载失败，使用默认字体")
        title_font = ImageFont.load_default()  # 使用默认字体
        text_font = ImageFont.load_default()  # 使用默认字体
        small_font = ImageFont.load_default()  # 使用默认字体
        extra_small_font = ImageFont.load_default()  # 使用默认字体

    # 标题位置
    x, y = 50, 50

    # 添加 "已锁屏" 文本
    lock_screen_text = "已锁屏"
    draw.text((x, y), lock_screen_text, fill=text_color, font=extra_small_font)
    y += 40  # 调整 y 坐标以避免与其他内容重叠

    # 添加标题到图片（"今日热榜"）
    draw.text((x, y), "今日热榜", fill=text_color, font=title_font)

    # 添加当前日期时间到标题右侧
    date_bbox = draw.textbbox((x, y), current_datetime, font=small_font)  # 获取文本的边界框
    date_width = date_bbox[2] - date_bbox[0]  # 宽度
    date_x = x + title_font.getbbox("今日热榜")[2] + 20  # 计算日期显示的位置，右侧
    draw.text((date_x, y), current_datetime, fill=text_color, font=small_font)

    # 更新 y 坐标，跳过标题和日期部分
    y += 100  # 跳过标题行，增加间隔

    # 添加前 15 个文章标题到图片
    line_height = 80  # 调整行高以适应大字体
    for title in titles:
        draw.text((x, y), title, fill=text_color, font=text_font)
        y += line_height

    # 保存图片
    image.save(output_path)
    print(f"图片已保存为 {output_path}")

# 生成图片并保存到 pic 文件夹
create_rank_image(top_15_titles, output_path="pic/richang.png")
