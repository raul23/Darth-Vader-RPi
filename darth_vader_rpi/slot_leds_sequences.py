"""Module that defines the slot LEDs sequences.

These slot LEDs are located on Darth Vader's chest control box and they light
up following a default or custom sequence.

References
----------
The default sequences of slot LEDs (ACTION and CALM) were obtained from this
`YouTube video`_.

"""

ACTION = [["top", "middle", "bottom"],
          ["top", "bottom"],
          ["top", "middle", "bottom"],
          ["top"],
          [],
          ["top", "middle", "bottom"],
          ["top"],
          ["top", "middle", "bottom"],
          ["middle", "bottom"],
          [],
          ["top", "bottom"],
          ["top", "middle", "bottom"],
          ["top", "bottom"],
          [],
          ["top"],
          []]

CALM = [["middle"],
        ["top"],
        ["middle"],
        ["top"],
        ["middle"],
        ["top"],
        [],
        ["top"],
        [],
        ["bottom"],
        []]
"""Darth Vader's physiological status.

These lists represent the sequence the 3 slot LEDs (on his chest box) should be
turned on.  Each item in the list represents a step in the sequence. Thus, in
the case of ``ACTION_MODE``, all the 3 slot LEDs will be turned on first, 
followed by the top and bottom LEDs, and so on.

An empty subsequence refers to all LEDs being turned off.

References
----------
- Where the sequences were obtained: https://youtu.be/E2J_xl2MbGU?t=333

"""
