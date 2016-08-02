#include <Constants.au3>
#include <File.au3>

FileDelete("C:\A002\Reports\Error_*.txt")

If Not ProcessExists("HRSTART.exe") Then
	Run("C:\A002\BIN\HRSTART.exe","C:\A002\BIN")
	Sleep(2000)
	Send("advia")
	Send("{TAB}")
	Send("advia")
	Send("{ENTER}")
	WinWaitActive("ADVIA 1800 - Operation Panel")
EndIf

Run("C:\A002\BIN\SFYTRC.exe","C:\A002\BIN")
Sleep(300)

WinActivate("Error Report")
WinWaitActive("Error Report")

;click <Print> button
ControlClick("Error Report", "Print", "[ID:1008]")

;wait <Save to File/Print> window
WinActivate("Save to File/Print")
WinWaitActive("Save to File/Print")

;click <Save to File> button
ControlClick("Save to File/Print", "Save to File", "[ID:1010]")

;wait <Save As> window
WinActivate("Save As")
WinWaitActive("Save As")

;enter file name of error report
Send("Error_" & @YEAR & @MON & @MDAY & "_" & @HOUR & @MIN & @SEC & ".TXT")
Send("{ENTER}")

;Close Window
WinActivate("Error Report")
WinWaitActive("Error Report")
ControlClick("Error Report","","[ID:57665]")

;confirm to close the window
WinActivate("Error Report")
WinWaitActive("Error Report")
ControlClick("Error Report","","[ID:6]")





