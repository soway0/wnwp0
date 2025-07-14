import pulp

# --- 데이터 설정 ---
# 각 여행지 정보: 이름, 만족도(가상), 관람 시간(시간), 입장료(원), 평균 식비(원)
places = {
    "설악산": {"satisfaction": 95, "time": 4, "admission": 3500, "food": 10000},
    "속초중앙시장": {"satisfaction": 85, "time": 2, "admission": 0, "food": 20000},
    "속초해수욕장": {"satisfaction": 80, "time": 1.5, "admission": 0, "food": 5000},
    "영금정": {"satisfaction": 75, "time": 1, "admission": 0, "food": 0},
    "아바이마을": {"satisfaction": 70, "time": 1.5, "admission": 0, "food": 15000},
    "국립산악박물관": {"satisfaction": 60, "time": 1.5, "admission": 0, "food": 0},
}

# 여행지 간 평균 이동 시간 및 비용 (가정)
avg_travel_time = 0.5  # 시간
avg_transport_cost = 5000  # 원

# --- 사용자 입력 ---
# 사용자가 설정하는 총 여행 시간과 예산
user_total_time = 8  # 8시간
user_total_budget = 50000  # 5만원

# --- 선형계획법 모델 구축 ---

# 1. 문제 정의: 만족도를 최대로 하는 문제
model = pulp.LpProblem("Sokcho_Trip_Optimizer", pulp.LpMaximize)

# 2. 변수 정의: 각 장소를 방문할지(1) 안 할지(0) 결정하는 이진 변수
visit_vars = pulp.LpVariable.dicts("Visit", places.keys(), cat='Binary')

# 3. 목적 함수 정의: 총 만족도의 합을 최대로
model += pulp.lpSum([places[p]["satisfaction"] * visit_vars[p] for p in places]), "Total_Satisfaction"

# 4. 제약 조건 정의
# (1) 시간 제약: 총 소요 시간(관람시간 + 이동시간) <= 사용자의 총 여행 시간
model += pulp.lpSum([
    (places[p]["time"] + avg_travel_time) * visit_vars[p] for p in places
]) <= user_total_time, "Total_Time_Constraint"

# (2) 예산 제약: 총 비용(입장료 + 식비 + 교통비) <= 사용자의 총 예산
model += pulp.lpSum([
    (places[p]["admission"] + places[p]["food"] + avg_transport_cost) * visit_vars[p] for p in places
]) <= user_total_budget, "Total_Budget_Constraint"

# --- 모델 해결 및 결과 출력 ---

def solve_and_print_results():
    """선형계획법 모델을 해결하고 결과를 출력합니다."""
    
    # 모델 해결
    model.solve()

    # 결과 출력
    print("--- 속초 여행 최적 경로 추천 ---")
    print(f"\n[입력 조건]")
    print(f"  - 최대 여행 시간: {user_total_time}시간")
    print(f"  - 최대 여행 예산: {user_total_budget:,}원\n")

    status = pulp.LpStatus[model.status]
    if status == 'Optimal':
        print("[추천 여행 계획]")
        total_satisfaction = 0
        total_time = 0
        total_cost = 0
        
        for place_name in places:
            if visit_vars[place_name].varValue == 1:
                place_info = places[place_name]
                print(f"  - {place_name} (만족도: {place_info['satisfaction']})")
                
                total_satisfaction += place_info['satisfaction']
                total_time += place_info['time'] + avg_travel_time
                total_cost += place_info['admission'] + place_info['food'] + avg_transport_cost

        print("\n[예상 결과]")
        print(f"  - 총 만족도: {pulp.value(model.objective):.2f}")
        print(f"  - 총 소요 시간: {total_time:.1f}시간")
        print(f"  - 총 예상 비용: {total_cost:,.0f}원")
    else:
        print("최적의 여행 계획을 찾을 수 없습니다.")
        print(f"이유: {status}")

if __name__ == "__main__":
    solve_and_print_results()
