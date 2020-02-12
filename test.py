# 라이브러리 호출
import numpy as np #numpy 데이터 행렬 연산 라이브러리
import pandas as pd #pandas 데이터 처리 라이브러리
from pandas import DataFrame as df #DataFrame 가져오기
from pandas.plotting import table #테이블 그리기용
import matplotlib as mpl #그래프 작성 라이브러리
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc #한글폰트 설정
# import plotly.offline as py
from plotly.subplots import make_subplots
import plotly.graph_objects as go # 인터랙티브 차트 라이브러리
import datetime as dt #날짜변환
import statistics # 통계 처리 라이브러리 (표준편차 stdev 계산용)
import math #수학 계산 라이브러리 (제곱근 sqrt 계산용)
import os #운영체제 제공 기능 라이브러리
from pandas.plotting import register_matplotlib_converters # 차트 컨버터 관련 이슈 메시지 처리
register_matplotlib_converters() # 차트 컨버터 관련 이슈 메시지 처리
from matplotlib import gridspec # subplot size 조절
import sys # GUI 호출
from PyQt5.QtWidgets import * # GUI 호출
from PyQt5 import uic # GUI 호출
import seaborn as sns # 데이터시각화 라이브러리 (상관도 그리기 용)

# # 파일 열기 폼 띄우기
# form_class = uic.loadUiType("genport_analysis_tool.ui")[0]
#
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = MyWindow()
#     myWindow.show()
#     app.exec_()

# 한글 폰트 사용
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
mpl.rcParams['axes.unicode_minus'] = False # 마이너스(-) 폰트 깨짐 처리

# csv 파일 호출
base_dir = '/'
port1_file = 'trade_history_daily_825555.csv'
port2_file = 'trade_history_daily_861231.csv'
port3_file = 'trade_history_daily_949125.csv'
port4_file = ''
port5_file = ''

# os.path.join 폴더명과 파일명 합쳐서 전체 경로 만들기
for i in range(1,6):
    port_file = "port"+str(i)+"_file" # 동적 변수명 규칙 : port(포트번호)_file
    port = "port"+str(i)
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port]=os.path.join(base_dir,locals()[port_file]) #globals():전역변수 설정, locals():지역변수 설정

# 데이터를 dataframe(df)으로 변환
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port = "port" + str(i)
    port_df = "port"+str(i)+"_df"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_df]=pd.read_csv(locals()[port])

# 날짜(date) 데이터 만들기
date=[dt.datetime.strptime(str(i),"%Y%m%d").date() for i in port1_df.날짜] #숫자형 YYYYMMDD를 날짜로 변환

# 일일등락률(return) 데이터 만들기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_df = "port"+str(i)+"_df"
    port_return = "port" + str(i) + "_return"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_return]=[float(j) for j in locals()[port_df].일일수익률] #수익률을 소수점 실수로 변환

# 최초 설정액(initial) 세팅
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_initial = "port" + str(i) + "_initial"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_initial]=1000 # 1000원으로 일괄 세팅 => 나중에 임의 설정 값 받을 수 있게

# 잔고(balance) 데이터 만들기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_initial = "port" + str(i) + "_initial"
    port_return = "port"+str(i)+"_return"
    port_balance = "port" + str(i) + "_balance"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_balance]=[] # 잔고 리스트 생성
        balance = locals()[port_initial] # 잔고 초기값 설정
        for j in locals()[port_return]:
            balance = balance * (1 + j / 100) # 잔고 계산
            globals()[port_balance].append(balance) # 잔고 리스트에 추가

# 누적수익률(cum_return) 데이터 만들기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_initial = "port" + str(i) + "_initial"
    port_return = "port"+str(i)+"_return"
    port_balance = "port" + str(i) + "_balance"
    port_cum_return = "port" + str(i) + "_cum_return"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_cum_return]=[] # 누적수익률 리스트 생성
        for j in locals()[port_balance]:
            cum_return = (j/locals()[port_initial]-1)*100 # 누적수익률 계산
            globals()[port_cum_return].append(cum_return) # 누적수익률 리스트에 추가

# 종합잔고(all_port_balance) 데이터 만들기
port_balance_tmp = [] # 포트별 잔고 리스트 모을 임시 리스트 생성

for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_balance = "port" + str(i) + "_balance"

    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        port_balance_tmp.append(locals()[port_balance]) # 포트별 잔고 모으기

all_port_balance=[sum(i) for i in zip(*port_balance_tmp)] # 리스트간 더하기 This uses a combination of zip and * to unpack the list and then zip the items according to their index. You then use a list comprehension to iterate through the groups of similar indices, summing them and returning in their 'original' position. https://stackoverflow.com/questions/13783315/sum-of-list-of-lists-returns-sum-list

# 종합등락률(all_port_return) 데이터 만들기
port_return_tmp=[]

for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_initial = "port" + str(i) + "_initial"

    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        port_return_tmp.append(locals()[port_initial]) # 포트별 최초 설정액 모으기

all_port_initial=sum(port_return_tmp) # 리스트 요소 합계 구하기 - 전체 포트 최초 설정액 합계

all_port_return=[] # 빈 리스트 만들기
all_port_return_tmp=all_port_initial # 최초값 설정

for i in all_port_balance:
    all_port_return.append((i/all_port_return_tmp-1)*100) # 등락률 계산
    all_port_return_tmp=i # 임시값 평가액 갱신

# 종합누적수익률(all_port_cum_return) 데이터 만들기
all_port_cum_return=[] # 빈 리스트 만들기

for i in all_port_balance:
    cum_return = (i/all_port_initial-1)*100 #누적수익률 계산 (최초평가액 대비 현재평가액)
    all_port_cum_return.append(cum_return) # 누적수익률 리스트에 추가

# 수익률(return) 기준 or 잔고(balance) 기준 선택 옵션
port_show_option = 'return'

# 전고점(port_high) 데이터 만들기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_cum_return = "port"+str(i)+"_cum_return"
    port_balance = "port" + str(i) + "_balance"
    port_high = "port" + str(i) + "_high"

    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_high] = []  # 빈 리스트 생성
        high = 0  # 전고점 초기값 생성
        if port_show_option=='return':
            for j in locals()[port_cum_return]:
                if high < j:
                    high=j
                else:
                    high=high
                globals()[port_high].append(high) # 리스트에 추가
        else:
            for j in locals()[port_balance]:
                if high < j:
                    high = j
                else:
                    high = high
                globals()[port_high].append(high)  # 리스트에 추가

all_port_high = [] # 전체 전고점
high=0
if port_show_option == 'return': # 수익률 전고점 데이터 생성
    for j in all_port_cum_return:
        if high < j:
            high = j
        else:
            high = high
        all_port_high.append(high)  # 리스트에 추가
else: # 잔고 전고점 데이터 생성
    for j in all_port_balance:
        if high < j:
            high = j
        else:
            high = high
        all_port_high.append(high)  # 리스트에 추가

# Drawdown(port_DD) 데이터 만들기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_cum_return = "port"+str(i)+"_cum_return"
    port_balance = "port" + str(i) + "_balance"
    port_high = "port" + str(i) + "_high"
    port_DD = "port" + str(i) + "_DD"

    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_DD] = []  # 빈 리스트 생성
        DD = 0  # DD 초기값 생성
        if port_show_option=='return':
            for j, k in zip(locals()[port_cum_return],locals()[port_high]): # zip : 여러개의 자료형을 묶어서 처리해주는 함수
                DD = ((j+100)/(k+100)-1)*100
                globals()[port_DD].append(DD) # 리스트에 추가
        else:
            for j, k in zip(locals()[port_balance], locals()[port_high]):  # zip : 여러개의 자료형을 묶어서 처리해주는 함수
                DD = (j / k - 1) * 100
                globals()[port_DD].append(DD)  # 리스트에 추가

all_port_DD = [] # 전체 DD
DD = 0  # DD 초기값 생성
if port_show_option=='return':
    for j, k in zip(all_port_cum_return,all_port_high): # zip : 여러개의 자료형을 묶어서 처리해주는 함수
        DD = ((j+100)/(k+100)-1)*100
        all_port_DD.append(DD) # 리스트에 추가
else:
    for j, k in zip(all_port_balance, all_port_high):  # zip : 여러개의 자료형을 묶어서 처리해주는 함수
        DD = (j / k - 1) * 100
        all_port_DD.append(DD)  # 리스트에 추가

# 최대낙폭(port_MDD) 데이터 만들기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_DD = "port" + str(i) + "_DD"
    port_MDD = "port" + str(i) + "_MDD"

    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_MDD] = []  # 빈 리스트 생성
        MDD = 0  # MDD 초기값 생성
        for j in locals()[port_DD] :
            if MDD > j :
                MDD = j
            else:
                MDD = MDD
            globals()[port_MDD].append(MDD)

all_port_MDD = [] # 전체 MDD
MDD = 0  # MDD 초기값 생성
for j in all_port_DD:
    if MDD > j :
        MDD = j
    else:
        MDD = MDD
    all_port_MDD.append(MDD)

all_port_MDD_val = all_port_MDD[-1] # MDD 값 저장 (리스트 마지막 요소 호출)

# 언더워터(port_UW) 데이터 만들기
all_port_UW_tmp=[]
for i in all_port_DD:
    if i < 0 :
        UW = True
    else :
        UW = False
    all_port_UW_tmp.append(UW)

all_port_UW=[]
pre_val = False
for i, j in zip(date,all_port_UW_tmp):
    if pre_val != j: # 이전 값이 현재 값과 다르다면,
        if j: # 값이 참이면 (=DD 상태이면 = 언더워터에 진입하면)
            start = i # 시작 값에 해당 날짜를 부여한다.
        else: # 값이 거짓이면 (=DD에서 벗어나면 = 언더워터에서 탈출하면)
            all_port_UW.append((start,end)) # 리스트에 시작일과 종료일로 이루어진 튜플을 추가한다.
    pre_val = j
    end = i

# 반응형 차트 그리기
fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])
if port_show_option=='return': # 수익률 그래프 그리기
    for i in range(1, 6):
        port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
        port_cum_return = "port" + str(i) + "_cum_return"
        port_high = "port" + str(i) + "_high"
        port = "포트" + str(i)

        if not locals()[port_file]:  # port 파일이 없으면 변수 안만들기
            pass
        else:
            fig.add_trace(go.Scatter(x=date, y=locals()[port_cum_return],mode='lines', name=port, line=dict(width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(x=date, y=locals()[port_high], mode='lines', name=port_high, line=dict(width=1, dash='dot')), row=1, col=1)

    # fig.add_trace(go.scatter(x=date, y=all_port_cum_return, mode='lines',name="전체", line=dict(width=2)), row=1, col=1)
    # fig.add_trace(go.scatter(x=date[-1], y=all_port_cum_return[-1], mode='markers'), row=1, col=1)
    # fig.add_trace(go.scatter(x=date, y=all_port_high, mode='lines',name=False, line=dict(width=1, dash='dash')), row=1, col=1)
    # plt.title('포트별 수익률',pad=10) #차트 제목
    # plt.xlabel('기간', labelpad=10) #가로축 제목
    # plt.ylabel('수익률(%)', labelpad=10) #세로축 제목
else: # 잔고 그래프 그리기
    for i in range(1, 6):
        port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
        port_balance = "port" + str(i) + "_balance"
        port_high = "port" + str(i) + "_high"
        port = "포트" + str(i)

        if not locals()[port_file]:  # port 파일이 없으면 변수 안만들기
            pass
        else:
            fig.add_trace(go.Scatter(x=date, y=locals()[port_balance], mode='lines', name=port, line=dict(width=2)), row=1, col=1)
            fig.add_trace(
                go.Scatter(x=date, y=locals()[port_high], mode='lines', name=port_high, line=dict(width=1, dash='dot')), row=1, col=1)

    # fig.add_trace(go.scatter(x=date, y=all_port_cum_return, mode='lines', name="전체", line=dict(width=2)), row=1, col=1)
    # fig.add_trace(go.scatter(x=date[-1], y=all_port_cum_return[-1], mode='markers'), row=1, col=1)
    # fig.add_trace(go.scatter(x=date, y=all_port_high, mode='lines', name=False, line=dict(width=1, dash='dash')), row=1, col=1)
    # plt.title('포트별 수익률',pad=10) #차트 제목
    # plt.xlabel('기간', labelpad=10) #가로축 제목
    # plt.ylabel('수익률(%)', labelpad=10) #세로축 제목

# for (start, end) in all_port_UW: #UW 구간 세로선 + 색상 표시
#     plt.axvspan(start, end, color='gray', alpha=0.2)

# plt.legend() #범례 추가
# plt.grid(b=True, which='both',axis='both') #보조선 추가
# plt.tight_layout() #화면 꽉 차게

fig.write_html('genport_result.html', auto_open=True)


# 그래프 그리기
plt.figure(figsize=[18,9]) #figure 생성

gs = gridspec.GridSpec(nrows=2, # row 몇 개
                       ncols=2, # col 몇 개
                       height_ratios=[2, 1], # 높이 비율
                       width_ratios=[3,1]
                      )

# 수익률 그래프
plt.subplot(gs[0]) # 좌측 상단
if port_show_option=='return': # 수익률 그래프 그리기
    for i in range(1,6):
        port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
        port_cum_return = "port" + str(i) + "_cum_return"
        port_high = "port" + str(i) + "_high"
        port = "포트" + str(i)

        if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
            pass
        else:
            plt.plot(date,locals()[port_cum_return],linewidth=0.5,label=port)
            plt.text(date[-1], locals()[port_cum_return][-1], "{0:.2f}".format(locals()[port_cum_return][-1]) + '%')
            plt.plot(date, locals()[port_high],linewidth=0.2)

    plt.plot(date,all_port_cum_return,label="전체")
    plt.text(date[-1], all_port_cum_return[-1], "{0:.2f}".format(all_port_cum_return[-1]) + '%')  # 텍스트 추가 (위치 x, 위치 y, 텍스트 내용)
    plt.plot(date, all_port_high)
    #plt.yscale('log') #log 스케일 표시
    #plt.ylim(10,10000) #y축 범위 표시
    plt.title('포트별 수익률',pad=10) #차트 제목
    plt.xlabel('기간', labelpad=10) #가로축 제목
    plt.ylabel('수익률(%)', labelpad=10) #세로축 제목
else: # 잔고 그래프 그리기
    for i in range(1, 6):
        port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
        port_balance = "port" + str(i) + "_balance"
        port_high = "port" + str(i) + "_high"
        port = "포트" + str(i)

        if not locals()[port_file]:  # port 파일이 없으면 변수 안만들기
            pass
        else:
            plt.plot(date, locals()[port_balance], linewidth=0.5,label=port)
            plt.text(date[-1], locals()[port_balance][-1], "{0:.0f}".format(locals()[port_balance][-1]) + '(만원)')
            plt.plot(date, locals()[port_high], linewidth=0.2)

    plt.plot(date, all_port_balance, linewidth=1, label="전체")
    plt.text(date[-1], all_port_balance[-1], "{0:.0f}".format(all_port_balance[-1]) + '(만원)')  # 텍스트 추가 (위치 x, 위치 y, 텍스트 내용)
    plt.plot(date, all_port_high, linewidth=0.2)
    # plt.yscale('log') #log 스케일 표시
    # plt.ylim(10,10000) #y축 범위 표시
    plt.title('포트별 평가액', pad=10)  # 차트 제목
    plt.xlabel('기간', labelpad=10)  # 가로축 제목
    plt.ylabel('평가액(만원)', labelpad=10)  # 세로축 제목

for (start, end) in all_port_UW: #UW 구간 세로선 + 색상 표시
    plt.axvspan(start, end, color='gray', alpha=0.2)

plt.legend() #범례 추가
plt.grid(b=True, which='both',axis='both') #보조선 추가
plt.tight_layout() #화면 꽉 차게

# 텍스트 정보 추가
plt.subplot(gs[1]) # 우측 상단
time_period = (date[-1] - date[0]).days/365 # 거래 기간 계산
# plt.text(0.1,0.9,'투자기간 : ' + "{0:.2f}".format(time_period) + '년')
plt.axis('off') # 축 모두 없애기
# plt.xticks([], []) # x축 눈금 없애기
# plt.yticks([], []) # y축 눈금 없애기

# 데이터프레임 인덱스 지정
result_df = pd.DataFrame() # 데이터 프레임 생성
result_df_index = ["설정액(만원)","최종잔고(만원)","손익액(만원)","누적수익률(%)","CAGR(%)","MDD(%)","C/M","일평균수익률(%)","연환산수익률(%)","연환산변동폭(%)", "매매성공률(%)", "샤프비"]
result_df["index"]=result_df_index

for i in range(1, 5):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_initial = "port" + str(i) + "_initial" # '설정액(만원)'
    port_balance = "port" + str(i) + "_balance" # '최종잔고(만원)'
    port_profit = "port" + str(i) + "_profit" # '손익액(만원)'
    port_return = "port" + str(i) + "_return"  # '일일수익률'
    port_cum_return = "port" + str(i) + "_cum_return" # '누적수익률(%)'
    port_CAGR = "port" + str(i) + "_CAGR" # 'CAGR'
    port_MDD = "port" + str(i) + "_MDD"  # 'MDD'
    port_MDD_result = "port" + str(i) + "_MDD_result"  # 'MDD 결과값'
    port_CM = "port" + str(i) + "_CM" # 'C/M'
    port_day_yield = "port" + str(i) + '_day_yield' # '일평균수익률'
    port_year_yield = "port" + str(i) + 'year_yield' # '연환산수익률'
    port_year_volatility = "port" + str(i) + 'year_volatility' # '연환산변동성'
    port_win_ratio = "port" + str(i) + 'win_ratio' # '매매성공률'
    port_sharpe_ratio = "port" + str(i) + 'sharpe_ratio' # '샤프비'
    port_result = "port" + str(i) + 'result' # '결과값'
    port = "포트" + str(i)

    locals()[port_result] = [] #결과값 리스트 생성

    if not locals()[port_file]:  # port 파일이 없으면 변수 안만들기
        pass
    else:
        locals()[port_initial] = globals()[port_initial] # 설정액
        locals()[port_balance] = globals()[port_balance][-1] # 누적평가액
        locals()[port_profit] = int(locals()[port_balance]) - int(locals()[port_initial]) # 손익액
        locals()[port_cum_return] = locals()[port_cum_return][-1] # 누적수익률
        locals()[port_CAGR] = ((1 + locals()[port_cum_return]/100)**(1 / float(time_period))- 1)*100 # CAGR
        locals()[port_MDD_result] = locals()[port_MDD][-1] # MDD
        locals()[port_CM] = locals()[port_CAGR]/locals()[port_MDD_result]*-1 #C/M
        locals()[port_day_yield] = np.mean(np.array(locals()[port_return])) #일평균수익률
        locals()[port_year_yield] = locals()[port_day_yield]*365 #연환산수익률
        locals()[port_year_volatility] = statistics.stdev(locals()[port_return]) * math.sqrt(12) #연환산변동폭
        locals()[port_win_ratio] = sum(1 for item in locals()[port_return] if item > 0) / len(locals()[port_return]) * 100 # 매매성공률
        locals()[port_sharpe_ratio] = np.mean(np.array(locals()[port_return])) / statistics.stdev(locals()[port_return]) #샤프비

        locals()[port_result] = [locals()[port_initial],
                                 "{0:.2f}".format(locals()[port_balance]),
                                 locals()[port_profit],
                                 "{0:.2f}".format(locals()[port_cum_return]),
                                 "{0:.2f}".format(locals()[port_CAGR]),
                                 "{0:.2f}".format(locals()[port_MDD_result]),
                                 "{0:.2f}".format(locals()[port_CM]),
                                 "{0:.2f}".format(locals()[port_day_yield]),
                                 "{0:.2f}".format(locals()[port_year_yield]),
                                 "{0:.1f}".format(locals()[port_year_volatility]),
                                 "{0:.2f}".format(locals()[port_win_ratio]),
                                 "{0:.2f}".format(locals()[port_sharpe_ratio])]

        result_df["포트"+str(i)] = locals()[port_result]

# all_port_initial = all_port_initial # 설정액
all_port_balance = all_port_balance[-1] # 누적평가액
all_port_profit = int(all_port_balance) - int(all_port_initial) # 손익액
all_port_cum_return = all_port_cum_return[-1] # 누적수익률
all_port_CAGR = ((1 + all_port_cum_return/100)**(1 / float(time_period))- 1)*100 # CAGR
all_port_MDD_result = all_port_MDD[-1] # MDD
all_port_CM = all_port_CAGR/all_port_MDD_result*-1 #C/M
all_port_day_yield = np.mean(np.array(all_port_return)) #일평균수익률
all_port_year_yield = all_port_day_yield*365 #연환산수익률
all_port_year_volatility = statistics.stdev(all_port_return) * math.sqrt(12) #연환산변동폭
all_port_win_ratio = sum(1 for item in all_port_return if item > 0) / len(all_port_return) * 100 # 매매성공률
all_port_sharpe_ratio = np.mean(np.array(all_port_return)) / statistics.stdev(all_port_return) #샤프비

all_port_result = [all_port_initial,
                   "{0:.2f}".format(all_port_balance),
                   all_port_profit,
                   "{0:.2f}".format(all_port_cum_return),
                   "{0:.2f}".format(all_port_CAGR),
                   "{0:.2f}".format(all_port_MDD_result),
                   "{0:.2f}".format(all_port_CM),
                   "{0:.2f}".format(all_port_day_yield),
                   "{0:.2f}".format(all_port_year_yield),
                   "{0:.1f}".format(all_port_year_volatility),
                   "{0:.2f}".format(all_port_win_ratio),
                   "{0:.2f}".format(all_port_sharpe_ratio)]

result_df["전체"] = all_port_result

result_df.reset_index()
# result_df.set_index('index')

table(plt.subplot(gs[1]), result_df, loc='upper center', cellLoc='center', fontsize=20)

# Drawdown 그래프
plt.subplot(gs[2]) # 좌측 하단
for i in range(1, 6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_DD = "port" + str(i) + "_DD"
    port_MDD = "port" + str(i) + "_MDD"
    port = "포트" + str(i)

    if not locals()[port_file]:  # port 파일이 없으면 변수 안만들기
        pass
    else:
        plt.plot(date, locals()[port_DD], linewidth=0.5, alpha=0.5, label=port_DD)
        plt.plot(date, locals()[port_MDD], linewidth=0.5)

plt.plot(date, all_port_DD, linewidth=1, label="전체_DD")
plt.fill_between(date, 0, all_port_DD, color='blue', alpha=.25) # 그래프 채우기
plt.plot(date, all_port_MDD, linewidth=1)
plt.text(date[-1], all_port_MDD[-1],"{0:.2f}".format(all_port_MDD[-1])+'%') # 텍스트 추가 (위치 x, 위치 y, 텍스트 내용)
# plt.yscale('log') #log 스케일 표시
# plt.ylim(10,10000) #y축 범위 표시
plt.title('포트별 Drawdown', pad=10)  # 차트 제목
plt.xlabel('기간', labelpad=10)  # 가로축 제목
plt.ylabel('Drawdown(%)', labelpad=10)  # 세로축 제목

plt.legend() #범례 추가
plt.grid(b=True, which='both',axis='both') #보조선 추가
plt.tight_layout() #화면 꽉 차게

# 전략간 상관도 그리기
plt.subplot(gs[3]) # 우측 하단
port_return_df=pd.DataFrame() # 수익률 dataframe 생성
for i in range(1,6): # 파일이 있는 포트만 수익률 불러와서 dataframe 컬럼 만들기
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port_return = "port" + str(i) + "_return"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        port_return_df["port" + str(i)] = locals()[port_return]

port_return_df["전체"] = all_port_return

# 삼각형 마스크를 만든다(위 쪽 삼각형에 True, 아래 삼각형에 False)
mask = np.zeros_like(port_return_df.corr(method='pearson'))
mask[np.triu_indices_from(mask)] = True

sns.heatmap(port_return_df.corr(method='pearson'), vmin=-1, cmap='BuGn_r', mask=mask, annot=True, annot_kws={"size": 10}) # 피어슨 상관관계 히트맵 생성

for i in range(1,6): # 파일이 있는 포트 갯수 만큼만 y축 높이 만들기
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        plt.ylim([0, int(i)+1])

plt.gca().invert_yaxis() # y축 순서 반대로

plt.show() # plot 보여주기