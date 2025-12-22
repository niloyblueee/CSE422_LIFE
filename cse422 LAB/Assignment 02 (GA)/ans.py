import math
import random

# --- 1. SETUP DATA ---
# Component data: (Width, Height)
COMPONENTS = {
    "ALU": (5, 5),
    "Cache": (7, 4),
    "Control Unit": (4, 4),
    "Register File": (6, 6),
    "Decoder": (5, 3),
    "Floating Unit": (5, 5)
}

# Order of components in the chromosome
COMPONENT_ORDER = ["ALU", "Cache", "Control Unit", "Register File", "Decoder", "Floating Unit"]

# Pairs that need wiring
WIRE_PAIRS = [
    ("Register File", "ALU"),
    ("Control Unit", "ALU"),
    ("ALU", "Cache"),
    ("Register File", "Floating Unit"),
    ("Cache", "Decoder"),
    ("Decoder", "Floating Unit")
]

GRID_SIZE = 25

# --- 2. FITNESS CALCULATION FUNCTIONS ---

def get_block_bounds(x, y, width, height):
    """Calculates the boundaries of a block."""
    return {
        "left": x,
        "right": x + width,
        "bottom": y,
        "top": y + height
    }

def check_overlap(rect1, rect2):
    """Returns True if two rectangles overlap."""
    # Logic: No overlap if one is completely to the side or above/below
    if rect1["right"] <= rect2["left"] or \
       rect1["left"] >= rect2["right"] or \
       rect1["bottom"] >= rect2["top"] or \
       rect1["top"] <= rect2["bottom"]:
        return False
    return True

def calculate_fitness(chromosome):
    """Calculates the fitness based on overlaps, wiring, and area."""
    
    # Extract coordinates and bounds for all blocks
    block_data = []
    for i in range(len(COMPONENT_ORDER)):
        name = COMPONENT_ORDER[i]
        x, y = chromosome[i]
        w, h = COMPONENTS[name]
        bounds = get_block_bounds(x, y, w, h)
        center = (x + w/2, y + h/2)
        block_data.append({"name": name, "bounds": bounds, "center": center})

    # 1. Calculate Overlaps
    overlap_count = 0
    for i in range(len(block_data)):
        for j in range(i + 1, len(block_data)):
            if check_overlap(block_data[i]["bounds"], block_data[j]["bounds"]):
                overlap_count += 1

    # 2. Calculate Total Wiring Distance
    total_wire_dist = 0
    # Map component names to their centers for easy lookup
    centers = {item["name"]: item["center"] for item in block_data}
    
    for start_node, end_node in WIRE_PAIRS:
        c1 = centers[start_node]
        c2 = centers[end_node]
        dist = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        total_wire_dist += dist

    # 3. Calculate Bounding Box Area
    all_x_min = min(b["bounds"]["left"] for b in block_data)
    all_x_max = max(b["bounds"]["right"] for b in block_data)
    all_y_min = min(b["bounds"]["bottom"] for b in block_data)
    all_y_max = max(b["bounds"]["top"] for b in block_data)
    
    area = (all_x_max - all_x_min) * (all_y_max - all_y_min)

    # Weights from the document
    alpha = 1000
    beta = 2
    gamma = 1
    
    fitness_value = -(alpha * overlap_count + beta * total_wire_dist + gamma * area)
    
    return fitness_value, overlap_count, total_wire_dist, area

# --- 3. GENETIC OPERATORS ---

def crossover_single_point(parent1, parent2):
    """Performs single-point crossover."""
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def crossover_two_point(parent1, parent2):
    """Performs two-point crossover (Task 2)."""
    point1 = random.randint(0, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1) - 1)
    
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

def mutate(chromosome, mutation_rate=0.1):
    """Randomly changes the coordinates of one block."""
    if random.random() < mutation_rate:
        block_index = random.randint(0, len(chromosome) - 1)
        new_x = random.randint(0, GRID_SIZE)
        new_y = random.randint(0, GRID_SIZE)
        chromosome[block_index] = (new_x, new_y)
    return chromosome

# --- 4. MAIN GA LOOP ---

def run_genetic_algorithm(initial_population, iterations=15):
    current_population = initial_population
    
    for gen in range(iterations):
        # Calculate fitness for everyone
        scored_population = []
        for chromo in current_population:
            fit, overlaps, wire, area = calculate_fitness(chromo)
            scored_population.append((fit, chromo, overlaps, wire, area))
        
        # Sort by fitness (descending, since values are negative)
        scored_population.sort(key=lambda x: x[0], reverse=True)
        
        # Elitism: Carry top 2 to next generation
        new_gen = [scored_population[0][1], scored_population[1][1]]
        
        # Fill the rest of the population (6 members total)
        while len(new_gen) < 6:
            # Selection: Randomly pick two parents
            p1 = random.choice(current_population)
            p2 = random.choice(current_population)
            
            # Crossover (using single point for Task 1)
            c1, c2 = crossover_single_point(p1, p2)
            
            # Mutation
            new_gen.append(mutate(c1))
            if len(new_gen) < 6:
                new_gen.append(mutate(c2))
        
        current_population = new_gen
        
    # Get the best result from the final generation
    best_fit, best_chromo, best_ov, best_wire, best_area = calculate_fitness(current_population[0])
    return best_chromo, best_fit, best_ov, best_wire, best_area

# Sample P1 to P6 from the document
sample_pop = [
    [(9,3), (12, 15), (13, 16), (1,13), (4,15), (9, 6)],
    [(8, 0), (7,12), (4,11), (1,13), (14,10), (9,11)],
    [(6, 5), (12, 9), (9, 7), (8, 6), (2, 7), (3, 1)],
    [(3,11), (11, 12), (14, 11), (6, 10), (3,11), (3,0)],
    [(10, 12), (8, 16), (10, 4), (13, 6), (6, 0), (3, 7)],
    [(0, 2), (0, 0), (14, 12), (4, 5), (12, 4), (3, 10)]
]

best_layout, fit, overlaps, wire, area = run_genetic_algorithm(sample_pop)

print(f"Best Fitness: {fit}")
print(f"Overlaps: {overlaps}, Wiring: {wire:.2f}, Area: {area}")
print("Optimal Placement (Bottom-Left):")
for name, coords in zip(COMPONENT_ORDER, best_layout):
    print(f"{name}: {coords}")