import time
import os
import requests
from bs4 import BeautifulSoup

def get_gold_price():
    # 네이버 금융 금 시세 페이지 URL (국내 금 시세)
    url = "https://finance.naver.com/marketindex/goldDetail.naver?code=CMDT_GD"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 현재가 추출
            price = soup.select_one("p.no_today span.blind")
            
            # 전일대비 변동 금액 및 상승/하락 여부 추출
            diff = soup.select_one("p.no_exday span.blind")
            ico_type = soup.select_one("p.no_exday span.ico")
            
            price_text = price.text if price else "N/A"
            diff_text = diff.text if diff else "0"
            status = ico_type.text if ico_type else ""

            return {
                "price": price_text,
                "diff": diff_text,
                "status": status,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        print(f"오류 발생: {e}")
    return None

def main():
    print("실시간 금 시세 트래커를 시작합니다... (Ctrl+C 로 종료)")
    time.sleep(1)

    while True:
        # 화면 깨끗하게 정리 (Windows: cls / Mac, Linux: clear)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        data = get_gold_price()
        
        print("=" * 45)
        print("             💰 실시간 금 시세 💰")
        print("=" * 45)
        
        if data:
            print(f" 🕒 조회 시간 : {data['time']}")
            print(f" 💵 순금(1g)  : {data['price']} 원")
            print(f" 📈 전일 대비 : {data['status']} {data['diff']} 원")
        else:
            print(" 데이터를 불러오는 데 실패했습니다.")
            
        print("=" * 45)
        print(" 🔄 5초 후 자동으로 가격이 갱신됩니다...")
        
        # 5초 간격으로 반복 (원하는 주기로 변경 가능)
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")