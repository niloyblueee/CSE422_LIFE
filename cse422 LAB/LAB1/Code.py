#INPUTS
graph = {'A': {'B': 75, 'C': 118,'E': 140}, 'B': {'A': 75}, 'C': {'A': 118,'D': 111}, 'D': {'C': 111},'E': {'A': 140, 'G': 80, 'F': 99}, 'F': {'E': 99, 'I': 211}, 'G': {'E':80, 'H': 97}, 'H': {'G': 97, 'I': 101}}
heuristics = {'A': 366, 'B': 374, 'C': 329, 'D': 244, 'E': 253, 'F': 178, 'G': 193, 'H': 98, 'I': 0}

import heapq as q
def A_star_search(graph, heuristics, start, goal):
  queue = [] # Use it as priority Queue
  visited = []
  tracker={}
  cost = 0
  parents={}
  for nodes in heuristics:
    parents[nodes] = None
    
  #q.heappush(queue, (graph[start])) <= same as for loop neighbour
  q.heappush(queue, (0 + heuristics[start],start))
  tracker.update({start: 0 + heuristics[start]})


  while queue:
    current = q.heappop(queue)[1]

    visited.append(current)
 

   


    if current in graph.keys():
      neighbour = graph[current]  #POP
      
      for i in neighbour:
        if i not in visited:
          q.heappush(queue, ( (neighbour[i] + heuristics[i]), i )) # expand

          if i not in tracker.keys() or tracker[i] > (neighbour[i] + heuristics[i]):
            tracker.update({i: (neighbour[i] + heuristics[i])})
            
            parents[i] = current


  path = [goal]
  current = goal

  while parents[current] is not None:
    current = parents[current]
    path.append(current)
  path.reverse()
  
  for idx in range(len(path)-1):
    
    cost+=(graph[path[idx]][path[idx+1]])

  return path, cost  # Path, Cost


path, cost = A_star_search(graph, heuristics, 'A', 'I')
print("Path =", path)   # Path = ['A', 'E', 'G', 'H', 'I']
print("Cost =", cost)   # Cost = 418