import ctypes
import traceback
p = r"C:\Users\hp\miniconda3\envs\akulearn-mlops\Lib\site-packages\torch\lib\fbgemm.dll"
print('checking:', p)
try:
    ctypes.WinDLL(p)
    print('DLL_LOAD_OK')
except Exception as e:
    print('DLL_LOAD_ERROR', type(e), e)
    traceback.print_exc()
