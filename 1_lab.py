import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

utility = {
    "вкрай погано": 0,
    "погано": 2,
    "посередньо": 5,
    "чудово": 8
}

outcomes = {
    "ліс": {"дощ": "вкрай погано", "сухо": "чудово"},
    "дім": {"дощ": "погано", "сухо": "посередньо"}
}

def expected_utility(decision, rain_probability):
    dry_probability = 1 - rain_probability
    
    outcome_rain = outcomes[decision]["дощ"]
    outcome_dry = outcomes[decision]["сухо"]
    
    # Очікувана корисність
    u = (rain_probability * utility[outcome_rain] + 
         dry_probability * utility[outcome_dry])
    
    return u

rain_probabilities = np.linspace(0, 1, 100)

utility_forest = [expected_utility("ліс", p) for p in rain_probabilities]
utility_home = [expected_utility("дім", p) for p in rain_probabilities]

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4) 

forest_line, = plt.plot(rain_probabilities, utility_forest, label="Ліс", color='m')
home_line, = plt.plot(rain_probabilities, utility_home, label="Дім", color='b')
plt.xlabel('Імовірність дощу')
plt.ylabel('Корисність')
plt.title('Рішення про пікнік')
plt.legend()
plt.grid(True)

axcolor = 'lightgoldenrodyellow'
ax_slider = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor=axcolor)  

rain_slider = Slider(ax_slider, 'Імовірність дощу', 0, 1, valinit=0.64)

decision_text = plt.text(0.5, 0.15, '', fontsize=12, ha='center', color='red', transform=fig.transFigure)
utility_forest_text = plt.text(0.5, 0.1, '', fontsize=10, ha='center', color='m', transform=fig.transFigure)
utility_home_text = plt.text(0.5, 0.05, '', fontsize=10, ha='center', color='b', transform=fig.transFigure)

def update(val):
    rain_prob = rain_slider.val
    expected_forest = expected_utility("ліс", rain_prob)
    expected_home = expected_utility("дім", rain_prob)

    forest_line.set_ydata([expected_utility("ліс", p) for p in rain_probabilities])
    home_line.set_ydata([expected_utility("дім", p) for p in rain_probabilities])
 
    if expected_home > expected_forest:
        decision = f"Сидимо вдома :) - {expected_home:.2f}"
    else:
        decision = f"Йдемо в ліс :) - {expected_forest:.2f}"

    decision_text.set_text(f'Рішення: {decision}')
    utility_forest_text.set_text(f'Очікувана корисність (Ліс): {expected_forest:.2f}')
    utility_home_text.set_text(f'Очікувана корисність (Дім): {expected_home:.2f}')
    
    fig.canvas.draw_idle()

rain_slider.on_changed(update)

update(0.64)

plt.show()
