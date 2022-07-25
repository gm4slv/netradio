# header
preamble = "\xfe"
controller = "\xe0"

# commands/requests
set_freq_cmd = "\x05"
set_mode_cmd = "\x06"
get_freq_cmd = "\x03"
get_mode_cmd = "\x04"
get_smeter_cmd = "\x15" + "\x02"
get_swr_cmd = "\x15" + "\x12"
digi_off_cmd = "\x1a" + "\x04" + "\x00" + "\x00"

set_pre_cmd = "\x16" + "\x02"

set_pre_off = "\x00"
set_pre_on = "\x01"
set_pre_2_on = "\x02"

set_att_cmd = "\x11"
set_att_on = "\x20"
set_att_off = "\x00"

ptt_on_cmd = "\x1c" + "\x00" + "\x01"
ptt_off_cmd = "\x1c" + "\x00" + "\x00"

pwr_cmd = "\x14" + "\x0a"

# end of message
eom = "\xfd"

# controller responses
ack = "\xfb"
nak = "\xfa"

a1 = "\x5A"
n1 = "IC-R75"
cal1 = ( 25, 1, 36, 47, 31, 18, 34, 35 )

a2 = "\x5e"
# a2 = "\x01"
n2 = "IC-718"
cal2 = ( 27, 28, 58, 10, 14, 14, 35, 42 )

n3 = "AR7030"

n4 = "IC-M710"
