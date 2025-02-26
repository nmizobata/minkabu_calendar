ECHO minicondaの設定および仮想環境の自動起動
ECHO 仮想環境を終了する場合は"deactivate"を実行
ECHO googleapi: googleカレンダー等、google apiを使うアプリ向け
ECHO conda install google-api-python-client google-auth
ECHO conda install google-auth-httplib2   : 上記をInstallすれば自動的にインストールされる
ECHO conda install google-auth-oauthlib
ECHO conda install pandas
ECHO conda install beutifulsoup4
ECHO conda install lxml

set minicondapath=C:\Users\blues\miniconda3
set kankyo=googleapi
set drive=c:

%drive%
%windir%\System32\cmd.exe /K "%minicondapath%\Scripts\activate.bat %minicondapath% & activate %kankyo%"
