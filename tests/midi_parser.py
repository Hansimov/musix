# encoding: utf-8
import os
import sys
import collections
import binascii
from math import floor, ceil

py_ver = sys.version_info[0]

# * Standard MIDI file format, updated 
# ** http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html

# * MIDI文件格式解析 | 码农家园 
# ** https://www.codenong.com/js59d74800b43b/

# * 读书笔记——MIDI文件结构简介 - 哔哩哔哩 
# ** https://www.bilibili.com/read/cv1753143/

# * MIDI文件格式分析──理论篇 - Midifan：我们关注电脑音乐 
# ** https://m.midifan.com/article_body.php?id=901

# * Note names, MIDI numbers and frequencies 
# ** https://newt.phys.unsw.edu.au/jw/notes.html

# * Frequency and Pitch of Sound: From Physclips 
# ** https://www.animations.physics.unsw.edu.au/jw/frequency-pitch-sound.htm

msg_level_D = {
    'shell'  : '1;34;40',
    'success': '1;32;40',
    'info'   : '1;36;40',
    'warn'   : '1;35;40',
    'error'  : '1;31;40',
}

def color_print(s, level=''):
    cb = '\x1b[{}m'
    ce = '\x1b[0m'

    cb = cb.format(msg_level_D[level])
    print(f'{cb}{s}{ce}')


bytes_L = []

hexchr = "0123456789abcdef"

TPQN = -1   # ticks per quarter-note
uspqn_L = []  # us per quarter-note
chan_inst_L = [] # list of [channel num, instrument num]
# NUME, DENO = [],[]
trk_cnt = -1

def sec2frm(sec):
    return ceil(sec*30)

def tick2sec(tick):
    return tick/TPQN * USPQN/10**6

def get_bytes(start,end=None):
    if end == None:
        end = start+1
    return "".join(bytes_L[start:end]).lower()

def hex2dec(hex_str,signed=False):
    if signed == False:
        return int(hex_str,16)
    else:
        sign = 1 if hex_str[0]==0 else -1
        return sign*int(hex_str[1:],16)

def bin2dec(bin_str):
    return int(bin_str,2)

def hex2bin(hex_str):
    bit_num = len(hex_str)*4 
    return "{val:0{width}b}".format(val=hex2dec(hex_str),width=bit_num)

def ptr2rc(ptr):
    row_num = 16
    row = ptr // row_num
    col = ptr % row_num
    return row, hexchr[col]


def read_delta_time(ptr, info_level=0):
    """ return (int, int) : (pointer offset, num of tick) """
    # * Variable Length Values 
    # ** http://www.ccarh.org/courses/253/handout/vlv/
    byte = get_bytes(ptr)
    bin_str = hex2bin(byte)
    if bin_str[0]=="0":
        pass
    else:
        bin_str = bin_str[1:]
        ptr+=1
        tmp_str = hex2bin(get_bytes(ptr))
        while tmp_str[0]!="0":
            bin_str+=tmp_str[1:]
            ptr+=1
            tmp_str = hex2bin(get_bytes(ptr))
        bin_str+=tmp_str[1:]
    dt = bin2dec(bin_str)
    ptr+=1
    if info_level>=3:
        print(f"dt: {dt}")
    return ptr, dt


def read_event(ptr, abs_t, info_level=1):
    """ return ptr, (event vars) """
    global uspqn_L, trk_cnt # , NUME, DENO
    byte = get_bytes(ptr)

    if byte == "ff":
    # Meta Event
    # * Standard MIDI file format, updated
    # ** http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BM3_1
        ptr += 1
        byte = get_bytes(ptr)

        if byte in ["03","04"]:
            txt_len = hex2dec(get_bytes(ptr+1))
            ptr+=2
            txt_name = get_bytes(ptr,ptr+txt_len)
            if info_level>=2:
                if byte=="03":
                    prefix = "Track name:"
                else:
                    prefix = "Instrument name:"
                # print(prefix, bytes.fromhex(txt_name).decode("windows-1252"))
                print(prefix, bytes.fromhex(txt_name).decode())
            ptr+=txt_len
            return ptr, txt_name

        elif byte=="2f":
            if get_bytes(ptr+1) != "00":
                print("x Invalid end notation!")
                return ptr, False
            if info_level>=2:
                print("=== End of track ===")
            ptr+=2
            trk_cnt += 1
            return ptr, "EOT"

        elif byte=="51":
        # Set Tempo: FF 51 03 tttttt
        # (us per MIDI quarter-note)
            if get_bytes(ptr+1) != "03":
                print("x Invalid set tempo byte length!")
                return ptr, False
            ptr+=2
            uspqn_L.append([abs_t, hex2dec(get_bytes(ptr,ptr+3))])
            if info_level>=2:
                print(f"USPQN: {uspqn_L[-1]} (us per quarter-note)")
            ptr+=3
            return ptr, uspqn_L

        elif byte=="58":
        # Time Signature: FF 58 04 nn dd cc bb
        #   nn: numerator
        #   dd: denominator (2**dd)
        #   cc: num of MIDI clocks per metronome click
        #   bb: num of notated 32nd-notes in a MIDI quarter-note (24 MIDI clocks)
            if get_bytes(ptr+1) != "04":
                print("x Invalid time signature byte length!")
                return ptr, False
            ptr+=2
            nn = hex2dec(get_bytes(ptr))
            dd = 2**hex2dec(get_bytes(ptr+1))
            cc = hex2dec(get_bytes(ptr+2))
            bb = hex2dec(get_bytes(ptr+3))
            if info_level>=2:
                print(f"  nn:{nn}, dd:{dd}, cc:{cc}, bb:{bb}")
            ptr+=4
            # NUME,DENO = nn, dd
            return ptr,(nn,dd,cc,bb)

        elif byte=="59":
        # Key Signature: FF 59 02 sf mi 
        #   sf = -7:  7 flats
        #      = -1:  1 flat
        #      =  0:  key of C
        #      =  1:  1 sharp
        #      =  7:  7 sharps
        #   mi =  0:  major key
        #      =  1:  minor key
            if get_bytes(ptr+1) != "02":
                print("x Invalid key signature byte length!")
                return ptr, False
            ptr+=2
            sf = hex2dec(get_bytes(ptr),signed=True)
            mi = hex2dec(get_bytes(ptr+1),signed=True)
            if info_level>=2:
                print(f"  sf:{sf}, mi:{mi}")
            ptr+=2
            return ptr, (sf,mi)

        else:
            color_print(f"x Unknown Meta-Event bytes: 0x{byte}", level="error")
            return ptr, False

    elif byte=="4d":
        if get_bytes(ptr+1)=="54":
            ptr+=2
            if get_bytes(ptr,ptr+2)=="726b":
                if info_level>=2:
                    color_print("\n=== MTrk ===", level="info")
                ptr+=2
                mtrk_chk_len = hex2dec(get_bytes(ptr,ptr+4))
                if info_level>=2:
                    print(f"MTrk chunk length: {mtrk_chk_len} (bytes)")
                ptr+=4
                return ptr, mtrk_chk_len
            else:
                color_print(f"x Unknown bytes {get_bytes(ptr)} after 4d54 at ptr {ptr}!", level="error")
                return ptr, False

    elif byte[0] in "89":
        # * MIDI Event Table
        # ** http://www33146ue.sakura.ne.jp/staff/iz/formats/midi-event.html
        # * Standard MIDI file format, updated 
        # ** http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BMA1_1
        if byte[0] == "8":
            switch = "OFF"
        else:
            switch = "ON"
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            pit_hex = get_bytes(ptr+1)
            pit = hex2dec(pit_hex)
            velocity = hex2dec(get_bytes(ptr+2))
            if info_level>=3:
                print(f"  Track {trk_cnt} Chan {chan_num} note {pit:<3} {switch:<3}  vel: {velocity:<3}")
            ptr+=3
            return ptr, (switch,pit,trk_cnt,chan_num,velocity)
        else:
            print(f"x Invalid chan num {byte[1]} of note {switch}!")
            return ptr, False

    elif byte[0]=="b":
        # * MIDI Control Table 
        # ** http://www33146ue.sakura.ne.jp/staff/iz/formats/midi-cntl.html
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            byte = get_bytes(ptr+1)
            mode_num = hex2dec(byte)
            # print("* Chan {} control mode change to 0x{}".format(chan_num,get_bytes(ptr+1,ptr+3)))
            byte = get_bytes(ptr+1)
            if byte == "07":
                if info_level>=3:
                    print(f"* Main Volume: {hex2dec(get_bytes(ptr+2))}")
            elif byte == "40":
                byte = get_bytes(ptr+2)
                if hex2dec(byte)==0:
                    if info_level>=3:
                        print("* Damper pedal OFF!")
                elif hex2dec(byte)==127:
                    if info_level>=3:
                        print("* Damper pedal ON!")
                else:
                    if info_level>=3:
                        print(f"* Damper pedal control mode {byte}!")
            elif 8<=hex2dec(byte)<=31:
                if info_level>=3:
                    print(f"* Continuous controller #{hex2dec(byte)}: {get_bytes(ptr+2)}")
            else:
                if info_level>=3:
                    print(f"* Chan {chan_num} control mode change to 0x{get_bytes(ptr+1,ptr+3)}")
            # ignore control commands (3 bytes)
            ptr+=3
            return ptr, (chan_num, mode_num)
        else:
            color_print(f"x Invalid chan num {byte[1]} of control!", level="error")
            return ptr, False

    elif byte[0]=="c":
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            inst_num = hex2dec(get_bytes(ptr+1))
            if info_level>=2:
                print(f"Chan {chan_num} program change to instrument {inst_num}")
            ptr+=2
            chan_inst_L.append([chan_num,inst_num])
            return ptr,(chan_num,inst_num)
        else:
            color_print("x Invalid chan num to change instrument!", level="error")
            return ptr, False
    else:
        row, col = ptr2rc(ptr)
        color_print(f"x Unknown bytes {byte.upper()} at ptr {ptr}: row {row:0>2} col {col:0>2}!", level="error")
        return ptr, False

active_note_L = []
played_note_L = []

def insert_note(abs_t,res):
    # played_note: start (tick), dura (tick), pit, trk_cnt, chan_num, vel
    # (switch,pit,trk_cnt,chan_num,velocity)
    global active_note_L, played_note_L
    pit, trk_cnt, chan_num, vel = res[1:5]
    if res[0] == "ON":
    # on_note: start (tick), pit, trk_cnt, chan_num, vel
        active_note_L.append([abs_t, pit, trk_cnt, chan_num,vel])
    elif res[0] == "OFF":
    # off_note: end (tick), pit, trk_cnt, chan_num, vel
        for idx,note in enumerate(active_note_L):
            if pit == note[1]:
                dura = abs_t - note[0]
                active_note_L[idx].insert(1,dura)
                played_note_L.append(active_note_L.pop(idx))
                break

def convert_note_time(uspqn_L,note_L):
    """  return list of [start_sec, dura_sec, pit, trk_cnt, chan_num, vel]"""

    uspqn_ptr = 0
    dt,uspqn = uspqn_L[uspqn_ptr][0:2]
    new_note_L = [""] * len(note_L)

    uspqn_mark = []
    uspqn_mark.append([0,0])
    uspqn_mark.append([dt,uspqn])

    for note_idx,note in enumerate(note_L):
        start_tick, dura_tick = note[0], note[1]

        if uspqn_ptr+1>= len(uspqn_L):
            pass
        else:
            if start_tick<uspqn_L[uspqn_ptr+1][0]:
                pass
            else:
                uspqn_ptr += 1
                dt,uspqn = uspqn_L[uspqn_ptr][0:2]
                uspqn_mark.append([start_tick,uspqn])
                # print("uspqn_mark: ",uspqn_mark)

        start_sec = 0
        for i in range(len(uspqn_mark)-1):
            start_sec += (uspqn_mark[i+1][0] - uspqn_mark[i][0]) * uspqn_mark[i][1] / TPQN / 1e6
        start_sec += (start_tick - uspqn_mark[-1][0]) * uspqn_mark[-1][1] / TPQN / 1e6
        start_sec = round(start_sec,3)
        dura_sec = dura_tick * uspqn_mark[-1][1] / TPQN / 1e6
        dura_sec = round(dura_sec,3)
        new_note_L[note_idx] = [start_sec,dura_sec,note[2],note[3],note[4],note[5]]

    return new_note_L


def read_mthd(info_level=2):
    global TPQN
    ptr = 0
    if get_bytes(ptr,ptr+4) == "4d546864":
        if info_level>=2:
            color_print("\n=== MThd ===", level="info")
    else:
        print("x Cannot parse MThd!")
        return ptr, False

    ptr+=4
    mthd_chk_len = hex2dec(get_bytes(ptr,ptr+4))
    if info_level>=2:
        print(f"MThd chunk length: {mthd_chk_len} (bytes)")

    ptr+=4
    trk_fmt = hex2dec(get_bytes(ptr,ptr+2))
    if info_level>=2:
        print(f"Track Format: {trk_fmt}")

    ptr+=2
    trk_cnt = hex2dec(get_bytes(ptr,ptr+2))
    if info_level>=2:
        print(f"Track Number: {trk_cnt}")

    ptr+=2
    TPQN = hex2dec(get_bytes(ptr,ptr+2))
    if info_level>=2:
        print(f"TPQN: {TPQN} (ticks per quarter-note)")

    ptr+=2
    return ptr, True

def read_mtrk(ptr,info_level):
    ptr, res = read_event(ptr,0,info_level)
    abs_t = 0
    while res != False:
        ptr, dt = read_delta_time(ptr,info_level)
        abs_t += dt
        ptr, res = read_event(ptr,abs_t,info_level)

        if res == "EOT":
            if get_bytes(ptr) == "":
                if info_level>=2:
                    print("\n>>> End of file <<<\n")
                if info_level>=0:
                    print("+++ MIDI processing finished +++\n")
                return ptr, "EOF"
            else:
                return ptr, "EOT"
        elif type(res)==tuple:
            if res[0] in ["ON","OFF"]:
                insert_note(abs_t,res)
        else:
            pass

def process_midi(filename, info_level=1):
    # info_level: 0: None | 1: warnig | 2: info | 3: details
    global bytes_L, played_note_L
    # with open("abc.mid","rb") as rf:
    with open(filename,"rb") as rf:
        # Note: py2:ord(b) || py3:b
        bytes_L = [f"{b:02x}" for b in rf.read()]

    ptr, res = read_mthd(info_level)
    print(ptr, res)
    while res != "EOF":
        ptr,res = read_mtrk(ptr, info_level)
    played_note_L = sorted(played_note_L, key=lambda l:l[0])
    # for played_note in played_note_L:
    #     print(played_note)
    # print(TPQN, USPQN, NUME, DENO, chan_inst_L)

    cvt_sec_note_L = convert_note_time(uspqn_L,played_note_L)

    # print(TPQN, uspqn_L,"\n")

    # for note,cvt_sec_note in zip(played_note_L,cvt_sec_note_L):
    #     print(note[0],note[1],note[-2])
    #     print("- ",cvt_sec_note[0],cvt_sec_note[1],cvt_sec_note[-2])
    #     print("- ",sec2frm(cvt_sec_note[0]),sec2frm(cvt_sec_note[1]),cvt_sec_note[-2])


    return cvt_sec_note_L

# Table of MIDI Note Numbers
# ---|-------------------------------------------------
# Oct|                  Note Numbers
# ---|-------------------------------------------------
#    |   C  C#   D  D#   E   F  F#   G  G#   A  A#   B 
# ---|-------------------------------------------------
# -1 |   0   1   2   3   4   5   6   7   8   9  10  11 
#  0 |  12  13  14  15  16  17  18  19  20  21  22  23 
#  1 |  24  25  26  27  28  29  30  31  32  33  34  35 
#  2 |  36  37  38  39  40  41  42  43  44  45  46  47 
#  3 |  48  49  50  51  52  53  54  55  56  57  58  59 
#  4 |  60  61  62  63  64  65  66  67  68  69  70  71 
#  5 |  72  73  74  75  76  77  78  79  80  81  82  83 
#  6 |  84  85  86  87  88  89  90  91  92  93  94  95 
#  7 |  96  97  98  99 100 101 102 103 104 105 106 107 
#  8 | 108 109 110 111 112 113 114 115 116 117 118 119 
#  9 | 120 121 122 123 124 125 126 127                
# ---|-------------------------------------------------

# Middle C = C4 (60, 0x3c)
# C4 is 40th key on 88-key piano keyboards
# 88-key range: A0-C8 | 21-108 | 0x15-0x80

if __name__ == '__main__':
    os.system("clear")
    filename = "passionate-duelist.mid"
    # filename = "secret-fast.mid"
    played_note_L = process_midi("E:/musix/mids/"+filename, info_level=2)
    
    # for note in played_note_L:
    #     print(note)
    # print(uspqn_L)
    # played_note: start (tick), dura (tick), chan_num, pit, vel
    # new_note_L = convert_note_time(uspqn_L,played_note_L)
    # print(new_note_L)
    # for played_note, new_note in zip(played_note_L, new_note_L):
    #     print(played_note,new_note)

