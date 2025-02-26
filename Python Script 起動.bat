rem Pythonファイルの起動用バッチファイルテンプレート
rem minicondapath : miniconda3のディレクトリパス
rem kankyo        : 仮想環境名
rem drive         : 実行ドライブ
rem python        : プロジェクトフォルダ名(__main__.pyが最初に実行される)
rem pypath        : プロジェクトフォルダがあるディレクトリパス

set minicondapath=C:\Users\blues\miniconda3
set kankyo=XXXXXXX
set drive=c:
set python=YYYYYYY
set pypath=C:\cfd_log\

%drive%
cd %pypath%
%windir%\System32\cmd.exe /K "%minicondapath\Scripts\activate.bat %kankyo%&python %python%"

rem pause
