#include <Constants.au3>
#include <File.au3>

FileDelete("C:\A002\Reports\Control_*.txt")

If Not ProcessExists("HRSTART.exe") Then
	Run("C:\A002\BIN\HRSTART.exe","C:\A002\BIN")
	Sleep(2000)
	Send("advia")
	Send("{TAB}")
	Send("advia")
	Send("{ENTER}")
	WinWaitActive("ADVIA 1800 - Operation Panel")
EndIf

Run("C:\A002\BIN\RTMONITOR.exe","C:\A002\BIN")
Sleep(300)

WinActivate("Realtime Monitor")
WinWaitActive("Realtime Monitor")

;click Standard
;2 = relative coords to the client area of the active window
Opt("MouseCoordMode", 2)
MouseMove(400, 26, 0)
MouseClick($MOUSE_CLICK_LEFT)

;determine how many records there.
WinActivate("Realtime Monitor")
WinWaitActive("Realtime Monitor")
Send("{DOWN}")

Local $iRecordCount = 0;
Local $bEnd = False
Local $strLastText = ""
While (False == $bEnd)
	If "" == ControlGetText ( "Realtime Monitor", "", 1011) Then
		$bEnd = True
	ElseIf $strLastText == ControlGetText ( "Realtime Monitor", "", 1011) Then
		$bEnd = True
	ElseIf $strLastText <> ControlGetText ( "Realtime Monitor", "", 1011) Then
		$strLastText = ControlGetText ( "Realtime Monitor", "", 1011)
		$iRecordCount += 1
		Send("{DOWN}")
	EndIf
WEnd

If 0 <> $iRecordCount Then
	;click print
	MouseMove(950, 26, 0)
	MouseClick($MOUSE_CLICK_LEFT)

	;
	WinWaitActive("Save to File/Print")
	Send("1")
	Sleep(100)
	Send("{TAB}")
	Sleep(200)
	Send($iRecordCount)
	Sleep(100)
	ControlClick("Save to File/Print","",3)

	;Save As
	WinWaitActive("Save As")
	Send("Control_" & @YEAR & @MON & @MDAY & "_" & @HOUR & @MIN & @SEC & ".TXT")
	;Send("{TAB 2}")
	;Sleep(100)
	Send("{ENTER}")
EndIf

;Close Window
WinActivate("Realtime Monitor")
WinWaitActive("Realtime Monitor")
ControlClick("Realtime Monitor","",1020)

;Confirm Ti Exit
WinWaitActive("Realtime Monitor")
Send("{ENTER}")

















