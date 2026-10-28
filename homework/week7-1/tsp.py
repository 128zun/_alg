import numpy as np
import matplotlib.pyplot as plt
import random
import math

# 固定亂數種子，確保每次測試的資料與結果一致
np.random.seed(42)
random.seed(42)

# ==========================================
# 1. 產生測試資料與輔助函數
# ==========================================
NUM_CITIES = 15
# 隨機生成 15 個城市的 (x, y) 座標，範圍在 0~100 之間
cities = np.random.rand(NUM_CITIES, 2) * 100

def calculate_distance(city1, city2):
    return np.linalg.norm(city1 - city2)

# 建立距離矩陣
dist_matrix = np.zeros((NUM_CITIES, NUM_CITIES))
for i in range(NUM_CITIES):
    for j in range(NUM_CITIES):
        dist_matrix[i][j] = calculate_distance(cities[i], cities[j])

def route_distance(route):
    """計算整條路線的總距離（包含回到起點）"""
    dist = 0
    for i in range(NUM_CITIES):
        dist += dist_matrix[route[i]][route[(i + 1) % NUM_CITIES]]
    return dist

# 隨機初始路線
initial_route = list(range(NUM_CITIES))
random.shuffle(initial_route)
initial_dist = route_distance(initial_route)

# ==========================================
# 5. 貪婪演算法 (Greedy Algorithm)
# 概念：每次尋找距離當前城市最近的未訪問城市
# ==========================================
def greedy_tsp():
    unvisited = list(range(NUM_CITIES))
    current_city = unvisited.pop(0) # 從城市 0 開始
    route = [current_city]
    
    while unvisited:
        # 找出距離當前城市最近的下一個城市
        nearest_city = min(unvisited, key=lambda city: dist_matrix[current_city][city])
        route.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
        
    return route, route_distance(route)

# ==========================================
# 1. 改良法 (2-opt Improvement Method)
# 概念：反轉路徑中的兩個節點區段，若能消除交叉使距離縮短則更新
# ==========================================
def two_opt_tsp(route):
    best_route = route.copy()
    improved = True
    while improved:
        improved = False
        for i in range(1, NUM_CITIES - 2):
            for j in range(i + 1, NUM_CITIES):
                if j - i == 1: continue # 相鄰節點反轉無意義
                # 反轉 i 到 j 的路徑
                new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
                if route_distance(new_route) < route_distance(best_route):
                    best_route = new_route
                    improved = True
        # 若遍歷所有組合都沒有改善，則結束
    return best_route, route_distance(best_route)

# ==========================================
# 2. 爬山演算法 (Hill Climbing)
# 概念：隨機交換兩個城市，若距離變短則接受，走到無法變短為止
# ==========================================
def hill_climbing_tsp(route, max_iterations=1000):
    current_route = route.copy()
    current_dist = route_distance(current_route)
    
    for _ in range(max_iterations):
        # 隨機挑選兩個要交換的城市索引
        i, j = random.sample(range(NUM_CITIES), 2)
        new_route = current_route.copy()
        new_route[i], new_route[j] = new_route[j], new_route[i]
        
        new_dist = route_distance(new_route)
        if new_dist < current_dist:
            current_route = new_route
            current_dist = new_dist
            
    return current_route, current_dist

# ==========================================
# 3. 模擬退火法 (Simulated Annealing)
# 概念：引入溫度機制，有一定機率接受較差的解，以跳出局部最佳解
# ==========================================
def simulated_annealing_tsp(route, initial_temp=1000, cooling_rate=0.995, min_temp=1):
    current_route = route.copy()
    current_dist = route_distance(current_route)
    best_route = current_route.copy()
    best_dist = current_dist
    
    temp = initial_temp
    while temp > min_temp:
        i, j = random.sample(range(NUM_CITIES), 2)
        new_route = current_route.copy()
        new_route[i], new_route[j] = new_route[j], new_route[i]
        new_dist = route_distance(new_route)
        
        # 若更好則接受，若較差則按機率接受
        if new_dist < current_dist or random.random() < math.exp((current_dist - new_dist) / temp):
            current_route = new_route
            current_dist = new_dist
            
            # 隨時記錄歷史最佳解
            if current_dist < best_dist:
                best_route = current_route.copy()
                best_dist = current_dist
                
        temp *= cooling_rate
        
    return best_route, best_dist

# ==========================================
# 4. 梯度下降法 (Steepest Descent / 離散最陡下降)
# 概念：評估當前路徑的「所有可能交換鄰居」，選擇下降幅度最大的一步
# ==========================================
def steepest_descent_tsp(route):
    current_route = route.copy()
    current_dist = route_distance(current_route)
    
    while True:
        best_neighbor = None
        best_neighbor_dist = current_dist
        
        # 展開當前狀態的所有鄰居 (交換任意兩城市) 以尋找最大梯度 (下降最多)
        for i in range(NUM_CITIES - 1):
            for j in range(i + 1, NUM_CITIES):
                neighbor = current_route.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                d = route_distance(neighbor)
                
                if d < best_neighbor_dist:
                    best_neighbor_dist = d
                    best_neighbor = neighbor
                    
        # 如果找到的最好鄰居比現在好，則更新並繼續；否則已達局部極小值，停止
        if best_neighbor is not None:
            current_route = best_neighbor
            current_dist = best_neighbor_dist
        else:
            break
            
    return current_route, current_dist

# ==========================================
# 執行與視覺化結果
# ==========================================
routes = {}
distances = {}

# 記錄初始狀態
routes['Initial'] = initial_route
distances['Initial'] = initial_dist

# 執行五種演算法
routes['Greedy'], distances['Greedy'] = greedy_tsp()
# 為了公平展示優化能力，後面四種皆以同一個 random_initial_route 為起點
routes['2-Opt'], distances['2-Opt'] = two_opt_tsp(initial_route)
routes['Hill Climbing'], distances['Hill Climbing'] = hill_climbing_tsp(initial_route)
routes['Steepest Descent'], distances['Steepest Descent'] = steepest_descent_tsp(initial_route)
routes['Simulated Annealing'], distances['Simulated Annealing'] = simulated_annealing_tsp(initial_route)

# 終端機輸出結果
print(f"測試城市數量: {NUM_CITIES}")
print("-" * 40)
for method, dist in distances.items():
    print(f"{method:20s}: {dist:.2f}")

# 繪圖視覺化比較
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, (method, route) in enumerate(routes.items()):
    ax = axes[idx]
    # 擷取按路徑排序的座標 (包含回到原點的閉環)
    route_coords = cities[route + [route[0]]]
    ax.plot(route_coords[:, 0], route_coords[:, 1], marker='o', linestyle='-', color='b')
    ax.plot(route_coords[0, 0], route_coords[0, 1], marker='s', color='r', markersize=8) # 起點標記為紅色方塊
    ax.set_title(f"{method}\nDist: {distances[method]:.2f}")
    ax.set_xticks([])
    ax.set_yticks([])

# 隱藏多餘的子圖空間
axes[5].axis('off')
plt.tight_layout()
plt.show()