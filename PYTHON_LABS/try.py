import numpy as np
import matplotlib.pyplot as plt

# Дані з таблиці
cos2_phi = np.array([1, 0.96, 0.88, 0.75, 0.58, 0.41, 0.25, 0.11, 0.03, 0, 0.03, 0.11, 0.25, 0.41, 0.58, 0.75, 0.88, 0.96])
I_exp = np.array([52, 48.3, 40.2, 25.5, 17.2, 8.9, 6.6, 4.4, 3.0, 2.7, 2.6, 3.8, 11.6, 22.5, 29.3, 37.2, 45.2, 44.3])

plt.figure(figsize=(9, 6))

# Теоретична крива (лінійна залежність I = 52 * cos^2(phi))
plt.plot([0, 1], [0, 52], color='blue', label='Теоретична (I_обчисл)', linewidth=2)

# Експериментальна крива (з'єднуємо точки по мірі зміни кута)
plt.plot(cos2_phi, I_exp, marker='o', linestyle='--', color='red', label='Експериментальна (I_експер)')

# Налаштування вигляду
plt.title('Залежність інтенсивності світла від $\cos^2(\\varphi)$ (Закон Малюса)', fontsize=14)
plt.xlabel('$\cos^2(\\varphi)$', fontsize=12)
plt.ylabel('Інтенсивність I, відн. од.', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12)

plt.tight_layout()
plt.show()