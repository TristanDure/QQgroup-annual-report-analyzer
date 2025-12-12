import requests
import json

# 配置参数（替换为你的实际密钥和模型）
API_KEY = "sk-tFD2jbRlOCoZ0Nk6qpBKzNXU8G2ZXN6d9IkBzzGawIi2LeFG"
BASE_URL = "https://api.gemai.cc/v1"
MODEL = "[满血B]gemini-2.5-pro"  # 去掉多余前缀，使用平台要求的模型名

# 发送测试请求
def test_api():
    url = f"{BASE_URL}/chat/completions"  # 假设接口路径与OpenAI兼容
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "测试响应格式，请返回一句话"}]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 检查HTTP错误
        print("响应状态码:", response.status_code)
        print("响应内容:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print("请求失败:", str(e))
        if response:
            print("错误响应内容:", response.text)

if __name__ == "__main__":
    test_api()