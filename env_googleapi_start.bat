ECHO minicondaの設定および仮想環境の自動起動
ECHO 仮想環境を終了する場合は"deactivate"を実行
ECHO googleapi: googleカレンダー等、google apiを使うアプリ向け

set minicondapath=C:\Users\blues\miniconda3
set kankyo=googleapi
set drive=c:

%drive%
%windir%\System32\cmd.exe /K "%minicondapath%\Scripts\activate.bat %minicondapath% & activate %kankyo%"
