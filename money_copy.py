import pandas as pd
import numpy as np
import operator
df=pd.read_csv('Deal_BTB.csv')
df1=pd.read_csv('Deal_Gold_no_Nah.csv')
df.drop('number',1)
df1.drop('number',1)
Gold_cost=0.006 #黄金和比特币的交易成本
BTB_cost=0.02
BTB_trade_flag=0 #BTB要买入信号
Gold_trade_flag=0 #黄金要买入信号
i=0 #调控黄金的时间
j=0 #调控整体时间进程,j为今天时间的index
df_Gold=df1.loc[0:2]
back_see=1
future_see_1=2
future_see_2=2
predict_day=2
TAV_daily=[]
transaction_date=[]
Gold_decision_count=0 #计算购买黄金的决策数
BTB_decision_count=0
correction=1826/1255
arr_money=[]
arr_ratio=[]
arr_days=[]
state=[1000,0,0] #三种财产的拥有状态[Cash,BTB,Gold],初始为[1000,0,0]
for w in range(20):
    i=0
    j=0
    Gold_decision_count=0 #计算购买黄金的决策数
    BTB_decision_count=0
    BTB_trade_flag=0 #BTB要买入信号
    Gold_trade_flag=0 #黄金要买入信号
    TAV_daily=[]
    transaction_date=[]
    df_Gold=df1.loc[0:2]
    state=[1000,0,0]
    for date_count in range(len(df.loc[:,'Date'])):
        temp=[] #记录交易日期信息
        BTB_trade_flag=0 #BTB要买入信号
        Gold_trade_flag=0 #黄金要买入信号

        walk1 = []
        df_BTB = df.iloc[0:j + 2 + predict_day]
        value_data1 = df['Value'].iloc[0:j + 2].values
        date_data1 = df['Date'].iloc[0:j + 2 + predict_day]
        for elem in value_data1:
            walk1.append(elem)
        day_diff = []
        for count in range(len(value_data1) - 1):
            elem_diff = (value_data1[count + 1] - value_data1[count]) / value_data1[count]
            day_diff.append(elem_diff)
        day_means1 = np.mean(day_diff)
        day_sd1 = np.std(day_diff)
        position = value_data1[0]
        epsilon = np.random.normal(loc=day_means1 + 1.0, scale=day_sd1, size=None)
        position = value_data1[len(value_data1) - 1] * epsilon
        walk1.append(position)
        for pred in range(predict_day - 1):
            # import pdb;pdb.set_trace()
            epsilon = np.random.normal(loc=day_means1 + 1.0, scale=day_sd1, size=None)
            position = position * epsilon
            walk1.append(position)
        for pred in range(predict_day):
            df_BTB=df_BTB.replace(df_BTB['Value'][len(df_BTB) - predict_day + pred] , walk1[len(df_BTB) - predict_day + pred])
        if(df.loc[j,'Date']==df1.loc[i,'Date']):
            Gold_cost=0.01 #黄金当天是否可以交易，可以为1
            walk2 = []
            df_Gold = df1.iloc[0:i + 2 + predict_day]
            value_data2 = df1['USD (PM)'].iloc[0:i + 2].values
            date_data2 = df1['Date'].iloc[0:i + 2 + predict_day]
            for elem in value_data2:
                walk2.append(elem)
            day_diff = []
            for count in range(len(value_data2) - 1):
                elem_diff = (value_data2[count + 1] - value_data2[count]) / value_data2[count]
                day_diff.append(elem_diff)
            day_means2 = np.mean(day_diff)
            day_sd2 = np.std(day_diff)
            position = value_data2[0]

            epsilon = np.random.normal(loc=day_means2 + 1.0, scale=day_sd2, size=None)
            position = value_data2[len(value_data2) - 1] * epsilon
            walk2.append(position)
            for pred in range(predict_day - 1):
                epsilon = np.random.normal(loc=day_means2 + 1.0, scale=day_sd2, size=None)
                position = position * epsilon
                walk2.append(position)
            for pred in range(predict_day):
                df_Gold = df_Gold.replace(df_Gold['USD (PM)'][len(df_Gold) - predict_day + pred],
                                                walk2[len(df_Gold) - predict_day + pred])
        else:
            Gold_cost=10000
        if(j<15): #找极小点与极大点
            min_value_BTB_index,min_value_BTB = min(enumerate(df_BTB.loc[0:j+future_see_1,'Value']),key=operator.itemgetter(1))
            max_value_BTB_index,max_value_BTB=max(enumerate(df_BTB.loc[0:j+future_see_1,'Value']),key=operator.itemgetter(1))
            j_index=list(df_BTB.loc[0:j+future_see_1,'Value']).index(df_BTB.loc[j,'Value'])
            min_value_Gold_index,min_value_Gold = min(enumerate(df_Gold.loc[0:i+future_see_1,'USD (PM)']),key=operator.itemgetter(1))
            max_value_Gold_index,max_value_Gold = max(enumerate(df_Gold.loc[0:i+future_see_1,'USD (PM)']),key=operator.itemgetter(1))
            i_index=list(df_Gold.loc[0:i+future_see_1,'USD (PM)']).index(df_Gold.loc[i,'USD (PM)'])
        else:
            min_value_BTB = min(df_BTB.loc[j-back_see:j+future_see_1,'Value'])
            max_value_BTB_index,max_value_BTB=max(enumerate(df_BTB.loc[j-back_see:j+future_see_1,'Value']),key=operator.itemgetter(1))
            j_index=list(df_BTB.loc[j-back_see:j+future_see_1,'Value']).index(df_BTB.loc[j,'Value'])
            min_value_Gold = min(df_Gold.loc[i-back_see:i+future_see_1,'USD (PM)'])
            max_value_Gold_index,max_value_Gold = max(enumerate(df_Gold.loc[i-back_see:i+future_see_1,'USD (PM)']),key=operator.itemgetter(1))
            i_index=list(df_Gold.loc[i-back_see:i+future_see_1,'USD (PM)']).index(df_Gold.loc[i,'USD (PM)'])
        if(state[1]==0 and abs(min_value_BTB-df_BTB.loc[j,'Value'])<=2000): #手中没有BTB时准备买入时才需要做这一步
            min_value_BTB=df_BTB.loc[j,'Value']
            min_index_BTB=j
            #print(j)
            if(max_value_BTB_index > j_index and ((min_value_BTB+max_value_BTB)*BTB_cost < (max_value_BTB-min_value_BTB)*0.9)): #有盈利所以购入的条件,发出购买信号
                BTB_trade_flag=1
        if(state[2]==0 and abs(min_value_Gold-df_Gold.loc[i,'USD (PM)'])<=20):
            min_value_Gold=df_Gold.loc[i,'USD (PM)']
            min_index_Gold=j
            if(max_value_Gold_index > i_index and ((min_value_Gold+max_value_Gold)*Gold_cost < (max_value_Gold-min_value_Gold)*0.9)): #有盈利所以购入的条件
                Gold_trade_flag=1
        if(state[1]!=0 and abs(max_value_BTB-df_BTB.loc[j,'Value'])<=20): #手中有BTB准备卖出且今天是极大值
            max_value_BTB_2_index , max_value_BTB_2 = max(enumerate(df_BTB.loc[j+1:j+future_see_2,'Value']),key=operator.itemgetter(1))  #max_value_BTB_2不包含j之前的最大值，用来寻找可能的卖点
            if(max_value_BTB_2<df_BTB.loc[j,'Value']): #如果第二个极大值比今天的值小
                state[0] = state[1]*df_BTB.loc[j,'Value']*(1-BTB_cost) #卖掉转换成现金
                state[1] = 0
                temp.append(j)
                temp.append(df_BTB.loc[j,'Date'])
                temp.append('B-')
                print(state,j,1,state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
            else:
                min_value_BTB_2_index , min_value_BTB_2 = min(enumerate(df_BTB.loc[j+1:j+future_see_2,'Value']),key=operator.itemgetter(1))  #同上
                if(min_value_BTB_2_index>max_value_BTB_2_index): #接下来的极小值在极大值之后，什么都不用做
                    print('', end='')
                else:
                    cash1 = (df_BTB.loc[j,'Value']*state[1]*(1-BTB_cost)) / (min_value_BTB_2*(1+BTB_cost)) * max_value_BTB_2 #卖了又买的情况
                    cash2 = state[1]*max_value_BTB_2 #不卖留到第二个极大值的情况
                    if(cash1-cash2>50):
                        state[0] = df_BTB.loc[j,'Value']*state[1]*(1-BTB_cost)
                        state[1]=0
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('B-')
                        print(state,j,2,state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
        if(state[2]!=0 and abs(max_value_Gold-df_Gold.loc[i,'USD (PM)'])<=15 and Gold_cost<1): #手中有Gold准备卖出且今天是极大值,且今天黄金可交易
            max_value_Gold_2_index , max_value_Gold_2 = max(enumerate(df_Gold.loc[i+1:i+future_see_2,'USD (PM)']),key=operator.itemgetter(1))  #max_value_Gold_2不包含j之前的最大值，用来寻找可能的卖点
            if(max_value_Gold_2<df_Gold.loc[i,'USD (PM)']): #如果第二个极大值比今天的值小
                state[0] = state[2]*df_Gold.loc[i,'USD (PM)']*(1-Gold_cost) #卖掉转换成现金
                state[2] = 0
                temp.append(j)
                temp.append(df_BTB.loc[j,'Date'])
                temp.append('G-')
                print(state,j,3,state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
            else:
                min_value_Gold_2_index , min_value_Gold_2 = min(enumerate(df_Gold.loc[i+1:i+future_see_2,'USD (PM)']),key=operator.itemgetter(1))  #同上
                if(min_value_Gold_2_index>max_value_Gold_2_index): #接下来的极小值在极大值之后，什么都不用做
                    print('',end='')
                else:
                    cash1 = (df_Gold.loc[i,'USD (PM)']*state[2]*(1-Gold_cost)) / (min_value_Gold_2*(1+Gold_cost)) * max_value_Gold_2 #卖了又买的情况
                    cash2 = state[2]*max_value_Gold_2 #不卖留到第二个极大值的情况
                    if(cash1>cash2):
                        state[0] = df_Gold.loc[i,'USD (PM)']*state[2]*(1-Gold_cost)
                        state[2]=0
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('G-')
                        print(state,j,4,state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
        if(BTB_trade_flag==1 or Gold_trade_flag==1): #收到了购买信号
            if(state[0]==0):
                if(BTB_trade_flag==1): #同时只能持有一种资产且Cash为0，不可能出现两个都要买的情况
                    BTB_maybe_number=(state[2]*df_Gold.loc[i,'USD (PM)']*(1-Gold_cost)) / (df_BTB.loc[j,'Value']*(1+BTB_cost)) #如果Gold换成BTB能买多少BTB
                    max_value_Gold_2=max(df_Gold.loc[i+1:i+future_see_2,'USD (PM)'])
                    if((max_value_BTB-min_value_BTB)*BTB_maybe_number-(max_value_BTB+min_value_BTB)*BTB_maybe_number*BTB_cost-max_value_Gold*state[2]*Gold_cost-(max_value_Gold_2-Gold_in_price)*state[2] > 2000): #判断是否更换为BTB的公式
                        state[1]=BTB_maybe_number
                        state[2]=0
                        BTB_in_price=df_BTB.loc[j,'Value']
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('G-B')
                        BTB_decision_count=BTB_decision_count+1
                        print(state,j,5,'换',state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
                else:
                    Gold_maybe_number=(state[1]*df_BTB.loc[j,'Value']*(1-BTB_cost)) / (df_Gold.loc[i,'USD (PM)']*(1+Gold_cost)) #如果BTB换成Gold能买多少Gold
                    max_value_BTB_2=max(df_BTB.loc[j+1:j+future_see_2,'Value'])
                    if((max_value_Gold-min_value_Gold)*Gold_maybe_number-(max_value_Gold+min_value_Gold)*Gold_maybe_number*Gold_cost-max_value_BTB*state[1]*BTB_cost-(max_value_BTB_2-BTB_in_price)*state[1] > 2000): #判断是否更换为Gold的公式
                        state[1]=0
                        state[2]=Gold_maybe_number
                        Gold_in_price=df_Gold.loc[i,'USD (PM)']
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('B-G')
                        Gold_decision_count=Gold_decision_count+1
                        print(state,j,6,'换',state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
            else: #有Cash时
                if(BTB_trade_flag==1 and Gold_trade_flag==0):
                    max_value_BTB_2=max(df_BTB.loc[j+1:j+future_see_2,'Value'])
                    benefit_BTB=(max_value_BTB_2-df_BTB.loc[j,'Value']) * state[0]/(df_BTB.loc[j,'Value']*(1+BTB_cost)) #乘号之后是所有现金能买到的BTB总数
                    min_value_Gold_2_index,min_value_Gold_2=min(enumerate(df_Gold.loc[i+1:i+future_see_2,'USD (PM)']),key=operator.itemgetter(1))
                    max_value_Gold_2_index,max_value_Gold_2=max(enumerate(df_Gold.loc[i+1:i+future_see_2,'USD (PM)']),key=operator.itemgetter(1))
                    if(max_value_Gold_2_index>min_value_Gold_2_index>0):
                        benefit_Gold=(max_value_Gold_2-min_value_Gold_2) * state[0]/(min_value_Gold_2*(1+Gold_cost))
                    else:
                        benefit_Gold=0
                    if(benefit_BTB - benefit_Gold > 20): #预测可能有误差所以要大于200阈值
                        state[1]=state[0]/(df_BTB.loc[j,'Value']*(1+BTB_cost))
                        state[0]=0
                        BTB_in_price=df_BTB.loc[j,'Value']
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('B+')
                        BTB_decision_count=BTB_decision_count+1
                        print(state,j,7,'Cash',state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
                elif(BTB_trade_flag==0 and Gold_trade_flag==1):
                    max_value_Gold_2=max(df_Gold.loc[i+1:i+future_see_2,'USD (PM)'])
                    benefit_Gold=(max_value_Gold_2-df_Gold.loc[i,'USD (PM)']) * state[0]/(df_Gold.loc[i,'USD (PM)']*(1+Gold_cost)) #乘号之后是所有现金能买到的Gold总数
                    min_value_BTB_2_index,min_value_BTB_2=min(enumerate(df_BTB.loc[j+1:j+future_see_2,'Value']),key=operator.itemgetter(1))
                    max_value_BTB_2_index,max_value_BTB_2=max(enumerate(df_BTB.loc[j+1:j+future_see_2,'Value']),key=operator.itemgetter(1))
                    if(max_value_BTB_2_index>min_value_BTB_2_index):
                        benefit_BTB=(max_value_BTB_2-min_value_BTB_2) * state[0]/(min_value_BTB_2*(1+BTB_cost))
                    else:
                        benefit_BTB=0
                    if(benefit_Gold - benefit_BTB > 200): #预测可能有误差所以要大于200阈值
                        state[2]=state[0]/(df_Gold.loc[i,'USD (PM)']*(1+Gold_cost))
                        state[0]=0
                        Gold_in_price=df_Gold.loc[i,'USD (PM)']
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('G+')
                        Gold_decision_count=Gold_decision_count+1
                        print(state,j,8,'Cash',state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
                elif(BTB_trade_flag==1 and Gold_trade_flag==1):
                    max_value_BTB_2=max(df_BTB.loc[j+1:j+future_see_2,'Value'])
                    benefit_BTB=(max_value_BTB_2-df_BTB.loc[j,'Value']) * state[0]/(df_BTB.loc[j,'Value']*(1+BTB_cost)) #乘号之后是所有现金能买到的BTB总数
                    max_value_Gold_2=max(df_Gold.loc[i+1:i+future_see_2,'USD (PM)'])
                    benefit_Gold=(max_value_Gold_2-df_Gold.loc[i,'USD (PM)']) * state[0]/(df_Gold.loc[i,'USD (PM)']*(1+Gold_cost)) #乘号之后是所有现金能买到的Gold总数
                    if(benefit_Gold > benefit_BTB):
                        state[2]=state[0]/(df_Gold.loc[i,'USD (PM)']*(1+Gold_cost))
                        state[0]=0
                        Gold_in_price=df_Gold.loc[i,'USD (PM)']
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('G+')
                        Gold_decision_count=Gold_decision_count+1
                    else:
                        state[1]=state[0]/(df_BTB.loc[j,'Value']*(1+BTB_cost))
                        state[0]=0
                        BTB_in_price=df_BTB.loc[j,'Value']
                        temp.append(j)
                        temp.append(df_BTB.loc[j,'Date'])
                        temp.append('B+')
                        BTB_decision_count=BTB_decision_count+1
                    print(state,j,9,'Cash',state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
        TAV_daily.append(state[0] + df_BTB.loc[j,'Value']*state[1] + df_Gold.loc[i,'USD (PM)']*state[2])
        if(len(temp)==3):
            transaction_date.append(temp)
        if(df_BTB.loc[j,'Date']==df_Gold.loc[i,'Date']):
            i=i+1
        j=j+1
    arr_money.append(state[0] + df_BTB.loc[j-1,'Value']*state[1] + df_Gold.loc[i-1,'USD (PM)']*state[2])
    arr_days.append(len(transaction_date))
    arr_ratio.append(Gold_decision_count/BTB_decision_count*correction)
with open('TAV_daily.txt','w') as file:
    for n in range(len(TAV_daily)):
        s = str(TAV_daily[n]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
with open('transaction_date.txt','w') as file:
    df_date=pd.DataFrame(transaction_date,columns=['index','Date','Decision'])
df_date.to_csv('transaction_date.txt')
state[0]=state[0] + df_BTB.loc[j-1,'Value']*state[1] + df_Gold.loc[i-1,'USD (PM)']*state[2]
state[1]=0
state[2]=0
print(state)
print('Total value average：'+str(np.mean(arr_money)))
print('ratio average：'+str(np.mean(arr_ratio)))
print('days average：'+str(np.mean(arr_days)))
print(df_BTB.shape)