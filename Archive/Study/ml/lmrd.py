# %%
import pandas as pd
import numpy as np

all_data = pd.read_csv('lmrd_review.csv', delimiter=',', error_bad_lines=False)

# %%
all_data.head()

# %%
all_data['review'] = all_data['review'].str.replace('\n', ' ')
all_data['review'] = all_data['review'].str.replace('\r', ' ')
all_data['review'] = all_data['review'].str.replace('\t', ' ')
all_data['review'] = all_data['review'].str.replace('  ', ' ')

# %%
all_data.dropna(subset=['review'], inplace=True)

# %%
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import SGDClassifier

# 데이터 분리
X = all_data["review"]
y = all_data["label"]

# 데이터셋을 학습용(80%)과 테스트용(20%)으로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 텍스트 벡터화
vectorizer = CountVectorizer(stop_words="english", max_features=5000)  # 상위 5000개의 단어만 사용
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 모델 정의
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Naive Bayes": MultinomialNB(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
    "LightGBM": LGBMClassifier(random_state=42),
    "SGD": SGDClassifier(loss="log", random_state=42)
}

results = {}

# 모델 학습 및 평가
for model_name, model in models.items():
    print(f"\n[ {model_name} ]")
    
    # XGBoost 모델의 경우 입력 데이터를 np.float32로 변환
    if model_name == "XGBoost":
        X_train_vec = X_train_vec.astype(np.float32)
        X_test_vec = X_test_vec.astype(np.float32)
    
    # 모델 학습
    model.fit(X_train_vec, y_train)
    
    # 테스트 데이터로 예측
    y_pred = model.predict(X_test_vec)
    
    # 정확도 계산
    accuracy = accuracy_score(y_test, y_pred)
    results[model_name] = accuracy
    
    # 평가 결과 출력
    print(f"정확도: {accuracy:.2f}")
    print("분류 리포트:")
    print(classification_report(y_test, y_pred))

# 결과 비교
print("\n모델 별 정확도 비교:")
for model_name, accuracy in results.items():
    print(f"{model_name}: {accuracy:.2f}")

# %%
import numpy as np

# CountVectorizer에서 단어 목록 가져오기
feature_names = vectorizer.get_feature_names_out()

# 모델 별 긍정/부정 단어 상위 20개 추출 함수
def extract_top_words(model, feature_names, model_name):
    if hasattr(model, "coef_"):  # 선형 모델 (Logistic Regression, Linear SVM)
        coefficients = model.coef_[0]
        sorted_indices = np.argsort(coefficients)
        negative_top20 = [(feature_names[i], coefficients[i]) for i in sorted_indices[:20]]
        positive_top20 = [(feature_names[i], coefficients[i]) for i in sorted_indices[-20:]]
    elif hasattr(model, "feature_importances_"):  # 트리 기반 모델 (Random Forest)
        importances = model.feature_importances_
        sorted_indices = np.argsort(importances)
        negative_top20 = [(feature_names[i], importances[i]) for i in sorted_indices[:20]]
        positive_top20 = [(feature_names[i], importances[i]) for i in sorted_indices[-20:]]
    else:
        print(f"{model_name} 모델은 가중치 또는 중요도를 제공하지 않음.")
        return None, None

    return negative_top20, positive_top20

# 각 모델에 대해 단어 추출
for model_name, model in models.items():
    print(f"\n[ {model_name} ]")
    negative_top20, positive_top20 = extract_top_words(model, feature_names, model_name)
    
    if negative_top20 and positive_top20:
        print("\n부정 단어 상위 20개:")
        for word, weight in negative_top20:
            print(f"{word}: {weight:.4f}")
        
        print("\n긍정 단어 상위 20개:")
        for word, weight in positive_top20:
            print(f"{word}: {weight:.4f}")


# %%
from nltk.corpus import opinion_lexicon
from nltk import download

# 감성 사전 다운로드
download("opinion_lexicon")

# %%
import re

# 긍정/부정 단어 리스트 로드
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

# 텍스트 전처리 및 감성 단어 카운트 함수
def preprocess_and_count_sentiment(text):
    # 텍스트 소문자로 변환
    text = text.lower()
    # 특수 문자 및 숫자 제거
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()

    # 긍정/부정 단어 카운트
    pos_count = sum(1 for word in words if word in positive_words)
    neg_count = sum(1 for word in words if word in negative_words)
    return text, pos_count, neg_count

# %%
# 데이터 전처리 및 감성 단어 카운트 적용
all_data["review_cleaned"], all_data["pos_count"], all_data["neg_count"] = zip(
    *all_data["review"].apply(preprocess_and_count_sentiment)
)

# 데이터 확인
all_data.head()

# %%
from scipy.sparse import hstack

# 기존 텍스트 벡터화
X_text_vec = vectorizer.fit_transform(all_data["review_cleaned"])

# 긍정/부정 단어 카운트 추가
X_features = hstack([X_text_vec, all_data[["pos_count", "neg_count"]].values])

# 학습/테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X_features, all_data["label"], test_size=0.2, random_state=42)


# 모델 학습 및 평가
for model_name, model in models.items():
    print(f"\n[ {model_name} ]")
    
    # XGBoost 모델의 경우 입력 데이터를 np.float32로 변환
    if model_name == "XGBoost":
        X_train = X_train.astype(np.float32)
        X_test = X_test.astype(np.float32)
    
    # 모델 학습
    model.fit(X_train, y_train)
    
    # 테스트 데이터로 예측
    y_pred = model.predict(X_test)
    
    # 정확도 계산
    accuracy = accuracy_score(y_test, y_pred)
    results[model_name] = accuracy
    
    # 평가 결과 출력
    print(f"정확도: {accuracy:.2f}")
    print("분류 리포트:")
    print(classification_report(y_test, y_pred))

# 결과 비교
print("\n모델 별 정확도 비교:")
for model_name, accuracy in results.items():
    print(f"{model_name}: {accuracy:.2f}")



# %% [markdown]
# 빈도 기반 모델 별 정확도 비교:  
# Logistic Regression: 0.87  
# Naive Bayes: 0.85  
# Random Forest: 0.85  
# XGBoost: 0.86  
# LightGBM: 0.86  
# SGD: 0.88  
#   
# 사전 기반 모델 별 정확도 비교:  
# Logistic Regression: 0.87  
# Naive Bayes: 0.86  
# Random Forest: 0.85  
# XGBoost: 0.86  
# LightGBM: 0.86  
# SGD: 0.87  

# %%
# grid search를 위한 하이퍼파라미터 설정

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Naive Bayes": MultinomialNB(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
    "LightGBM": LGBMClassifier(random_state=42),
    "SGD": SGDClassifier(loss="log", random_state=42)
}

hyperparameters = {
    "Logistic Regression": {"C": [0.1, 1.0, 10.0]},
    "Naive Bayes": {"alpha": [0.1, 1.0, 10.0]},
    "Random Forest": {"n_estimators": [50, 100, 200]},
    "XGBoost": {"n_estimators": [50, 100, 200]},
    "LightGBM": {"n_estimators": [50, 100, 200]},
    "SGD": {"alpha": [0.0001, 0.001, 0.01]}
}

# %%
# GridSearchCV를 사용한 하이퍼파라미터 튜닝
from sklearn.model_selection import GridSearchCV

best_models = {}

for model_name, model in models.items():
    param_grid = hyperparameters[model_name]
    grid_search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1)
    
    if model_name == "XGBoost":
        X_train = X_train.astype(np.float32)
    
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    best_models[model_name] = best_model
    
    print(f"\n[ {model_name} ]")
    print(f"최적 하이퍼파라미터: {grid_search.best_params_}")
    print(f"최상 교차 검증 점수: {grid_search.best_score_:.2f}")
    

# %%
# 최적 모델 평가

for model_name, model in best_models.items():
    print(f"\n[ {model_name} ]")
    
    if model_name == "XGBoost":
        X_test = X_test.astype(np.float32)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"정확도: {accuracy:.2f}")
    print("분류 리포트:")
    print(classification_report(y_test, y_pred))

# %%
# 결과 비교

print("\n모델 별 정확도 비교:")
for model_name, model in best_models.items():
    if model_name == "XGBoost":
        X_test = X_test.astype(np.float32)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model_name}: {accuracy:.2f}")


