import datetime
import os
import random
import string
import time

import pypinyin
import qrcode
from PIL import Image, ImageDraw, ImageFont

black = "#000000"


def generate_ticket_template():
    im = Image.open("./images/background_blue.png")
    im = im.convert("RGBA")

    font = ImageFont.truetype("./fonts/STHeiti.ttf", 24)

    draw = ImageDraw.Draw(im)
    # 生成票号
    ticket_no = ''.join(random.sample(string.ascii_letters + string.digits, 9)).upper();
    draw.text((20, 10), ticket_no, font=font, fill="#ff0000")

    # 两个"站"字
    draw.text((200, 60), "站", font=font, fill=black)
    draw.text((550, 60), "站", font=font, fill=black)

    # 箭头
    draw.text((300, 100), "————>", font=font, fill=black)
    # 网
    draw.text((350, 160), "网", font=font, fill=black)
    # 二等座
    draw.text((450, 160), "二等座", font=font, fill=black)

    simsung_24 = ImageFont.truetype(os.path.relpath("./fonts/simsun.ttf"), 24);
    # 限乘当日当次车
    draw.text((80, 200), "限乘当日当次车", font=simsung_24, fill=black)

    # 画虚线框
    draw.text((120, 290), "---------------------------", font=simsung_24, fill=black)
    draw.text((120, 335), "---------------------------", font=simsung_24, fill=black)
    draw.text((110, 300), "¦                           ¦", font=simsung_24, fill=black)
    draw.text((110, 325), "¦                           ¦", font=simsung_24, fill=black)
    # 买票请到12306 发货请到95306
    simsung_18 = ImageFont.truetype(os.path.relpath("./fonts/simsun.ttf"), 18);
    draw.text((150, 305), "买票请到12306\t发货请到95306", font=simsung_18, fill=black)
    # 中国铁路祝您旅途愉快
    draw.text((180, 325), "中国铁路祝您旅途愉快", font=simsung_18, fill=black)
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

    qr_img = qr.make_image(fill_color="black")
    qr_img = qr_img.convert("RGBA")
    image_data = qr_img.getdata()
    new_data = list()
    for item in image_data:
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    qr_img.putdata(new_data)
    im.paste(qr_img, (510, 265))
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


# 绘制车站
def draw_station_name(draw, f, t):
    font = ImageFont.truetype(os.path.relpath("./fonts/simhei.ttf"), 32)
    f_pinyin = convert_to_pinyin(f)
    t_pinyin = convert_to_pinyin(t)
    if len(f) == 2:
        f = f[0] + "  " + f[1]
    if len(t) == 2:
        t = t[0] + "  " + t[1]
    draw.text((100, 50), f, font=font, fill=black)
    draw.text((450, 50), t, font=font, fill=black)
    pinyin_font = ImageFont.truetype(os.path.relpath("./fonts/FangSong_GB2312.ttf"), 24)
    draw.text((100, 85), f_pinyin, font=pinyin_font, fill=black)
    draw.text((450, 85), t_pinyin, font=pinyin_font, fill=black)


def draw_train_no(draw, no):
    font = ImageFont.truetype(os.path.relpath("./fonts/STSongti.ttf"), 32)
    offset = ((abs(len(no) - 5)) * 5)
    draw.text((300 + offset / 2, 70), no, font=font, fill=black)
    # 次
    ci_font = ImageFont.truetype(os.path.relpath("./fonts/simsun.ttf"), 24)
    x_axis = 300 + offset / 2 + len(no) * 10
    draw.text((x_axis + 30, 80), "次", font=ci_font, fill=black)


# 生成随机时间
def random_date():
    start = time.mktime((2015, 1, 1, 0, 0, 0, 0, 0, 0))
    end = time.mktime((2018, 12, 31, 23, 59, 59, 59, 00, 00))
    return datetime.datetime.fromtimestamp(random.randint(start, end))


# 绘制时间
def draw_datetime(draw, datetime=datetime.datetime.now()):
    num_font = ImageFont.truetype(os.path.relpath("./fonts/TechnicBold.ttf"), 32, encoding="armn")
    # 年 月 日 开
    text_font = ImageFont.truetype(os.path.relpath("./fonts/STSongti.ttf"), 18)
    draw.text((120, 130), "年\t\t月\t\t日\t\t\t\t\t开", font=text_font, fill=black)
    # 时间
    draw.text((60, 125), str(datetime.year), font=num_font, fill=black)
    draw.text((145, 125), str(datetime.month) if datetime.month > 9 else "0" + str(datetime.month), font=num_font,
              fill=black)
    draw.text((195, 125), str(datetime.day) if datetime.day > 9 else "0" + str(datetime.day), font=num_font,
              fill=black)
    time_clock = (str(datetime.hour) if datetime.hour > 9 else "0" + str(datetime.hour)) + ":" + (
        str(datetime.minute) if datetime.minute > 9 else "0" + str(datetime.minute))
    draw.text((250, 125), time_clock, font=num_font, fill=black)


def draw_sit_no(draw):
    num_font = ImageFont.truetype(os.path.relpath("./fonts/TechnicBold.ttf"), 30, encoding="armn")
    text_font = ImageFont.truetype(os.path.relpath("./fonts/STSongti.ttf"), 18)
    # 车 号
    draw.text((475, 130), "车\t\t号", font=text_font, fill=black)
    no_len = random.randint(1, 2)
    carriage_no = int("".join(random.sample(string.digits if no_len > 1 else string.digits.replace("0", ""), no_len)))
    draw.text((440, 125), str(carriage_no) if carriage_no > 9 else "0" + str(carriage_no), font=num_font, fill=black)
    sit_no_num = int("".join(random.sample(string.digits, random.randint(1, 2))))
    sit_no = (str(sit_no_num) if sit_no_num > 9 else "0" + str(sit_no_num))
    draw.text((490, 125), sit_no, font=num_font, fill=black)

    # 座位号单独画
    sit_no_alpha = random.sample(("A", "B", "C", "D", "E", "F"), 1)[0]
    alpha_font = ImageFont.truetype(os.path.relpath("./fonts/TechnicBold.ttf"), 20, encoding="armn")
    draw.text((520, 130), sit_no_alpha, font=alpha_font, fill=black)


def random_ticket_price():
    return random.randint(10, 1100) + (random.sample((0, 5), 1)[0] / 10)


def draw_ticket_price(draw, price=random_ticket_price()):
    text_font = ImageFont.truetype(os.path.relpath("./fonts/STSongti.ttf"), 18)
    money_symbol_font = ImageFont.truetype(os.path.relpath("./fonts/STSongti.ttf"), 24)
    num_font = ImageFont.truetype(os.path.relpath("./fonts/TechnicBold.ttf"), 32, encoding="armn")
    # ¥ 元
    draw.text((80, 160), "¥", font=money_symbol_font, fill=black)
    str_price = str(price)
    draw.text((95, 160), str_price, font=num_font, fill=black)
    draw.text((95 + (len(str_price) * 15), 165), "元", font=text_font, fill=black)


def random_id_no():
    id_no = ""
    for i in range(18):
        if 9 < i < 14:
            id_no += "*"
        else:
            id_no += random.sample(string.digits if i != 0 else string.digits.replace("0", ""), 1)[0]
    return id_no


def random_chinese():
    name = ""
    name_len = random.randint(2, 4)
    for i in range(name_len):
        name += str(chr(random.randint(0x4e00, 0x9fbf)))
    return name


def draw_id_no(draw, id_no=random_id_no(), name=random_chinese()):
    num_font = ImageFont.truetype(os.path.relpath("./fonts/TechnicBold.ttf"), 28, encoding="armn")
    name_font = ImageFont.truetype(os.path.relpath("./fonts/STSongti.ttf"), 24)
    # 身份证号
    draw.text((80, 270), id_no, font=num_font, fill=black)
    # 计算号码中1的数量计算名字的偏移
    num_one_count = 0
    for i in range(len(id_no)):
        if id_no[i] == 1:
            num_one_count += 1
    # 姓名
    draw.text((num_one_count * 5 / 2 + 360, 270), name, font=name_font, fill=black)


if __name__ == "__main__":
    stations = load_stations_from_file()
    img = generate_ticket_template()
    draw = ImageDraw.Draw(img)
    draw_station_name(draw, stations[random.randint(0, len(stations))], stations[random.randint(0, len(stations))])
    draw_train_no(draw, random_train_no())
    draw_datetime(draw, random_date())
    draw_sit_no(draw)
    draw_ticket_price(draw)
    draw_id_no(draw)
    img.show()
