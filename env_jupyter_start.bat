ECHO miniconda�̐ݒ肨��щ��z���̎����N��
ECHO ���z�����I������ꍇ��"deactivate"�����s

set minicondapath=C:\Users\blues\miniconda3
set kankyo=jupyter
set drive=c:

%drive%
%windir%\System32\cmd.exe /K "%minicondapath%\Scripts\activate.bat %minicondapath% & activate %kankyo%"
