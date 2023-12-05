import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 파일 경로 설정
file_path = '/home/jeongil/classi (1).csv'

# 데이터 불러오기
df = pd.read_csv(file_path, encoding='euc-kr')

def cal_safety_score(data):
    weights = {
        "사고": 0.02,
        "사망": 0.01,
        "부상": 0.03,
        "경찰서": 0.05,
        "파출소": 0.05,
        "119안전센터": 0.1,
        "불법주정차 합계": 0.03,
        "공원수": 0.05,
        "학교수": 0.07,
        "어린이인구수": 0.1,
        '자동차등록수': 0.03
    }
    result_df = pd.DataFrame(data).transpose()  # Create a new DataFrame to store the result

    result_df['안전도'] = (
        data['사고'] * weights['사고'] +
        data['사망'] * weights['사망'] +
        data['부상'] * weights['부상'] -
        data['경찰서'] * weights['경찰서'] +
        data['파출소'] * weights['파출소'] +
        data['119안전센터'] * weights['119안전센터'] +
        data['불법주정차 합계'] * weights['불법주정차 합계'] +
        data['공원수'] * weights['공원수'] +
        data['학교수'] * weights['학교수'] +
        data['어린이인구수'] * weights['어린이인구수'] +
        data['자동차등록수'] * weights['자동차등록수']
    )
    return result_df[['year', '구', '안전도']]  # Include 'year', '구', and '안전도' columns

def normalization(data):
    # Assuming data is your DataFrame
    # Select the columns you want to normalize (exclude non-numeric columns)
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    
    # Initialize the MinMaxScaler
    scaler = MinMaxScaler()

    # Fit and transform the selected columns
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

    return data

# 함수 호출
sum_result = pd.DataFrame()
for i in range(len(df)):
    result = cal_safety_score(df.iloc[i])
    sum_result = pd.concat([sum_result, result], ignore_index=True)

sum_result = normalization(sum_result)
sum_result.to_csv("/home/jeongil/nor_202122.csv", index=False)

# 'year' 열을 카테고리형으로 변환
sum_result['year'] = sum_result['year'].astype('category')

# 'year' 열을 제외한 피처와 레이블로 데이터 분리
X = sum_result.drop(['안전도'], axis=1)
y = sum_result['안전도']

# 학습 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# '구' 열을 원핫 인코딩
X_train = pd.get_dummies(X_train, columns=['구'], drop_first=True)
X_test = pd.get_dummies(X_test, columns=['구'], drop_first=True)

# RandomForestRegressor 초기화
model = RandomForestRegressor(n_estimators=100, random_state=42)

# 모델 학습
model.fit(X_train, y_train)

# 2024년의 데이터 생성 (여기서는 간단하게 2022년의 데이터를 복제)
X_2024 = X[X['year'] == 2022].copy()
X_2024['year'] = 2024  # 2024로 변경

# '구' 열을 원핫 인코딩
X_2024 = pd.get_dummies(X_2024, columns=['구'], drop_first=True)

# 2024년의 데이터로 예측
predictions = model.predict(X_2024)

# 예측 결과 출력
result_2024 = pd.DataFrame({'year': X_2024['year'], '안전도': predictions})
nor_24 = normalization(result_2024)
nor_24.to_csv("/home/jeongil/nor_24.csv", index=False)
