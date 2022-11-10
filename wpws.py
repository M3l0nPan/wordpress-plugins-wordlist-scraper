#!/usr/bin/dev python3

import argparse
from bs4 import BeautifulSoup
import pathlib
import re
from urllib.request import Request as request
from urllib.request import urlopen

DEFAULT_URL_WORDPRESS_PLUGIN_LIST = "http://plugins.svn.wordpress.org/"
DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:199.0) Gecko/21000101 Firefox/199.0"


def argument_parser():
    """Parse argument provided to the script."""
    parser = argparse.ArgumentParser(description='WordPress Plugin Wordlist Scraper')

    parser.add_argument("-u", "--url",
                        type=str,
                        help="""WordPress url listing all plugins
                        (default: http://plugins.svn.wordpress.org/)""")

    parser.add_argument("--user_agent",
                        type=str,
                        help="""Change user-agent used by the script_args
                        (default: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0)""")

    parser.add_argument("-f", "--file",
                        type=pathlib.Path,
                        help="File where will be saved the WordPress wordlist")

    script_args = parser.parse_args()

    return script_args


def scrape_plugins_list(script_args):
    """Scrape from WordPress website or from given URL a plugin list."""
    if not script_args.url:
        url = DEFAULT_URL_WORDPRESS_PLUGIN_LIST
    else:
        url = script_args.url

    if not script_args.user_agent:
        user_agent = DEFAULT_USER_AGENT
    else:
        user_agent = script_args.user_agent

    header = {'User-Agent': user_agent}

    response = request(url, headers=header)

    return urlopen(response)


def parse_plugin_list(response):
    """Parse plugin list from scrapped information.

    Customization is required if plugins are scrapped from a custom source.
    """
    plugins_list = []

    response = BeautifulSoup(response, "lxml").get_text()

    for line in response.splitlines():
        match_plugin = re.search(r'^([^:]+?)/$', line)
        if match_plugin:
            plugin = match_plugin.group(1)

            # Sanitize
            plugin = plugin.replace('\u200b', '')

            plugins_list.append(plugin)

    return plugins_list


def write_plugins_to_file(plugins_list, file_path):
    """Write plugins list in a file."""
    with open(file_path, 'w') as file:
        for plugin in plugins_list:
            file.write("%s\n" % plugin)


def main():
    """Run main program."""
    script_args = argument_parser()

    response = scrape_plugins_list(script_args)

    plugins_list = parse_plugin_list(response)

    if script_args.file:
        write_plugins_to_file(plugins_list, script_args.file)
    else:
        print('\n'.join(plugins_list))


if __name__ == "__main__":
    main()
