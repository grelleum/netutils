"""Test for the IP functions."""
import pytest

from netutils import ip

IP_TO_HEX = [
    {
        "sent": {"ip": "10.1.1.1"},
        "received": "a010101",
    },
    {
        "sent": {"ip": "2001:db8:3333:4444:5555:6666:7777:8888"},
        "received": "20010db8333344445555666677778888",
    },
]

IP_ADDITION = [
    {
        "sent": {"ip": "10.1.1.1", "val": 10},
        "received": "10.1.1.11",
    },
    {
        "sent": {"ip": "2001:db8:3333:4444:5555:6666:7777:8888", "val": 10},
        "received": "2001:db8:3333:4444:5555:6666:7777:8892",
    },
]

IP_FIRST_USABLE = [
    {
        "sent": {"ip_network": "10.1.1.0/24"},
        "received": "10.1.1.1",
    },
    {
        "sent": {"ip_network": "10.1.1.0/255.255.255.0"},
        "received": "10.1.1.1",
    },
    {
        "sent": {"ip_network": "10.1.1.0/31"},
        "received": "10.1.1.0",
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/64"},
        "received": "2001:db8:3c4d:15::1",
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/127"},
        "received": "2001:db8:3c4d:15::",
    },
]

IP_TO_BIN = [
    {
        "sent": {
            "ip": "10.1.1.1",
        },
        "received": "1010000000010000000100000001",
    },
    {
        "sent": {
            "ip": "2001:db8:3333:4444:5555:6666:7777:8888",
        },
        "received": "100000000000010000110110111000001100110011001101000100010001000101010101010101011001100110011001110111011101111000100010001000",
    },
]

IP_SUBTRACT = [
    {
        "sent": {"ip": "10.1.1.1", "val": 10},
        "received": "10.1.0.247",
    },
    {
        "sent": {"ip": "2001:db8:3333:4444:5555:6666:7777:8888", "val": 10},
        "received": "2001:db8:3333:4444:5555:6666:7777:887e",
    },
]

IS_IP = [
    {
        "sent": {
            "ip": "10.1.1.1",
        },
        "received": True,
    },
    {
        "sent": {
            "ip": "255.255.255.255",
        },
        "received": True,
    },
    {
        "sent": {
            "ip": "2001:db8:3333:4444:5555:6666:7777:8888",
        },
        "received": True,
    },
    {
        "sent": {
            "ip": "NOT AN IP",
        },
        "received": False,
    },
    {
        "sent": {
            "ip": "255.255.255.256",
        },
        "received": False,
    },
]

GET_BROADCAST_ADDRESS = [
    {
        "sent": {"ip_network": "10.1.1.0/24"},
        "received": "10.1.1.255",
    },
    {
        "sent": {"ip_network": "10.1.1.0/255.255.255.0"},
        "received": "10.1.1.255",
    },
    {
        "sent": {"ip_network": "10.1.1.0/31"},
        "received": "10.1.1.1",
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/64"},
        "received": "2001:db8:3c4d:15:ffff:ffff:ffff:ffff",
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/127"},
        "received": "2001:db8:3c4d:15::1",
    },
]

GET_ALL_HOST = [
    {
        "sent": {"ip_network": "10.1.1.0/30"},
        "received": ["10.1.1.1", "10.1.1.2"],
    },
    {
        "sent": {"ip_network": "10.1.1.0/255.255.255.252"},
        "received": ["10.1.1.1", "10.1.1.2"],
    },
    {
        "sent": {"ip_network": "10.1.1.0/31"},
        "received": ["10.1.1.0", "10.1.1.1"],
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/126"},
        "received": ["2001:db8:3c4d:15::1", "2001:db8:3c4d:15::2", "2001:db8:3c4d:15::3"],
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/127"},
        "received": ["2001:db8:3c4d:15::", "2001:db8:3c4d:15::1"],
    },
]

USABLE_RANGE = [
    {
        "sent": {"ip_network": "10.1.1.0/24"},
        "received": "10.1.1.1 - 10.1.1.254",
    },
    {
        "sent": {"ip_network": "10.1.1.0/255.255.255.0"},
        "received": "10.1.1.1 - 10.1.1.254",
    },
    {
        "sent": {"ip_network": "10.1.1.0/31"},
        "received": "10.1.1.0 - 10.1.1.1",
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/64"},
        "received": "2001:db8:3c4d:15::1 - 2001:db8:3c4d:15:ffff:ffff:ffff:fffe",
    },
    {
        "sent": {"ip_network": "2001:db8:3c4d:15::/127"},
        "received": "2001:db8:3c4d:15:: - 2001:db8:3c4d:15::1",
    },
]

IS_NETMASK = [
    {"sent": {"netmask": "255.255.255.0"}, "received": True},
    {"sent": {"netmask": "255.192.0.0"}, "received": True},
    {"sent": {"netmask": "255.266.0.0"}, "received": False},
    {"sent": {"netmask": "255.0.128.0"}, "received": False},
    {"sent": {"netmask": "44"}, "received": False},
    {"sent": {"netmask": "mynetmask"}, "received": False},
    {"sent": {"netmask": "dead:beef:cafe::"}, "received": False},
    {"sent": {"netmask": "ff00::"}, "received": True},
    {"sent": {"netmask": "ffff:ffff:ffff:ffff:ffff::"}, "received": True},
]

NETMASK_CIDR = [
    {"sent": {"netmask": "255.255.255.0"}, "received": 24},
    {"sent": {"netmask": "255.192.0.0"}, "received": 10},
    {"sent": {"netmask": "255.255.255.252"}, "received": 30},
    {"sent": {"netmask": "ff00::"}, "received": 8},
    {"sent": {"netmask": "ffff:ffff:ffff:ffff:ffff::"}, "received": 80},
]

CIDR_NETMASK = [
    {"sent": {"cidr": 24}, "received": "255.255.255.0"},
    {"sent": {"cidr": 28}, "received": "255.255.255.240"},
    {"sent": {"cidr": 10}, "received": "255.192.0.0"},
    {"sent": {"cidr": 17}, "received": "255.255.128.0"},
]

CIDR_NETMASK6 = [
    {"sent": {"cidr": 8}, "received": "ff00::"},
    {"sent": {"cidr": 80}, "received": "ffff:ffff:ffff:ffff:ffff::"},
]

COUNT_BITS = [
    {"sent": 0, "received": 0},
    {"sent": 234, "received": 5},
    {"sent": 255, "received": 8},
    {"sent": 0xFFFFFFFFFFFFFFFF, "received": 64},
]


@pytest.mark.parametrize("data", IP_TO_HEX)
def test_ip_to_hex(data):
    assert ip.ip_to_hex(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", IP_ADDITION)
def test_ip_addition(data):
    assert ip.ip_addition(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", IP_TO_BIN)
def test_ip_to_bin(data):
    assert ip.ip_to_bin(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", IP_SUBTRACT)
def test_ip_subtract(data):
    assert ip.ip_subtract(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", IS_IP)
def test_is_ip(data):
    assert ip.is_ip(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", GET_ALL_HOST)
def test_get_all_host(data):
    assert list(ip.get_all_host(**data["sent"])) == data["received"]


@pytest.mark.parametrize("data", GET_BROADCAST_ADDRESS)
def test_get_broadcast_address(data):
    assert ip.get_broadcast_address(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", IP_FIRST_USABLE)
def test_get_first_usable(data):
    assert ip.get_first_usable(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", USABLE_RANGE)
def test_get_usable_range(data):
    assert ip.get_usable_range(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", IS_NETMASK)
def test_is_netmask(data):
    assert ip.is_netmask(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", NETMASK_CIDR)
def test_netmask_to_cidr(data):
    assert ip.netmask_to_cidr(**data["sent"]) == data["received"]


def test_netmask_to_cidr_fail():
    with pytest.raises(ValueError, match=r"Subnet mask is not valid"):
        data = {"netmask": "255.266.0.0"}
        ip.netmask_to_cidr(**data)


@pytest.mark.parametrize("data", CIDR_NETMASK)
def test_cidr_to_netmask(data):
    assert ip.cidr_to_netmask(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", CIDR_NETMASK6)
def test_cidr_to_netmaskv6(data):
    assert ip.cidr_to_netmaskv6(**data["sent"]) == data["received"]


def test_cidr_to_netmask_fail():
    with pytest.raises(ValueError, match=r"Parameter must be an integer between 0 and 32."):
        data = {"cidr": 37}
        ip.cidr_to_netmask(**data)
