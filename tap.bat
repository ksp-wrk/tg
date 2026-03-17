::adb shell input tap 111 1150 

:a
timeout /T 6
adb shell input tap 55 125 

adb shell input tap 185 1115 
::timeout /T 2
adb shell input tap 670 120 
::timeout /T 2
adb shell input tap 525 120 
::timeout /T 2
adb shell input swipe 500 1000 300 300 
::timeout /T 2
adb shell input tap 220 1300 
::timeout /T 2
::pause
adb shell input tap 200 1355 
::timeout /T 2
:adb shell input keyevent KEYCODE_HOME
::timeout /T 3
goto a