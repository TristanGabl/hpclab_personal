import numpy as np
import matplotlib.pyplot as plt

pi_phase_1 = 41.6
beta_phase_1 = 24.995
pi_phase_2 = 39.2
beta_phase_2 = 33.522

def f(x, pi, beta):
    return np.minimum(pi, beta * x)


x = np.logspace(-5, 8, 100, base=2.0)

plt.plot(x, f(x, pi_phase_1, beta_phase_1), label='Phase 1')
plt.plot(x, f(x, pi_phase_2, beta_phase_2), label='Phase 2')
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.ylim(1e-1, 1e2)
plt.grid(True)
plt.xlabel('Operational Intensity I [FLOPS/Byte]')
plt.ylabel('Performance P [GFLOPS/s]')
plt.title('Roofline Model')
plt.show()






