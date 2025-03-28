import ZHOR_Modules.fileManager as fm

# generate .rule files


# append dates from 1900 to 2030
for year in range(1900, 2031):
    formatted_year = '$'.join(str(year))
    print(f'${formatted_year}')


# prepend dates from 
for year in range(1900, 2031):
    formatted_year = '^'.join(str(year)[::-1])
    print(f'^{formatted_year}')


# append and prepend common paddings
# taken from t3l3machus psudohash
# https://github.com/t3l3machus/psudohash

paddings = fm.fileToSimpleList('common-paddings.txt')

for p in paddings:
    formatted = '$'.join(p)
    print(f'${formatted}')

    formatted_reverse = '$'.join(p[::-1])
    print(f'${formatted_reverse}')


for p in paddings:
    formatted = '^'.join(p)
    print(f'^{formatted}')
    
    formatted_reverse = '^'.join(p[::-1])
    print(f'^{formatted_reverse}')


# append 2 digits
for i in range(0, 100):
    formatted_number = f"{i:02}"
    print(f"${formatted_number[0]} ${formatted_number[1]}")


# prepend 2 digits
for i in range(0, 100):
    formatted_number = f"{i:02}"
    print(f"^{formatted_number[0]} ?{formatted_number[1]}")


# append 3 digits
for i in range(0, 1000):
    formatted_number = f"{i:03}"
    print(f"${formatted_number[0]} ${formatted_number[1]} ${formatted_number[2]}")


# prepend 3 digits
for i in range(0, 1000):
    formatted_number = f"{i:03}"
    print(f"^{formatted_number[0]} ^{formatted_number[1]} ^{formatted_number[2]}")