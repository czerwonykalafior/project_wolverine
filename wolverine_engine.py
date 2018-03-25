from lxml import html, etree

import pandas as pd
import requests

# CONF:
ONLINE = False


def get_all_parents(html_element):

    if html_element is None:
        return []

    ancestor = html_element.getparent()
    return [html_element] + get_all_parents(ancestor)


def common_elements(list_1, list_2):
    common_el = []

    for item in list_1:
        if item in list_2:
            common_el.append(item)

    return common_el


def offline_web_test(file_path):
    with open(file_path, 'r') as raw_html:
        html_sample = raw_html.read()
        return html_sample


def find_selectors(url, expected_values_csv):

    # gGt expected fields and values from csv input
    expected_values = pd.read_csv(expected_values_csv, sep='|')
    fields = list(expected_values.columns.values)

    # Init dict with results
    field_selectors = {k: '' for k in fields}
    # print(field_selectors)

    # Get the HTML - Online / Offline testing
    if ONLINE:
        page = requests.get(url).content
    else:
        page = offline_web_test('sample_html.html')
    root = html.fromstring(page)

    parser = etree.HTMLParser()
    tree = etree.HTML(page)

    field_html_el = tree.xpath("//*[@class='filters']")

    print(field_html_el)

    print(tree.find(".//div"))

    # Get selector for each filed
    for filed in expected_values:
        for exp_val in expected_values[filed]:
            print("\nGetting the element: ", filed, '=', exp_val)

            # This is only first element. For case when there are more, additional logic will be crated
            field_html_el = root.xpath("//*[text()='"+str(exp_val)+"']")[0]
            print(field_html_el)



    item_path = root.xpath("//*[text()='San Remo']")

    it1 = get_all_parents(item_path[0])
    print("1", item_path[0], item_path[0].tag, item_path[0].items())
    print(it1)

    it2 = get_all_parents(item_path[1])
    print("2", item_path[1], item_path[1].tag, item_path[1].items())
    print(it2)

    common_parents = (common_elements(it1, it2))
    print("Common parents:", common_parents)

    return field_selectors


if __name__ == '__main__':



    location_url = 'https://www.patek.com/en/retail-service/authorized-retailers'
    expected_values_input = 'sample_expected_data.csv'

    r = find_selectors(location_url, expected_values_input)
    # print('\nSelectors: ', r)


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
#           SOLUTION:
#
