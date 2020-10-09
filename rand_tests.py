x = [0, 2, 0, 2, 3, 0, 4, 0]

water_held = 0
potential_water_held = 0
current_height = 0

for new_height in x:
    if new_height >= current_height:
        current_height = new_height
        water_held += potential_water_held
        potential_water_held = 0
    else:
        potential_water_held += current_height - new_height

print(water_held)
