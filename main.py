import ipaddress
import json
import pprint
import argparse

# Not in use yet...


def sort_networks(vpc_data, remove_default_vpcs=True):
    # Filter out default VPCs
    # Make sure they are both call default AND have the default cidr range
    if remove_default_vpcs:
        vpc_data = list(filter(
            lambda x: x['vpc_name'] != 'default' or x['cidr'] != '172.31.0.0/16', vpc_data))

    for item in vpc_data:
        item['cidr'] = ipaddress.ip_network(item['cidr'])

    # Sort VPCs by cidr
    vpc_data.sort(key=lambda x: x.get('cidr'), reverse=False)

    for item in vpc_data:
        print(f"{item['account_name']} - {item['cidr']}")

# Takes a cidr range and splits it into predefined subnet layout


def split_network_small(ip_network):

    # add validation for correct network size /22

    network = ip_network

    subnets_top = list(network.subnets(2))
    subnets_public = list(subnets_top[0].subnets(1))
    subnets_data = list(subnets_top[1].subnets(1))
    subnets_private = subnets_top[2:]

    network_map = {
        'public-a': subnets_public[0],
        'public-b': subnets_public[1],
        'data-a': subnets_data[0],
        'data-b': subnets_data[1],
        'private-a': subnets_private[0],
        'private-b': subnets_private[1]
    }

    pprint.pprint(network_map)


def split_network_medium(ip_network):

    network = ip_network
    # add validation for correct network size /21

    subnets_top = list(network.subnets(2))
    subnets_public = list(subnets_top[0].subnets(2))
    subnets_data = list(subnets_top[1].subnets(2))
    subnets_private = list(subnets_top[2].subnets(1))
    for item in subnets_top[3].subnets(1):
        subnets_private.append(item)

    network_map = {
        'public-a': subnets_public[0],
        'public-b': subnets_public[1],
        'public-c': subnets_public[2],
        'public-d': subnets_public[3],
        'data-a': subnets_data[0],
        'data-b': subnets_data[1],
        'data-c': subnets_data[2],
        'data-d': subnets_data[3],
        'private-a': subnets_private[0],
        'private-b': subnets_private[1],
        'private-c': subnets_private[2],
        'private-d': subnets_private[3]
    }

    # pprint.pprint(network_map)
    print_subnets(network_map)


def print_subnets(subnet_map):
    for k, v in subnet_map.items():
        print(f"{k} - {v.network_address}/{v.prefixlen}")


def split_network(network: ipaddress.ip_network):
    if network.prefixlen == 22:
        split_network_small(network)
    elif network.prefixlen == 21:
        split_network_medium(network)
    else:
        print('cidr didnt match valid prefix length')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Split some CIDRs!!')

    parser.add_argument(
        '-c', '--cidr', help='the cidr of the vpc to break down. Must be a /21 or /22')

    args = parser.parse_args()

    split_network(ipaddress.ip_network(args.cidr))
