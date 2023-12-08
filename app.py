from flask import Flask, render_template, request
import requests
import json

# Flask 애플리케이션 초기화
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        # 사용자 입력 받기
        prompt = request.form['prompt']
        api_key = request.form['api_key']

        # 카카오 API 요청 헤더 설정
        headers = {
            "Authorization": f"KakaoAK {api_key}",
            "Content-Type": "application/json"
        }

        # 카카오 API 요청 데이터 설정
        data = {
            "prompt": prompt
        }

        # 카카오 이미지 생성 API 호출
        response = requests.post(
            'https://api.kakaobrain.com/v2/inference/karlo/t2i', headers=headers, json=data)

        # 응답 확인 및 이미지 URL 추출
        if response.status_code == 200:
            print("Image generation successful.")
            response_data = json.loads(response.content)
            if response_data.get("images"):
                image_url = response_data["images"][0]["image"]
            else:
                print("No image found in response.")
        else:
            print(
                f"Image generation failed with status code: {response.status_code}")

    # 결과를 포함하여 템플릿 렌더링
    return render_template('index.html', image_url=image_url)


# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, port=5001)