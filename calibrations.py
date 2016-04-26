import matplotlib.pyplot as plt
from scipy import stats

res = [9.94, 26.88, 66.86, 148.77, 178.15, 216.67]
magnitude = [33689.50798, 90249.98716, 224441.3741, 491983.597, 586605.9217, 705302.461]
angle = [-0.4663205913,
        -0.557941331,
        -0.5849221276,
        -0.606361898,
        -0.6098806478,
        -0.6161327537]

slope, intercept, r_value, p_value, std_err = stats.linregress(res,magnitude)

print "slope: " + str(slope)
print "intercept: " + str(intercept)
print "r_value: " + str(r_value)

plt.scatter(res, magnitude)
plt.show()


