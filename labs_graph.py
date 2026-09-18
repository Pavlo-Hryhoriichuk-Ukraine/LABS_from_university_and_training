import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Експериментальні дані
# Неон (Ne)
lambda_ne = np.array([7032, 6929, 6599, 6506, 6402, 6334, 6226, 6146, 6074, 5945, 5852, 5400, 5330])
n_ne = np.array([3108, 3112, 2980, 2949, 2908, 2862, 2858, 2812, 2788, 2722, 2692, 2418, 2372])

# Ртуть (Hg) — відомі лише поділки барабана монохроматора
n_hg = np.array([2830, 2746, 2618, 2478, 2904])

# Сортування даних Неону за зростанням поділок N
sort_idx = np.argsort(n_ne)
n_ne_sorted = n_ne[sort_idx]
lambda_ne_sorted = lambda_ne[sort_idx]

# Побудова інтерполяційної функції градуювальної кривої
f_interp = interp1d(n_ne_sorted, lambda_ne_sorted, kind='linear')
lambda_hg = f_interp(n_hg)

# Створення графіка
plt.figure(figsize=(10, 6), dpi=120)

# Градуювальна крива Неону
n_dense = np.linspace(n_ne_sorted.min(), n_ne_sorted.max(), 300)
plt.plot(n_ne_sorted, lambda_ne_sorted, 'o', color='tab:blue', label='Лінії Ne (експ.)', markersize=6)
plt.plot(n_dense, f_interp(n_dense), '-', color='tab:blue', alpha=0.7, label='Градуювальна крива Ne')

# Точки перетину для ліній Ртуті
plt.plot(n_hg, lambda_hg, 's', color='tab:red', markersize=7, zorder=5, label='Визначені лінії Hg')

# Побудова ліній перетину (проекцій) на осі
for n_val, l_val in zip(n_hg, lambda_hg):
    # Вертикальна лінія від осі X до кривої
    plt.vlines(x=n_val, ymin=plt.ylim()[0] if plt.ylim()[0] > 5000 else 5200, ymax=l_val,
               color='tab:red', linestyle='--', alpha=0.6)
    # Горизонтальна лінія від кривої до осі Y
    plt.hlines(y=l_val, xmin=plt.xlim()[0] if plt.xlim()[0] > 2300 else 2300, xmax=n_val,
               color='tab:red', linestyle='--', alpha=0.6)
    # Підпис довжини хвилі біля точки
    plt.annotate(f'{l_val:.1f} Å',
                 xy=(n_val, l_val),
                 xytext=(n_val - 35, l_val + 35),
                 fontsize=9,
                 color='darkred',
                 weight='bold')

plt.title('Градуювальна крива монохроматора та визначення довжин хвиль Hg', fontsize=13)
plt.xlabel('Поділки шкали монохроматора ($N$)', fontsize=11)
plt.ylabel('Довжина хвилі $\lambda$ (Å)', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

plt.show()

# Вивід значень у консоль
print("Результати визначення довжин хвиль ліній Ртуті (Hg):")
for n_val, l_val in sorted(zip(n_hg, lambda_hg)):
    print(f"N = {n_val:4d}  -->  lambda = {l_val:6.1f} Å")