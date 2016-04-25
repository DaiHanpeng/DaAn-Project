import wpf

from System.Windows import Window

class DaAnDialog(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'DaAnDialog.xaml')
    
    def DataGrid_SelectionChanged(self, sender, e):
        pass
