#-*- coding:utf-8 -*-

"""
데이터 전처리 모듈
"""
# 라이브러리 호출
import pandas as pd #pandas 데이터 처리 라이브러리
import datetime as dt #날짜변환
from pandas import Series, DataFrame #dataframe 호출
import sqlite3 # db 관리 라이브러리
import os #운영체제 제공 기능 라이브러리


"""
csv 파일 불러서 기본 데이터프레임 만들기
"""
# csv 파일 호출 - GUI로 파일 열어서 값 입력 될 수 있도록 하자.
base_dir = 'D:/Dropbox/genport_trade_result_analysis_tool/'
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

# csv 파일 데이터 읽기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port = "port" + str(i)
    port_df = "port"+str(i)+"_df"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        globals()[port_df]=pd.read_csv(locals()[port])

# 날짜-일일수익률 데이터프레임 만들기
port_merge_df = pd.DataFrame(columns={"날짜"}) # 날짜 컬럼만 가진 빈 데이터프레임 만들기
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port = "port" + str(i)
    port_df = "port"+str(i)+"_df"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        locals()[port_df] = pd.DataFrame({"날짜":locals()[port_df].날짜, "port" + str(i) + "_return":locals()[port_df].일일수익률})
        port_merge_df = pd.merge(port_merge_df, locals()[port_df], on="날짜", how="outer")

port_merge_df = port_merge_df.fillna(0)

"""
각 데이터 리스트 만들기
"""
# 날짜(date) 리스트 생성
date=port_merge_df['날짜']
date=[dt.datetime.strptime(str(i),"%Y%m%d").date() for i in date] #숫자형 YYYYMMDD를 날짜로 변환

# 일일수익률(port_return) 리스트 생성
for i in range(1,6):
    port_file = "port" + str(i) + "_file"  # 동적 변수명 규칙 : port(포트번호)_file
    port = "port" + str(i)
    port_return = "port" + str(i) + "_return"
    if not locals()[port_file] : # port 파일이 없으면 변수 안만들기
        pass
    else:
        locals()[port_return] = port_merge_df["port" + str(i) + "_return"]
        locals()[port_return] = [float(j) for j in locals()[port_return]]  # 수익률을 소수점 실수로 변환

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

