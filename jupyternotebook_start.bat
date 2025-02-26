ECHO 
ECHO 仮想環境を有効化しJupyter Notebookを自動起動
ECHO 仮想環境を終了する場合は"deactivate"を実行

set minicondapath=C:\Users\blues\miniconda3
set kankyo=jupyter

%windir%\System32\cmd.exe /K "%minicondapath%\Scripts\activate.bat %minicondapath% & activate %kankyo% & jupyter notebook"
