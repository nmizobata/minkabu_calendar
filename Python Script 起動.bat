rem Python�t�@�C���̋N���p�o�b�`�t�@�C���e���v���[�g
rem minicondapath : miniconda3�̃f�B���N�g���p�X
rem kankyo        : ���z����
rem drive         : ���s�h���C�u
rem python        : �v���W�F�N�g�t�H���_��(__main__.py���ŏ��Ɏ��s�����)
rem pypath        : �v���W�F�N�g�t�H���_������f�B���N�g���p�X

set minicondapath=C:\Users\blues\miniconda3
set kankyo=XXXXXXX
set drive=c:
set python=YYYYYYY
set pypath=C:\cfd_log\

%drive%
cd %pypath%
%windir%\System32\cmd.exe /K "%minicondapath\Scripts\activate.bat %kankyo%&python %python%"

rem pause
