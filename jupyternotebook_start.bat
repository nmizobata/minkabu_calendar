ECHO 
ECHO ���z����L������Jupyter Notebook�������N��
ECHO ���z�����I������ꍇ��"deactivate"�����s

set minicondapath=C:\Users\blues\miniconda3
set kankyo=jupyter

%windir%\System32\cmd.exe /K "%minicondapath%\Scripts\activate.bat %minicondapath% & activate %kankyo% & jupyter notebook"
