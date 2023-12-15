
@Rem 'shell:startup' 快速启动

@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin

@Rem 切换到当前目录 8801, 19110
cd  %~dp0
python app.py

