# nec-dci-porjector-control-api
Example python command line tools to control NEC NC class (DCI) Projectors

This repo contains example Python code for controlling  NEC DCI class projectors (Listed below)

Thexe command are based on the API document **"ControlCommandsForCinemaPJS2_rev12.00.pdf"**

I keep this for my own reference but also hope others will be encouraged to start writing their own code to automate complex (cinema) system.

Its a lot of fun.

## Projects API targets

- NC3240S-A
- NC3200S ( Including NC3200S-A(+) )
- NC2000C ( Including NC2000C-A(+) )
- NC1200C ( Including NC1200C+ )
- NC900C-A ( Including NC900C-A+ )
- NC1040L-A ( Including NC1040L-A+ )
- NC1440L-A ( Including NC1440L-A+ )
- NC1100L-A(Including NC1100L-A+)
- NC1201L-A (Including NC1201L-A+)
- NC1101L-A (Including NC1101L-A+)
- NC1205L-A+
- NC1000C (Including NC1000C+)
- NC1001C+
- NC1005C+
- NC1700L (Including NC1700L+)
- NC3541L (Including NC3541L+)
- NC2041L (Including NC2041L+)
- NC2001L+ (Including NC2005L+)
- NC2601L+
- NP-02HD (Including NP-02HD+)
- NC2402ML (Including NC2402ML+)
- NC2002ML (Including NC2002ML+)
- NC1802ML (Including NC1802ML+)
- NC1402L (Including NC1402L+)
- NC1202L (Including NC1202L+)

## How to use

The command is found here. "<code>command/nec_cmd.py</code>" And required python3 is installed.  Run the command without arguments to get help on how to use the tool.

## Supported commands

Following is a list of implemented commands

- power_status
- power_on
- power_off
- version_data_request
- input_switch_change
- picture_mute_on
- picture_mute_off
- dowser_open
- dowser_close
- lamp_info_request2
- input_status_request
- mute_status_request
- lamp_on
- lamp_off
- lamp_mode

## Example

Some examples:

    prompt> nec_cmd.py -ip 192.168.1.101 power_status

Have fun coding.<br/>
James
