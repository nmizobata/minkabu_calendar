# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# 

from MT4_common_lib import mt4_lib as mt

# +
print("サンプルファイルです")

mt4_name = "Titan MT4"
MT4 = mt.Mt4(mt4_name)
print("{}のデータフォルダは[{}]です".format(mt4_name, MT4.datafolder))
# -


