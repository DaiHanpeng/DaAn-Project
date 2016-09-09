#include <Constants.au3>

FileDelete("C:\A002\Reports\Calibration Curve*.txt")

If Not ProcessExists("HRSTART.exe") Then
	Run("C:\A002\BIN\HRSTART.exe","C:\A002\BIN")
	Sleep(2000)
	Send("advia")
	Send("{TAB}")
	Send("advia")
	Send("{ENTER}")
	;WinWaitActive("ADVIA 1800 - Operation Panel")
	WinWaitActive("ADVIA 2400 - Operation Panel")
EndIf

;View Calibration Curve Window
Run("C:\A002\BIN\CALIB.exe","C:\A002\BIN")
WinActivate("View Calibration Curve")
WinWaitActive("View Calibration Curve")

;click Print button
ControlClick("View Calibration Curve","Print","[ID:1151]")

;wait <Save to File/Print> window
WinActivate("Save to File/Print")
WinWaitActive("Save to File/Print")

;click <Select All> button
ControlClick("Save to File/Print", "Select &All", "[ID:1156]")

;de-select <Print &Graph> option
ControlClick("Save to File/Print", "Print &Graph", "[ID:1155]")

;click <Save to &File> button
ControlClick("Save to File/Print", "Save to &File", "[ID:1344]")

;wait <Save As> window
WinActivate("Save As")
WinWaitActive("Save As")

;enter file name of error report
Send("Calibration Curve " & @YEAR & @MON & @MDAY & "_" & @HOUR & @MIN & @SEC & ".TXT")
Send("{ENTER}")

;close View Calibration Curve Window
WinActivate("View Calibration Curve")
WinWaitActive("View Calibration Curve")
ControlClick("View Calibration Curve","","[ID:1007]")

;confirm to close
WinActivate("View Calibration Curve")
WinWaitActive("View Calibration Curve")
ControlClick("View Calibration Curve","&Yes","[ID:6]")
