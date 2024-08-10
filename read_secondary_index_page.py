
INNODB_PAGE_SIZE = 16 * 1024


def read_page(file_path, page_no):
    with open(file_path, 'rb') as f:
        f.seek(page_no * INNODB_PAGE_SIZE)
        page = f.read(INNODB_PAGE_SIZE)
    return page


def read_index_name(page_data):
    # print(page_data)
    # 把读取到的数据转成字节数组
    byte_arr = bytearray(page_data)

    # 前面92个字节是 File Header 和 Page Header，从第93个字节开始
    offset = 93
    # 读取 infimum recorder header 的头记录最后两个字节是第一条记录的偏移量
    # 最后2个字节才是第一条数据的偏移位置，直接先读取到第一个记录信息，基本上是固定的位置了
    first_offset = int.from_bytes(byte_arr[(offset + 5):(offset + 6)], byteorder='big')
    # print(first_offset)

    index_vale_map = {}
    index_char_offset = 93 + first_offset
    # print(byte_arr[index_char_offset:index_char_offset+16])
    while True:
        # 当前索引的字符串长度
        char_len = int.from_bytes(byte_arr[index_char_offset:(index_char_offset + 1)], byteorder='big')
        # 读取8个字节看看有没有值，如果都是0，假设已经读完，我们这测试就不那么严谨了；正常的找偏移节点的，会跳过了很多，就用这个笨办法了
        is_0 = int.from_bytes(byte_arr[index_char_offset:index_char_offset + 8], byteorder='big')
        if is_0 == 0:
            break
        cur_offset = char_len + 8 + 6  # 字符串长度+主键索引+(头信息+1个字符串长度)
        finish_char_offset = index_char_offset + cur_offset
        chunk = byte_arr[index_char_offset:finish_char_offset]

        # 读取索引列数据、和主键数据
        index_value_hex = chunk[6:(char_len + 6)]
        index_value = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in index_value_hex)
        if index_value not in index_vale_map:
            index_vale_map[index_value] = []
        index_vale_map[index_value].append(int.from_bytes(chunk[(char_len + 8):(char_len + 6 + 8)], byteorder='big'))

        # 输出读取到的一行数据
        # hex_chunk = " ".join(f"{byte:02x}" for byte in chunk)
        # print(f"{index_char_offset:08x} {hex_chunk:<39}")

        index_char_offset = index_char_offset + cur_offset

    # for item in index_vale_map:
    #     print(item + ": " + str(index_vale_map[item]))
    return index_vale_map.keys()


def start():
    # 修改这个页号信息，INFORMATION_SCHEMA.INNODB_BUFFER_PAGE 表中的 PAGE_NUMBER
    page_nos = [23760]
    file_path = '/usr/local/mysql/data/test/test2.ibd'
    index_names = []
    for page_no in page_nos:
        page_data = read_page(file_path, page_no)
        index_names.extend(read_index_name(page_data))

    print(index_names)


if __name__ == '__main__':
    start()
