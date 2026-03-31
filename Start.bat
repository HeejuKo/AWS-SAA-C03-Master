@echo off
chcp 65001 > nul
echo ==========================================
echo    AWS SAA-C03 Master - Start Program
echo ==========================================
echo.

:: 1. 파이썬 설치 여부 확인
python --version >nul 2>&1
if %errorlevel% equ 0 goto :RUN_APP

:: 2. 파이썬이 없다면 자동 다운로드 및 설치 진행
echo [안내] PC에 파이썬이 설치되어 있지 않습니다.
echo 지금부터 파이썬을 자동으로 다운로드하고 설치합니다.
echo (이 작업은 PC 환경에 따라 1~3분 정도 소요될 수 있습니다. 잠시만 기다려주세요!)
echo.

:: 파이썬 공식 홈페이지에서 설치 파일 자동 다운로드 (윈도우 기본 기능)
curl -o python_installer.exe https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe

:: 사용자가 아무것도 누를 필요 없이 백그라운드에서 조용히 자동 설치 (PATH 추가 포함)
echo 다운로드 완료! 설치를 진행 중입니다...
start /wait python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

:: 설치가 끝나면 껍데기 파일 삭제
del python_installer.exe

echo.
echo 🎉 [성공] 파이썬 설치 및 기본 세팅이 완벽하게 끝났습니다!
echo 새로 설치된 파이썬을 시스템에 인식시키기 위해,
echo 지금 열려있는 이 까만 창을 닫고 'Start.bat'을 다시 한번만 실행해 주세요.
echo.
pause
exit /b

:: 3. 프로그램 실행 구간 (파이썬이 이미 설치된 경우 여기로 넘어옴)
:RUN_APP
echo 필요한 환경(Streamlit)을 확인 및 설치 중입니다... (최초 1회만 시간 소요)
pip install -r requirements.txt -q

echo.
echo 🚀 프로그램을 시작합니다. 잠시만 기다려주세요!
echo (곧 인터넷 브라우저가 자동으로 열립니다)
echo.
streamlit run app.py