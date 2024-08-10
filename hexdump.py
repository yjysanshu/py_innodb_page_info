
INNODB_PAGE_SIZE = 16 * 1024


def read_page(file_path, page_no):
    with open(file_path, 'rb') as f:
        f.seek(page_no * INNODB_PAGE_SIZE)
        page = f.read(INNODB_PAGE_SIZE)
    return page


def hexdump(data, page_no):
    hex_str = data.hex()
    for i in range(0, len(hex_str), 32):
        chunk = hex_str[i:i+32]
        hex_chunk = ' '.join(chunk[j:j+2] for j in range(0, len(chunk), 2))
        ascii_chunk = ''.join(chr(int(chunk[j:j+2], 16)) if 32 <= int(chunk[j:j+2], 16) <= 126 else '.' for j in range(0, len(chunk), 2))
        print(f"{(page_no*INNODB_PAGE_SIZE+i//2):08x}  {hex_chunk:<39}  |{ascii_chunk}|")


def start():
    # 修改这个页号信息，INFORMATION_SCHEMA.INNODB_BUFFER_PAGE 表中的 PAGE_NUMBER
    page_no = 23760
    file_path = '/usr/local/mysql/data/test/test2.ibd'
    page_data = read_page(file_path, page_no)
    hexdump(page_data, page_no)


if __name__ == '__main__':
    start()
