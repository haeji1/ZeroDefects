import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# 데이터 로드
df = pd.read_csv('data.csv')

# 'Time' 컬럼을 datetime 타입으로 변환
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

# JSON 파일의 cycles 및 steps 데이터
cycles_data = {
    # 이 부분 채워야함
}

# 스텝별 시작 및 종료 시각을 DataFrame으로 변환
steps_data = []
for cycle in cycles_data['cycles']:
    for step in cycle['steps']:
        for step_name, step_detail in step.items():
            steps_data.append({
                'Step': step_name,
                'Start': pd.to_datetime(step_detail['start_time'], format='%H:%M:%S'),
                'End': pd.to_datetime(step_detail['end_time'], format='%H:%M:%S')
            })

steps_df = pd.DataFrame(steps_data)

# 사용자 선택에 따른 컬럼 및 스텝 데이터 (예시를 위한 하드코딩, 사용자 입력에 따라 변경 가능)
# 예: {'A': ['step2'], 'B': ['step5', 'step6'], 'C': ['step1']}
user_selected = {
    'param1': ['step0', 'step2'],
    'param2': ['step5', 'step6'],
    'param3': ['step1']
}

# plt.figure(figsize=(15, 7))

# 사용자가 선택한 컬럼 및 스텝에 대해 반복
for column, steps in user_selected.items():
    selected_steps_df = steps_df[steps_df['Step'].isin(steps)]
    for _, row in selected_steps_df.iterrows():
        mask = (df['Time'] >= row['Start']) & (df['Time'] <= row['End'])
        filtered_df = df.loc[mask].copy()
        filtered_df['Elapsed Time'] = (filtered_df['Time'] - row['Start']).dt.total_seconds()
        elapsed_time_in_seconds = int(filtered_df['Elapsed Time'].iloc[-1])  # 마지막 행의 경과 시간을 가져옵니다.

        # # 해당 컬럼에 대해 그래프 그리기
        # if column in df.columns:
        #     plt.plot(filtered_df['Elapsed Time'], filtered_df[column], label=f"{column} - {row['Step']} ({elapsed_time_in_seconds}s)")
        # else:
        #     print(f'Warning: Column {column} does not exist in the DataFrame.')

# plt.xlabel('Elapsed Time[s]')
# plt.ylabel('Value')
# plt.legend()
# plt.show()