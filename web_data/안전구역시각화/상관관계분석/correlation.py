import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 파일을 읽어 데이터프레임으로 변환
df = pd.read_csv('en_final.csv', delimiter=',')

# 상관계수 행렬 계산
corr = df.corr()

# 히트맵 그리기
plt.figure(figsize=(14, 14))
sns.heatmap(corr, annot=True, fmt='.2f', square=True)
plt.show()