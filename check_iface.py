#!/usr/bin/python3
# GPL v3+

import argparse
import netifaces
import psutil
import sys

NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3

nagios_states = {
        NAGIOS_OK: "OK",
        NAGIOS_WARNING: "WARNING",
        NAGIOS_CRITICAL: "CRITICAL",
        NAGIOS_UNKNOWN: "UNKNOWN"
        }

nagios_state = NAGIOS_UNKNOWN

def check_duplex(value):
    allowed_duplex = [ "full", "half" ]
    if value not in allowed_duplex:
        raise argparse.ArgumentTypeError("must be one of: %s" % ", ".join(allowed_duplex))

    if value == "full":
        return psutil._common.NicDuplex.NIC_DUPLEX_FULL
    elif value == "half":
        return psutil._common.NicDuplex.NIC_DUPLEX_HALF

def get_default_iface():
    try:
        return netifaces.gateways()['default'][netifaces.AF_INET][1]
    except IndexError as e:
        return "eth0"

parser = argparse.ArgumentParser()
parser.add_argument('--speed', '-s', action="store", type=int, default=1000, help='expected minimal interface speed')
parser.add_argument('--duplex', '-d', action="store", type=check_duplex, default="full", help='expected duplex')
parser.add_argument('--mtu', '-m', action="store", type=int, default=1500, help='expected minimal MTU')
parser.add_argument('--interface', '-i', action="store", type=str, help='interface name')
parser.add_argument("--verbose", help="Verbose mode.", action="store_true")

args = parser.parse_args()

try:

    if not args.interface:
        args.interface = get_default_iface()

    ifs = psutil.net_if_stats()
    if args.interface not in ifs:
        nagios_state = NAGIOS_CRITICAL
        print("Network interface `{iface}' not found".format(iface=args.interface))
        sys.exit(nagios_state)

    msgs = []

    iface = ifs[args.interface]

    nagios_state = NAGIOS_OK

    if iface.duplex != psutil._common.NicDuplex.NIC_DUPLEX_UNKNOWN and iface.duplex < args.duplex:
        nagios_state = max(nagios_state, NAGIOS_CRITICAL)
        msgs.append("duplex={duplex} (CRITICAL, expected: {duplex_expected})".format(duplex=str(iface.duplex), duplex_expected=args.duplex))
    else:
        msgs.append("duplex={duplex} (OK)".format(duplex=str(iface.duplex)))

    if iface.speed != 0 and iface.speed < args.speed:
        nagios_state = max(nagios_state, NAGIOS_CRITICAL)
        msgs.append("speed={speed} (CRITICAL, expected min: {speed_expected})".format(speed=iface.speed, speed_expected=args.speed))
    else:
        msgs.append("speed={speed} (OK)".format(speed=iface.speed))

    if iface.mtu != 0 and iface.mtu != args.mtu:
        nagios_state = max(nagios_state, NAGIOS_CRITICAL)
        msgs.append("mtu={mtu} (CRITICAL, expected min: {mtu_expected})".format(mtu=iface.mtu, mtu_expected=args.mtu))
    else:
        msgs.append("mtu={mtu} (OK)".format(mtu=iface.mtu))

    print("{state} - interface `{iface}': {msg}".format(state=nagios_states[nagios_state], iface=args.interface, msg=", ".join(msgs)))
except Exception as e:
    print("UNKNOWN: %{e}".format(e=e))
    nagios_state = NAGIOS_UNKNOWN
sys.exit(nagios_state)
