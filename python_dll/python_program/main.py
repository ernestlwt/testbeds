import ctypes

simpleDLL = ctypes.cdll.LoadLibrary("..\\dll\\SimpleDLL\\x64\\Debug\\SimpleDLL.dll")

result1 = simpleDLL.add(5, 3);
result2 = simpleDLL.minus(5, 3);

print("add result: " + str(result1))
print("minus result: " + str(result2))
