
import datetime
import json

import requests

CURRENT_LONGITUDE="30.3134"
CURRENT_LATITUDE="120.3532"

	
CAIYUN_API_TOKEN="4Ol0FEX9i8oRvxaz"

def get_comprehensive_url(token: str, longitude, latitude):
    return (
        f"https://api.caiyunapp.com/v2.6/4Ol0FEX9i8oRvxaz/101.6656,39.2072/weather?"
        f"dailysteps=3&hourlysteps=48"
    )


def get_weather() -> dict | int:
    """
    :return: dict 天气查询结果 , int 天气查询失败后的代码
    """
    # old_weather = LocalStorage.get("weather")
    # if old_weather:
    #     old_data: dict = json.loads(old_weather)
    #     if old_data['server_time'] + 900 > datetime.datetime.now().timestamp():
    #         return old_data

    response = requests.get(get_comprehensive_url(CAIYUN_API_TOKEN, CURRENT_LONGITUDE, CURRENT_LATITUDE))
    if response.status_code == 200:
        resp_data = response.text
        # LocalStorage.set("weather", resp_data)
        return dict(json.loads(resp_data))
    print(response.status_code)
    return response.status_code
def output_weather():
    weather_map = {
        "CLEAR_DAY": "晴（白天）",
        "CLEAR_NIGHT": "晴（夜间）",
        "PARTLY_CLOUDY_DAY": "多云（白天）",
        "PARTLY_CLOUDY_NIGHT": "多云（夜间）",
        "CLOUDY": "阴",
        "LIGHT_HAZE": "轻度雾霾",
        "MODERATE_HAZE": "中度雾霾",
        "HEAVY_HAZE": "重度雾霾",
        "LIGHT_RAIN": "小雨",
        "MODERATE_RAIN": "中雨",
        "HEAVY_RAIN": "大雨",
        "STORM_RAIN": "暴雨",
        "FOG": "雾",
        "LIGHT_SNOW": "小雪",
        "MODERATE_SNOW": "中雪",
        "HEAVY_SNOW": "大雪",
        "STORM_SNOW": "暴雪",
        "DUST": "浮尘",
        "SAND": "沙尘",
        "WIND": "大风"
    }
    weather_info = get_weather()
    if isinstance(weather_info, dict):
        description = weather_map[weather_info['result']['realtime']['skycon']]
        temp = weather_info['result']['realtime']['temperature']
        humidity = weather_info['result']['realtime']['humidity'] * 100
        wind_speed = weather_info['result']['realtime']['wind']['speed']
        forcast = weather_info['result']['forecast_keypoint']
        answer = f"当前天气{description}，气温{temp}度，湿度{int(humidity)}%，风速是{wind_speed}米每秒。{forcast}"
    else:
        answer = "获取天气信息失败。"
    print(answer)
    return answer