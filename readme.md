# Project Wolverine

Find selectors based on given sample.
Robots could heal itself using data already scraped.


Current state:

Locations on flat list. Each loc has some common attribute. 
Ideal state works, everything else fails.
 
Use to open dom_graph.graphml :        
https://www.yworks.com/yed-live/


TODO: Selector for whole list
      Get The Lowest Common Ancestor (LCA) of all items from expected values and get a selector for it.

TODO: Selector for one item
      Get LCA of all fields in each item and get a selector for it.
      CASE_1:
          Items's values could be ALSO found in not the "item node",
          than there will be more than one LCA for given item's values.
          SOLUTION:
          Real LCA will be the shortest path from given node.
TODO: Selectors for each filed
      Get the selector for each value in the item.
      CASE_2:
          The same value in different item OR/AND somewhere else in html.
          SOLUTION_2:
