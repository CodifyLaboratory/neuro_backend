pow = [
    0.078, 0.143, 0.016, 0.034, 0.037,
    0.099, 0.096, 0.042, 0.025, 0.043,
    0.054, 0.034, 0.021, 0.025, 0.164,
    0.046, 0.03, 0.031, 0.026, 0.149,
    0.065, 0.032, 0.026, 0.035, 0.282,
    0.881, 0.279, 0.141, 12.908, 8.12,
    0.065, 0.035, 0.031, 0.045, 0.066,
    0.048, 0.017, 0.053, 0.029, 0.335,
    0.023, 0.035, 0.033, 0.028, 0.117,
    0.048, 0.025, 0.02, 0.018, 0.038,
    0.038, 0.04, 0.014, 0.018, 0.022,
    0.085, 0.034, 0.035, 0.021, 0.08,
    0.893, 0.112, 0.185, 0.127, 0.491,
    6.298, 0.916, 0.807, 0.143, 0.364
]

# sample = [
#     0. "AF3/theta", 1. "AF3/alpha", 2. "AF3/betaL", 3. "AF3/betaH", 4. "AF3/gamma",
#     5. "F7/theta", 6. "F7/alpha", 7. "F7/betaL", 8. "F7/betaH", 9. "F7/gamma",
#     10. "F3/theta", 11. "F3/alpha", 12. "F3/betaL", 13. "F3/betaH", 14. "F3/gamma",
#     15. "FC5/theta", 16. "FC5/alpha", 17. "FC5/betaL", 18. "FC5/betaH", 19. "FC5/gamma",
#     20. "T7/theta", 21. "T7/alpha", 22. "T7/betaL", 23. "T7/betaH", 24. "T7/gamma",
#     25. "P7/theta", 26. "P7/alpha", 27. "P7/betaL", 28. "P7/betaH", 29. "P7/gamma",
#     30. "O1/theta", 31. "O1/alpha", 32. "O1/betaL", 33. "O1/betaH", 34. "O1/gamma",
#     35. "O2/theta", 36. "O2/alpha", 37. "O2/betaL", 38. "O2/betaH", 39. "O2/gamma",
#     40. "P8/theta", 41. "P8/alpha", 42. "P8/betaL", 43. "P8/betaH", 44. "P8/gamma",
#     45. "T8/theta", 46. "T8/alpha", 47. "T8/betaL", 48. "T8/betaH", 49. "T8/gamma",
#     50. "FC6/theta", 51. "FC6/alpha", 52. "FC6/betaL", 53. "FC6/betaH", 54. "FC6/gamma",
#     55. "F4/theta", 56. "F4/alpha", 57. "F4/betaL", 58. "F4/betaH", 59. "F4/gamma",
#     60. "F8/theta", 61. "F8/alpha", 62. "F8/betaL", 63. "F8/betaH", 64. "F8/gamma",
#     65. "AF4/theta", 66. "AF4/alpha", 67. "AF4/betaL", 68. "AF4/betaH", 69. "AF4/gamma"
# ]

import numpy as np
from scipy import signal

# Это калькуляции для расчета fa1, fa2 и tar
# fa1 = np.log(pow[56] / pow[11])
# fa2 = np.log(pow[61] / pow[6])
# tar = pow[10] + pow[55] / pow[26] + pow[41]

# Это каналы,которые нужны для расчета coh
# wave1 = 'AF4', 'betaL' 67
# wave2 = 'F4', 'betaL' 57
# wave3 = 'F8', 'betaL' 62

# Это примеры трех наборов данных с нужными каналами,которые нужны для расчета coh
wave1 = [0.777, 1.019, 1.29, 1.513, 1.608, 1.535, 1.329, 1.091, 0.932, 0.932, 1.102, 1.367, 1.6, 1.692, 1.605, 1.391,
         1.139, 0.93, 0.801, 0.751, 0.759, 0.811, 0.915, 1.072, 1.256, 1.416, 1.492, 1.453, 1.316, 1.122, 0.92, 0.751,
         0.632, 0.567, 0.543, 0.538, 0.526, 0.497, 0.456, 0.42, 0.777, 1.019, 1.29, 1.513, 1.608, 1.535, 1.329, 1.091,
         0.932, 0.932, 1.102, 1.367, 1.6, 1.692, 1.605, 1.391]
wave2 = [0.089, 0.086, 0.091, 0.103, 0.12, 0.139, 0.154, 0.163, 0.164, 0.159, 0.15, 0.14, 0.132, 0.126, 0.123, 0.12,
         0.118, 0.117, 0.115, 0.112, 0.108, 0.103, 0.099, 0.094, 0.089, 0.083, 0.077, 0.072, 0.069, 0.07, 0.073, 0.079,
         0.084, 0.086, 0.085, 0.082, 0.08, 0.079, 0.082, 0.086, 0.089, 0.086, 0.091, 0.103, 0.12, 0.139, 0.154, 0.163,
         0.164, 0.159, 0.15, 0.14, 0.132, 0.126, 0.123, 0.12]
wave3 = [11.912, 13.737, 15.355, 16.343, 16.427, 15.603, 14.183, 12.711, 11.777, 11.763, 12.669, 14.093, 15.395, 16.005,
         15.699, 14.715, 13.603, 12.901, 12.829, 13.199, 13.598, 13.709, 13.529, 13.314, 13.333, 13.655, 14.14, 14.571,
         14.797, 14.802, 14.682, 14.581, 14.604, 14.75, 14.917, 15.001, 14.982, 14.888, 14.712, 14.42, 11.912, 13.737,
         15.355, 16.343, 16.427, 15.603, 14.183, 12.711, 11.777, 11.763, 12.669, 14.093, 15.395, 16.005, 15.699, 14.715]

# Это калькуляции для расчета coh
c1 = signal.coherence(wave1, wave2)
c2 = signal.coherence(wave1, wave3)
c3 = signal.coherence(wave2, wave3)

PC1 = np.nanmean(c1[1]) if np.any(np.isfinite(c1[1])) else 1
PC2 = np.nanmean(c2[1]) if np.any(np.isfinite(c2[1])) else 1
PC3 = np.nanmean(c3[1]) if np.any(np.isfinite(c3[1])) else 1

PC = (PC1 + PC2 + PC3) / 3 * 100
