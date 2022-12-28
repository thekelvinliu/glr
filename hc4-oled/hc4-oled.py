# based on: https://codeberg.org/wh0ami/hc4-oled/

from os import path, getloadavg
from psutil import boot_time, cpu_count
from time import sleep, time

from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

DELAY = 3

DEVICE = ssd1306(i2c(port=0, address=0x3C), rotate=2)

FONT = ImageFont.truetype(
    path.abspath(path.join(path.dirname(__file__), "fonts", "DejaVuSansMono.ttf")), 16
)


def delay():
    sleep(DELAY)


def draw(*lines):
    data = "\n".join(map(str, lines))

    # uncomment for debug
    # print("\n".join(["", string, ""]))

    with canvas(DEVICE) as draw:
        draw.text((0, 0), data, fill="white", font=FONT)


def cur_cpu_freq():
    count = cpu_count()
    total = 0
    for i in range(count):
        with open(f"/sys/devices/system/cpu/cpu{i}/cpufreq/cpuinfo_cur_freq") as fin:
            total += int(fin.read())
    freq = total / count / 1000 / 1000
    return freq


def cur_cpu_temp():
    temp = 0
    with open("/sys/devices/virtual/thermal/thermal_zone0/hwmon0/temp1_input") as fin:
        temp = int(fin.read()) / 1000
    return temp


def fmt_cpu_freq_and_temp():
    return [" ~ cpu info ~ ", f"{cur_cpu_freq():.1f} GHz", f"{cur_cpu_temp():.1f}°C"]


def fmt_sys_load():
    labels = ["01", "05", "15"]
    load = getloadavg()
    return map(lambda t: f"load {t[0]}: {t[1]}", zip(labels, load))


def fmt_uptime():
    MIN_SEC = 60
    HOUR_MIN = 60
    HOUR_SEC = HOUR_MIN * MIN_SEC
    DAY_HOUR = 24
    DAY_SEC = DAY_HOUR * HOUR_SEC
    WEEK_DAY = 7
    WEEK_SEC = WEEK_DAY * DAY_SEC

    secs = int(time() - boot_time())
    weeks = secs // WEEK_SEC
    days = (secs % WEEK_SEC) // DAY_SEC
    hours = (secs % WEEK_SEC % DAY_SEC) // HOUR_SEC
    mins = (secs % WEEK_SEC % DAY_SEC % HOUR_SEC) // MIN_SEC

    return [" ~ uptime ~ ", f"{weeks:02}w, {days:02}d, ", f"{hours:02}h, {mins:02}m"]


def main():
    while True:
        draw(*fmt_cpu_freq_and_temp())
        delay()

        draw(*fmt_sys_load())
        delay()

        draw(*fmt_uptime())
        delay()


if __name__ == "__main__":
    main()
