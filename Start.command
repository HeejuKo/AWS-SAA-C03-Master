#!/bin/zsh
cd "$(dirname "$0")"

clear
echo "=========================================="
echo "   AWS SAA-C03 Master - Start Program"
echo "=========================================="
echo ""

# 1. Python 설치 여부 확인
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "[안내] 이 Mac에 Python이 설치되어 있지 않습니다."
    echo "지금부터 Python 설치 안내를 진행합니다."
    echo ""

    # Homebrew가 있으면 자동 설치 시도
    if command -v brew >/dev/null 2>&1; then
        echo "Homebrew를 통해 Python 3.11을 설치합니다..."
        brew install python@3.11

        if command -v python3 >/dev/null 2>&1; then
            PYTHON_CMD="python3"
        else
            echo ""
            echo "[오류] Python 설치 후에도 python3 명령을 찾지 못했습니다."
            echo "터미널을 완전히 닫았다가 다시 열고 이 파일을 다시 실행해 주세요."
            read -k 1 "?계속하려면 아무 키나 누르세요..."
            exit 1
        fi
    else
        echo "Homebrew가 설치되어 있지 않아 Python 자동 설치를 진행할 수 없습니다."
        echo ""
        echo "먼저 아래 명령어로 Homebrew를 설치해 주세요:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        echo ""
        echo "설치 후 다시 이 파일을 실행해 주세요."
        read -k 1 "?계속하려면 아무 키나 누르세요..."
        exit 1
    fi
fi

echo "[확인] 사용 Python: $($PYTHON_CMD --version 2>&1)"
echo ""

# 2. pip 준비
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    echo "[안내] pip를 준비합니다..."
    $PYTHON_CMD -m ensurepip --upgrade
fi

# 3. 가상환경 생성
if [ ! -d ".venv" ]; then
    echo "[안내] 가상환경(.venv)을 생성합니다..."
    $PYTHON_CMD -m venv .venv
fi

# 4. 가상환경 활성화
source .venv/bin/activate

# 5. 패키지 설치
echo "필요한 환경(Streamlit)을 확인 및 설치 중입니다... (최초 1회만 시간 소요)"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo ""
echo "프로그램을 시작합니다. 잠시만 기다려주세요!"
echo "(곧 인터넷 브라우저가 자동으로 열립니다)"
echo ""

# 6. 프로그램 실행
python -m streamlit run app.py
