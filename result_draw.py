#-*- coding:utf-8 -*-

'''
플롯 작성 모듈
'''

# 라이브러리 호출
import numpy as np #numpy 데이터 행렬 연산 라이브러리
import pandas as pd #pandas 데이터 처리 라이브러리
from pandas import DataFrame as df #DataFrame 가져오기
from pandas.plotting import table #테이블 그리기용
import matplotlib as mpl #그래프 작성 라이브러리
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc #한글폰트 설정
from matplotlib import gridspec # subplot size 조절
import statistics # 통계 처리 라이브러리 (표준편차 stdev 계산용)
import math #수학 계산 라이브러리 (제곱근 sqrt 계산용)
from pandas.plotting import register_matplotlib_converters # 차트 컨버터 관련 이슈 메시지 처리
register_matplotlib_converters() # 차트 컨버터 관련 이슈 메시지 처리
import seaborn as sns # 데이터시각화 라이브러리 (상관도 그리기 용)

from result_data import * # 결과 데이터 모듈 호출

import sys # GUI 호출
from PyQt5.QtWidgets import * # GUI 호출
from PyQt5 import uic # GUI 호출

# 한글 폰트 사용
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
mpl.rcParams['axes.unicode_minus'] = False # 마이너스(-) 폰트 깨짐 처리

# 그래프 그리기
plt.figure(figsize=[18,9]) #figure 생성

gs = gridspec.GridSpec(nrows=2, # row 몇 개
                       ncols=2, # col 몇 개
                       # hspace=0.3,#위아래 여백
                       # wspace=0.1, #좌우 여백
                       height_ratios=[2, 1], # 높이 비율
                       width_ratios=[2, 1] # 너비 비율
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
plt.tight_layout() #화면 꽉 차게

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
plt.tight_layout() #화면 꽉 차게

plt.show() # plot 보여주기