#include <Constants.au3>

FileDelete("C:\A002\Reports\REAGENT INVENTORY*.txt")

If Not ProcessExists("HRSTART.exe") Then
	Run("C:\A002\BIN\HRSTART.exe","C:\A002\BIN")
	Sleep(2000)
	Send("advia")
	Send("{TAB}")
	Send("advia")
	Send("{ENTER}")
	WinWaitActive("ADVIA 1800 - Operation Panel")
EndIf



RunWait("Reagent.exe","C:\A002\BIN",@SW_MAXIMIZE)
WinActivate("Reagent Inventory")
WinWaitActive("Reagent Inventory")

Send("{LALT}F")
Sleep(300)

Send("{DOWN}")
Sleep(300)
Send("{ENTER}")

WinWaitActive("Save to File/Print")
Send("{TAB}")
Sleep(300)
Send("{ENTER}")

Send("{TAB 2}")
Sleep(300)
Send("{ENTER}")



