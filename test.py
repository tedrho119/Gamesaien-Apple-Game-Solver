from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pyautogui
import numpy as np
import keyboard

enable_mouse_movements = True

def find_horizontal_vertical(grid):
    rows, cols = grid.shape

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0:
                continue
            total = grid[i, j]
            sequence = [(i, j)]
            for k in range(j + 1, cols):
                if grid[i, k] == 0:
                    break
                total += grid[i, k]
                sequence.append((i, k))
                if total == 10:
                    return sequence
                elif total > 10:
                    break

            total = grid[i, j]
            sequence = [(i, j)]
            for k in range(i + 1, rows):
                if grid[k, j] == 0:
                    break
                total += grid[k, j]
                sequence.append((k, j))
                if total == 10:
                    return sequence
                elif total > 10:
                    break
    return None

def find_rectangle_square(grid):
    rows, cols = grid.shape

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0:
                continue

            for width in range(1, cols - j + 1):
                for height in range(1, rows - i + 1):
                    total = 0
                    sequence = []
                    for x in range(i, i + height):
                        for y in range(j, j + width):
                            total += grid[x, y]
                            sequence.append((x, y))
                        else:
                            continue
                        break
                    else:
                        if total == 10:
                            return sequence
                        elif total > 10:
                            break 
    return None 

def update_grid(grid, sequence):
    for (i, j) in sequence:
        grid[i, j] = 0

def select_group(sequence, top_left_x, top_left_y, cell_width, cell_height):
    if not enable_mouse_movements:
        return
    x = top_left_x + sequence[0][1] * cell_width + cell_width / 2
    y = top_left_y + sequence[0][0] * cell_height + cell_height / 2
    pyautogui.moveTo(x, y, duration=0)
    pyautogui.mouseDown()
    for (i, j) in sequence[1:]:
        x = top_left_x + j * cell_width + cell_width / 2
        y = top_left_y + i * cell_height + cell_height / 2
        pyautogui.moveTo(x, y, duration=0)
    pyautogui.mouseUp()

def refetch_grid(driver):
    grid_container = driver.find_element(By.CLASS_NAME, "board-container")
    rows = grid_container.find_elements(By.CLASS_NAME, "row")
    grid = []
    for row in rows:
        cells = row.find_elements(By.CLASS_NAME, "cell")
        row_data = [int(cell.text) if cell.text else 0 for cell in cells]
        grid.append(row_data)
    return np.array(grid)

def toggle_mouse_movements():
    global enable_mouse_movements
    enable_mouse_movements = not enable_mouse_movements
    print(f"Mouse movements {'enabled' if enable_mouse_movements else 'disabled'}")

keyboard.on_press_key("esc", lambda _: toggle_mouse_movements())

# Main script
chrome_driver_path = "D:/lemon_game/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
url = "https://wwme.kr/lemon/play?mode=normal"
driver.get(url)

start_button = driver.find_element(By.CLASS_NAME, "game-button")
start_button.click()
print("Clicked the '🍋 게임 시작' button.")
time.sleep(3)

print("Move your mouse to the top-left corner of the grid and wait 5 seconds...")
time.sleep(5)
top_left_x, top_left_y = pyautogui.position()
print(f"Top-left corner: ({top_left_x}, {top_left_y})")

print("Move your mouse to the bottom-right corner of the grid and wait 5 seconds...")
time.sleep(5)
bottom_right_x, bottom_right_y = pyautogui.position()
print(f"Bottom-right corner: ({bottom_right_x}, {bottom_right_y})")

cell_width = (bottom_right_x - top_left_x) / 17
cell_height = (bottom_right_y - top_left_y) / 10

while True:
    grid = refetch_grid(driver)

    while True:
        sequence = find_horizontal_vertical(grid)
        if not sequence:
            sequence = find_rectangle_square(grid)
            if not sequence:
                print("No more groups found. Refetching grid...")
                break

        select_group(sequence, top_left_x, top_left_y, cell_width, cell_height)
        update_grid(grid, sequence)

# Close the browser (this won't be reached since the loop runs indefinitely)
driver.quit()
