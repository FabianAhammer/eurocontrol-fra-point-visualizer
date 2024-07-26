import itertools
import os


def svg_start() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="48"
   height="48"
   viewBox="0 0 48 48"
   version="1.1"
   id="svg1"
   inkscape:version="1.3 (0e150ed6c4, 2023-07-21)"
   sodipodi:docname="half_waypoint.svg"
   inkscape:export-filename="Desktop\waypoint_EXIDA.svg"
   inkscape:export-xdpi="96"
   inkscape:export-ydpi="96"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview1"
     pagecolor="#b8b8b8"
     bordercolor="#000000"
     borderopacity="0.25"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="false"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="px"
     inkscape:zoom="12.668997"
     inkscape:cx="5.5252995"
     inkscape:cy="28.849957"
     inkscape:window-width="2560"
     inkscape:window-height="1377"
     inkscape:window-x="1912"
     inkscape:window-y="-8"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" />
  <defs
     id="defs1">
    <linearGradient
       id="swatch17"
       inkscape:swatch="solid">
      <stop
         style="stop-color:#000000;stop-opacity:1;"
         offset="0"
         id="stop17" />
    </linearGradient>
  </defs>
   <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="matrix(3.7906854,0,0,3.7644956,3.0404125,4.4996046)"
     style="display:inline">"""


def svg_end() -> str:
    return """  </g>
</svg>
"""


def not_intermediate() -> str:
    return """<g
       id="g10"
       inkscape:label="half_waypoint_not_intermediate">
      <path
         id="rect11"
         style="display:inline;opacity:1;fill:#ffffff;fill-opacity:1;stroke:#000000;stroke-width:0.75;stroke-opacity:1"
         inkscape:label="rect11"
         d="M 1.0232976,0.54504567 H 5.0004609 V 10.378902 H 1.0232976 Z" />
    </g>"""


def intermediate() -> str:
    return """ <g
       id="g2"
       inkscape:label="intermediate"
       style="display:inline">
      <path
         id="path4"
         style="stroke-width:0.264583"
         d="m 5.110238,-1.9961915 -3.6261139,6.3084741 3.638561,-0.00709 0.00296,-5.4e-6 z"
         transform="matrix(1.7407582,0.00365943,-0.00425618,2.0246232,-3.3615543,2.8171843)"
         inkscape:label="outside" />
      <path
         id="path5"
         style="fill:#ffffff;stroke-width:0.264583"
         inkscape:transform-center-x="0.0012984433"
         inkscape:transform-center-y="-1.2998527"
         d="M 5.1331771,-1.9580764 5.1106742,-1.9970212 1.4841791,4.3121774 5.1484907,4.305135 Z"
         transform="matrix(1.1267122,0.00223704,-0.00275483,1.2376673,-0.24534633,4.5491208)"
         inkscape:label="inside" />
    </g>"""


def entry() -> str:
    return """ <g
       id="g6-6"
       inkscape:label="entry_arrow"
       transform="matrix(-1.3725781,0,0,0.7506461,19.151229,1.7935231)"
       style="display:inline">
      <path
         style="fill:#00bd16;fill-opacity:1;stroke-width:0.264721"
         d="M 5.5518754,8.2336368 H 8.5131658 V 9.0554181 L 10.011299,7.5468624 H 5.5402168 Z"
         id="path6-0"
         inkscape:label="lower_arrow" />
      <path
         style="fill:#00bd16;fill-opacity:1;stroke-width:0.264721"
         d="M 5.5518754,6.8656323 H 8.5131658 V 6.043851 L 10.011299,7.5524067 H 5.5402168 Z"
         id="path3-9"
         inkscape:label="upper_arrow" />
    </g>"""


def exitpt() -> str:
    return """<g
       id="g6"
       inkscape:label="exit_arrow"
       transform="matrix(1.3166914,0,0,0.77849566,-1.6649515,4.0126618)"
       style="display:inline">
      <path
         style="fill:#ff3c00;fill-opacity:1;stroke-width:0.264721"
         d="M 5.5518754,8.2336368 H 8.5131658 V 9.0554181 L 10.011299,7.5468624 H 5.5402168 Z"
         id="path6"
         inkscape:label="lower_arrow" />
      <path
         style="fill:#ff3c00;fill-opacity:1;stroke-width:0.264721"
         d="M 5.5518754,6.8656323 H 8.5131658 V 6.043851 L 10.011299,7.5524067 H 5.5402168 Z"
         id="path3"
         inkscape:label="upper_arrow" />
    </g>"""


def arrival() -> str:
    return """<path
       style="display:inline;fill:#0000ff;fill-opacity:1;stroke-width:0.453946"
       d="m 5.6735088,4.4220844 c 0,0 -0.00378,-1.1314499 0.053022,-1.178423 0.090707,-0.074998 0.2995313,-0.066486 0.3319718,0 0.049403,0.101249 0.2287178,0.6454287 0.4326896,0.8867797 0.074192,0.087787 1.0953534,0.3472846 1.0953534,0.3472846 0,0 -0.061989,-1.7383608 0,-1.8669211 0.056678,-0.1175476 0.5428892,-0.2070957 0.6943245,0 0.086032,0.1176517 0.9758534,2.1165565 1.080758,2.2149711 0.075046,0.070403 1.2094299,0.383453 1.2094299,0.383453 0,0 0.671357,0.2400394 0.83135,0.5679392 0.0535,0.1096437 0.06514,0.2793744 0,0.3798176 -0.09397,0.144912 -0.292957,0.1418263 -0.447326,0.1418263 -0.232916,0 -5.0523758,-1.4312314 -5.2491429,-1.6748683 -0.038657,-0.047864 -0.032435,-0.2018591 -0.032435,-0.2018591 z"
       id="path7"
       sodipodi:nodetypes="cssscssscsssscc"
       inkscape:label="arrival" />"""


def departure() -> str:
    return """ <path
       style="fill:#ff1c7f;fill-opacity:1;stroke-width:0.4642"
       d="m 6.3618334,2.7629121 c 0,0 -0.7134612,-0.7924837 -0.7017155,-0.873895 0.018763,-0.1299935 0.1757627,-0.3018555 0.2410848,-0.2827267 0.099477,0.02913 0.5715229,0.2591148 0.871255,0.2551329 0.1090226,-0.00145 1.0136135,-0.6886359 1.0136135,-0.6886359 0,0 -1.1369614,-1.16972675 -1.1726986,-1.31293125 -0.032676,-0.1309381 0.264171,-0.6079987 0.5042328,-0.5913278 0.136381,0.00947 2.038191,0.6573958 2.1761935,0.6372639 0.098722,-0.014403 1.1191771,-0.7603547 1.1191771,-0.7603547 0,0 0.638332,-0.40295645 0.960492,-0.30861725 0.107724,0.031545 0.222791,0.1409981 0.238581,0.26711055 0.02278,0.1819448 -0.123665,0.3492404 -0.23577,0.4807099 C 11.20713,-0.21699405 6.808118,2.8810133 6.5121822,2.8772516 6.4540431,2.8765135 6.3618299,2.7629162 6.3618299,2.7629162 Z"
       id="path8"
       sodipodi:nodetypes="cssscssscsssscc"
       inkscape:label="depature" />"""


chars = ["E", "X", "I", "D", "A"]

# Initialize an empty list to store all combinations
all_combinations: list[str] = []

# Loop over lengths from 1 to the length of the array
for length in range(1, len(chars) + 1):
    # Generate permutations of the current length
    permutations = itertools.permutations(chars, length)
    # Convert each permutation to a string and add to the list
    all_combinations.extend("".join(p) for p in permutations)

if not os.path.exists("output"):
    os.mkdir("output")

# Print the result
uniques = list(sorted(set(map(lambda x: "".join(sorted(x)), all_combinations))))

for unq in uniques:
    if unq == "I":
        continue
    svg = svg_start()

    if unq.__contains__("E"):
        svg += entry()

    if unq.__contains__("X"):
        svg += exitpt()

    if unq.__contains__("I"):
        svg += intermediate()

    if not unq.__contains__("I"):
        svg += not_intermediate()

    if unq.__contains__("A"):
        svg += arrival()

    if unq.__contains__("D"):
        svg += departure()
    svg += svg_end()

    with open(f"output/{unq}.svg", "w") as fw:
        fw.write(svg)
        fw.flush()

print(os.listdir("./output"))
