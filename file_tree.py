import glob
import os.path

ndir = nfile = 0

def traverse(dir, depth):
    global ndir, nfile

    if depth == 0:
        # 최상위 폴더인 경우 폴더 이름만 출력
        print('|' + os.path.basename(dir))
        depth += 1  # 최상위 폴더 이후 depth 증가

    items = glob.glob(dir + '/*')
    file_count = 0
    has_printed_ellipsis = False  # '...' 표시 여부

    for obj in items:
        prefix = '|' + '    ' * depth + '|--'

        if os.path.isdir(obj):  # 디렉터리인 경우
            ndir += 1
            print(prefix + os.path.basename(obj))
            traverse(obj, depth + 1)

        elif os.path.isfile(obj):
            if file_count < 2:  # 파일이 2개 이하일 때만 출력
                print(prefix + os.path.basename(obj))
                file_count += 1
                nfile += 1
            elif not has_printed_ellipsis:  # 파일이 2개 이상일 때 ... 표시 후 종료
                print(prefix + "...")
                has_printed_ellipsis = True
                break
        else:
            print(prefix + "unknown object : " + obj)

if __name__ == '__main__':
    traverse('./data', 0)
    print('\n', ndir, 'directories,', nfile, 'files')
