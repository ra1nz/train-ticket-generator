from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import string
import qrcode
import pypinyin
import re

black = "#000000"


def generate_ticket_template():
    im = Image.open("./images/background_blue.jpg")

    font = ImageFont.truetype("./fonts/STHeiti.ttf", 24)

    draw = ImageDraw.Draw(im)
    # 生成票号
    ticket_no = ''.join(random.sample(string.ascii_letters + string.digits, 9)).upper();
    draw.text((20, 10), ticket_no, font=font, fill="#ff0000")

    # 两个"站"字
    draw.text((200, 60), "站", font=font, fill=black)
    draw.text((550, 60), "站", font=font, fill=black)

    # 车次
    draw.text((335, 80), "G123", font=font, fill=black)
    # 箭头
    draw.text((325, 100), "————>", font=font, fill=black)

    # 年 月 日 开
    draw.text((120, 130), "年\t\t\t\t月\t\t\t\t日\t\t\t\t\t\t\t开", font=font, fill=black)
    # 车 号
    draw.text((500, 130), "车\t\t\t\t号", font=font, fill=black)
    # ¥ 元
    draw.text((80, 180), "¥\t\t\t\t\t\t元", font=font, fill=black)
    # 网
    draw.text((350, 180), "网", font=font, fill=black)
    # 二等座
    draw.text((500, 180), "二等座", font=font, fill=black)

    # 限乘当日当次车
    draw.text((80, 230), "限乘当日当次车", font=font, fill=black)

    # 身份证号
    draw.text((80, 290), "000000000000000000", font=font, fill=black)
    # 姓名
    draw.text((330, 290), "姓名", font=font, fill=black)
    # 画虚线框
    draw.text((100, 310), "---------------------------", font=font, fill=black)
    draw.text((100, 350), "---------------------------", font=font, fill=black)
    draw.text((90, 320), "¦                                  ¦", font=font, fill=black)
    draw.text((90, 340), "¦                                  ¦", font=font, fill=black)
    # 下方的票号
    ticket_serial_no = []
    for i in range(14):
        ticket_serial_no.extend(random.sample(string.digits, 1))
    ticket_serial_no.extend(random.sample(string.ascii_uppercase, 1))
    ticket_serial_no.extend(random.sample(string.digits, 6))
    draw.text((80, 380), "".join(ticket_serial_no), font=font, fill=black)
    # 售票站
    draw.text((380, 380), "北京西售", font=font, fill=black)

    # 二维码部分
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=0)
    qr.add_data("test")
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    im.paste(qr_img, (550, 270))
    return im


# 从文件读取车站
def load_stations_from_file():
    f = open("./files/stations.txt", encoding="utf-8")
    line = f.readline()
    result = []
    while line:
        result.append(line.replace("\n", ""))
        line = f.readline()
    return result


# 转换为拼音并且首字母大写
def convert_to_pinyin(text):
    pinyin = pypinyin.lazy_pinyin(text)
    pinyin[0] = pinyin[0].capitalize()
    return "".join(pinyin)


def random_train_no():
    rtn = list()
    rtn.append(random.sample(["GC", "D", "Z", "T", "K"], 1)[0])
    for i in range(random.randint(2, 4)):
        rtn.append(random.sample(string.digits.replace("0", "") if i == 0 else string.digits, 1)[0])
    return "".join(rtn)


def draw_station_name(draw, f, t):
    font = ImageFont.truetype("./fonts/simhei.ttf", 32)
    f_pinyin = convert_to_pinyin(f)
    t_pinyin = convert_to_pinyin(t)
    if len(f) == 2:
        f = f[0] + "  " + f[1]
    if len(t) == 2:
        t = t[0] + "  " + t[1]
    draw.text((100, 50), f, font=font, fill=black)
    draw.text((450, 50), t, font=font, fill=black)
    pinyin_font = ImageFont.truetype("./fonts/仿宋_GB2312.ttf", 24)
    draw.text((100, 85), f_pinyin, font=pinyin_font, fill=black)
    draw.text((450, 85), t_pinyin, font=pinyin_font, fill=black)


stations = load_stations_from_file()

img = generate_ticket_template()
draw = ImageDraw.Draw(img)
draw_station_name(draw, stations[random.randint(0, len(stations))], stations[random.randint(0, len(stations))])
img.show()
