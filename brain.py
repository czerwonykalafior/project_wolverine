import pprint
import re

import pandas
import requests
from lxml import html, etree

# CONF:
ONLINE = True


def csv_to_dic(csv_file_path):
    """Read CSV and map it to dictionary

    Args:
        csv_file_path (str): Path to a file with sample data in csv format

    Returns: Dictionary with key : list where key=field name e.g city; list= sample values for this field e.g. Lausanne

    """
    sample_data_csv = pandas.read_csv(csv_file_path, sep='|')
    fields = list(sample_data_csv.columns.values)
    return {filed: sample_data_csv[filed].values.tolist() for filed in fields}


def read_html(file_path):
    with open(file_path, encoding="utf8") as raw_html:
        html_sample = raw_html.read()
        return html_sample


def find_selectors(html_with_loc, wanted_values):
    """Take provided sample data. Find it on a given url. Find common selector across one filed.

    E.g: city = [Lausanne, Nicosia, Limassol]
    Find each city. Check what are the attributes in it's html tag. Take common part. Repeat for the next field.

    Args:
        html_with_loc (lxml.html.HtmlElement): URL address that contains locations from sample data.
        wanted_values (dict): sample data, sample values for each filed

    Returns:
        dict: with selectors for each field

    """

    # Init
    selectors = {k: '' for k in wanted_values.keys()}
    selector_set = []

    # Loop over each field in each location
    for filed in wanted_values:
        print('Looking for a cure...')
        print('field = {}'.format(filed))
        for wanted_value in wanted_values[filed]:
            print('value = {}'.format(wanted_value))

            # Get tag equals to wanted value
            html_elem = html_with_loc.xpath('//*[text()="' + str(wanted_value) + '"]')[0]
            html_elem_s = etree.tostring(html_elem).decode('utf-8')

            # Get all tag attributes
            html_attr = re.findall('\s(.*?=".*?")', html_elem_s)

            # Get selector
            if len(selector_set) == 0:
                # for the first location's filed
                selector_set = html_attr
            else:
                # for next location, get intersection of previous selectors and current
                selector_set = list(set(selector_set) & set(html_attr))

        print('CURE FOUND: Selector for "{}" = {}\n'.format(filed, selector_set))
        selectors[filed] = selector_set
    return selectors


if __name__ == "__main__":

    source_url = 'https://www.patek.com/en/retail-service/authorized-retailers'
    sample_html_path = 'sample_html.html'
    sample_csv_path = 'sample_data.csv'

    sample_data_dict = csv_to_dic(sample_csv_path)

    # Get the HTML - Online / Offline testing
    if ONLINE:
        page = requests.get(source_url).content
    else:
        page = read_html(sample_html_path)
    html_tree = html.fromstring(page)


    print('\nTarget website:', source_url)

    print('\nSAMPLE DATA:')
    pprint.pprint(sample_data_dict)

    print('\nHealing process initiated ... \n')

    result = find_selectors(html_tree, sample_data_dict)

    pprint.pprint(result)


# TODO: Selector for whole list
#       Get The Lowest Common Ancestor (LCA) of all items from expected values and get a selector for it.
#
# TODO: Selector for one item
#       Get LCA of all fields in each item and get a selector for it.
#       CASE_1:
#           Items's values could be ALSO found in not the "item node",
#           than there will be more than one LCA for given item's values.
#           SOLUTION:
#           Real LCA will be the shortest path from given node.
# TODO: Selectors for each filed
#       Get the selector for each value in the item.
#       CASE_1:
#           The same value in different item OR/AND somewhere else in html.
#           SOLUTION: ...
