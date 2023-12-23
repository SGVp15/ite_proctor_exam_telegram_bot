import pygetwindow as pg

print(pg.getAllTitles())
win_name = 'passbase.kdbx - KeePass'
if win_name in pg.getAllTitles():
    pg.getWindowsWithTitle(win_name)[0].activate()