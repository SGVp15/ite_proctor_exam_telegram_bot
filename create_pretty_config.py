names = ['EXCEL', 'CSV', 'Ispring', 'proctoredu', 'webdriver']
len_row = 116
for name in names:
    name = name.upper()
    print('# ', str(f'== ' * len_row)[:len_row])
    print('# ', str(f'-- {name} ' * len_row)[:len_row])
    print('# ', str(f'-- ' * len_row)[:len_row])
    print('')
    print('# ', str('-- ' * len_row)[:len_row])
    print('# ', str(f'== {name} ' * len_row)[:len_row])
    print('# ', str(f'== ' * len_row)[:len_row])
    print('')
