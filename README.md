# lack.py
- Pipe data between Python functions in the command line.  
- Create command line functions from Python scripts without modifying the scripts.  
- Automatically parse input expressions, and serialize outputs. 
- Simplify the process of reading from and writing to files.  
- Facilitate interaction with other command line tools.  
- Support for boolean flags and keyword arguments.  
- Small, single-file source (~100 lines).

### Table of Contents:
**Features:**  
[Lack.py Call Format](#lackpy-call-format)  
[Setup for Examples](#setup-for-examples)  
[Simple Function Call](#simple-function-call)  
[Boolean Flags](#boolean-flags)  
[Named Arguments](#named-arguments)  
[Piped Data](#piped-data)  
[File Input and Output](#file-input-and-output)  
[Composition with other Command Line Tools](#composition-with-other-command-line-tools)

**Other Info:**  
[Comparison with Similar Tools](#comparison-with-similar-tools)  
[Sample Output](#sample-output)

#### Lack.py Call Format:
```shell
./lack.py script.py funcName [args...]
```

#### Setup for Examples:
The script `gameOfLife.py` contains functions for running simulations of
[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life) (cellular autonomaton).  
The examples use the following aliases:
```shell
alias simulate="./lack.py gameOfLife.py simulate"
alias showCells="./lack.py gameOfLife.py showCells"
alias randomCells="./lack.py gameOfLife.py randomCells"
```
The variable `initCells` contains an array of arrays of binary digits 
(see [initCells.txt](https://github.com/averynortonsmith/lackadaisical/blob/master/initCells.txt))

#### Simple Function Call:
*python:*
```python
>>> simulate(initCells, 100)
```
*using lack.py:*
```shell
$ simulate initCells.txt 100
```
Positional Python arguments become positional command line arguments.  
If the name of a file is given as an argument, the contents of that file become the argument.  
If the given file contains a Python expression, the expression is parsed and the resulting
value becomes the argument.  
Similarly, Python expressions given as positional arguments are parsed to their values.  
*Watch out for spaces in command line expressions: `[1,2,3]` will work, `[1, 2, 3]` will cause an error.*

#### Boolean Flags:
*python:*
```python
>>> simulate(initCells, 100, showSteps=True)
```
*using lack.py:*
```shell
$ simulate initCells.txt 100 --showSteps
```
A flag of the form `--flagName` sets the keyword-argument `flagName` to the value `True`.  
For example: `--flagName` is equivalent to `flagName=True`.

#### Named Arguments:
*python:*
```python
>>> simulate(initCells, 100, showSteps=True, delay=.04)
```
*using lack.py:*
```shell
$ simulate initCells.txt 100 --showSteps delay=.04
```
Named Python arguments become named command line arguments.


#### Piped Data:
*python:*
```python
>>> print(showCells(simulate(randomCells(10, 30), 100)))
```
*using lack.py:*
```shell
$ randomCells 10 30 | simulate 100 | showCells
```
A value sent through a pipe becomes the first argument to the function.  
If the piped text contains a Python expression, the expression is parsed and its value becomes the argument.      
For example: `arg0 | foo arg1` is equivalent to `foo arg0 arg1`.

#### File Input and Output:
*python:*
```python
import ast

with open("initCells.txt", "r") as file:
    initCells = ast.literal_eval(file.read())

with open("output.txt", "w") as file:
    output = showCells(simulate(initCells, 100))
    file.write(output)
```
*using lack.py:*
```shell
$ simulate initCells.txt 100 | showCells >> output.txt
```
The file [`initCells.txt`](https://github.com/averynortonsmith/lackadaisical/blob/master/initCells.txt) 
contains a Python expression (a list of lists), which is 
parsed by the `ast.literal_eval` function before it becomes an argument.  
Piped argument strings containing Python expressions are also parsed in this way.  
For example: `simulate initCells.txt 100` is equivalent to `cat initCells.txt | simulate 100`.

#### Composition with other Command Line Tools:
*python:*
```python
import ast
import urllib.request

url = "https://averyn.scripts.mit.edu/lack/initCells.txt"
initCells = ast.literal_eval(urllib.request.urlopen(url).read().decode('utf-8'))
simulate(initCells, 100, showSteps=True, delay=.04)
```
*using lack.py:*
```shell
$ curl https://averyn.scripts.mit.edu/lack/initCells.txt | simulate 100 --showSteps delay=.04
```
Since command line functions made with lack.py always take strings as arguments and return string values,
they can be used with many existing command line tools.

#### Comparison with Similar Tools:
**google/[python-fire](https://github.com/google/python-fire)**  
- supports pip for installation
- focused on objects, rather than functions
- many options for working with classes / methods
- includes help and debugging options
- doesn't support piped data or filename arguments
- requires modification of original script (import)
- larger codebase, more complex overall

**shmuelamar/[cbox](https://github.com/shmuelamar/cbox)**  
- supports pip for installation
- support for error handling, concurrency, streams, documentation
- supports piped data (for text only)
- doesn't support filename arguments
- requires default values or type annotations for expression parsing
- requires modification of original script (import, decorators)
- larger codebase, more complex overall

**tellapart/[commandr](https://github.com/tellapart/commandr)**  
- supports pip, easy_install for installation
- automatic documentation
- supports boolean arguments, expression parsing
- doesn't support piped data or filename arguments
- requires modification of original script (import, decorators)
- larger codebase

#### Sample Output:
```shell
$ randomCells 10 30 | simulate 20 --showSteps delay=.1
```

```
iteration  1 of 20:
[                                                           ]
[                                                           ]
[                                                           ]
[            * *                                            ]
[          * *                                              ]
[            *                                 *            ]
[                                  * *                      ]
[                                    *       * * *          ]
[                                                           ]
[                                                           ]

iteration  2 of 20:
[                                                           ]
[                                                           ]
[                                                           ]
[          * * *                                            ]
[          *                                                ]
[          * *                                              ]
[                                  * *       *   *          ]
[                                  * *         *            ]
[                                              *            ]
[                                                           ]

iteration  3 of 20:
[                                                           ]
[                                                           ]
[            *                                              ]
[          * *                                              ]
[        *     *                                            ]
[          * *                                              ]
[                                  * *         *            ]
[                                  * *       * * *          ]
[                                                           ]
[                                                           ]

iteration  4 of 20:
[                                                           ]
[                                                           ]
[          * *                                              ]
[          * * *                                            ]
[        *     *                                            ]
[          * *                                              ]
[                                  * *       * * *          ]
[                                  * *       * * *          ]
[                                              *            ]
[                                                           ]

iteration  5 of 20:
[                                                           ]
[                                                           ]
[          *   *                                            ]
[        *     *                                            ]
[        *     *                                            ]
[          * *                                 *            ]
[                                  * *       *   *          ]
[                                  * *                      ]
[                                            * * *          ]
[                                                           ]

iteration  6 of 20:
[                                                           ]
[                                                           ]
[            *                                              ]
[        * *   * *                                          ]
[        *     *                                            ]
[          * *                                 *            ]
[                                  * *         *            ]
[                                  * *       *   *          ]
[                                              *            ]
[                                              *            ]

iteration  7 of 20:
[                                                           ]
[                                                           ]
[          * * *                                            ]
[        * *   * *                                          ]
[        *     * *                                          ]
[          * *                                              ]
[                                  * *       * * *          ]
[                                  * *       *   *          ]
[                                            * * *          ]
[                                                           ]

iteration  8 of 20:
[                                                           ]
[            *                                              ]
[        * *   * *                                          ]
[        *                                                  ]
[        *       *                                          ]
[          * * *                               *            ]
[                                  * *       *   *          ]
[                                  * *     *       *        ]
[                                            *   *          ]
[                                              *            ]

iteration  9 of 20:
[                                                           ]
[          * * *                                            ]
[        * * * *                                            ]
[      * *     * *                                          ]
[        *   * *                                            ]
[          * * *                               *            ]
[            *                     * *       * * *          ]
[                                  * *     * *   * *        ]
[                                            * * *          ]
[                                              *            ]

iteration  10 of 20:
[            *                                              ]
[        *     *                                            ]
[      *                                                    ]
[      *         *                                          ]
[      * *                                                  ]
[                                            * * *          ]
[          * * *                   * *     *       *        ]
[                                  * *     *       *        ]
[                                          *       *        ]
[                                            * * *          ]

iteration  11 of 20:
[                                              *            ]
[                                                           ]
[      * *                                                  ]
[    * *                                                    ]
[      * *                                     *            ]
[        * * *                               * * *          ]
[            *                     * *     *   *   *        ]
[            *                     * *   * * *   * * *      ]
[                                          *   *   *        ]
[                                            * * *          ]

iteration  12 of 20:
[                                            * * *          ]
[                                                           ]
[    * * *                                                  ]
[    *                                                      ]
[    *                                       * * *          ]
[      * *   *                                              ]
[            * *                   * * * *           *      ]
[                                  * * * *           *      ]
[                                        *           *      ]
[                                                           ]

iteration  13 of 20:
[                                              *            ]
[      *                                       *            ]
[    * *                                                    ]
[  * *                                         *            ]
[    *                                         *            ]
[      *   * * *                     * *       *            ]
[          * * *                   *     *                  ]
[                                  *       *       * * *    ]
[                                    *   *                  ]
[                                              *            ]

iteration  14 of 20:
[                                            * * *          ]
[    * *                                                    ]
[  *   *                                                    ]
[  *                                                        ]
[  * * *     *                               * * *          ]
[        * *   *                     * *                    ]
[        * *   *                   *   * *           *      ]
[            *                     * * * * *         *      ]
[                                                    *      ]
[                                                           ]

iteration  15 of 20:
[                                              *            ]
[    * *                                       *            ]
[  *   *                                                    ]
[* *   *                                       *            ]
[  * * * * * *                                 *            ]
[    *         *                     * * *     *            ]
[        *     *                   *       *                ]
[          * *                     *       *       * * *    ]
[                                    * * *                  ]
[                                              *            ]

iteration  16 of 20:
[                                            * * *          ]
[    * *                                                    ]
[* *   * *                                                  ]
[*         *                                                ]
[*       * * *                         *     * * *          ]
[  * *         *                     * * *   *              ]
[          *   *                   *   *   * *       *      ]
[          * *                     *   *   *         *      ]
[                                    * * *           *      ]
[                                      *                    ]

iteration  17 of 20:
[                                              *            ]
[  * * * *                                     *            ]
[* *   * *                                                  ]
[*     *     *                                 *           *]
[*       * * *                       * * * * * *            ]
[  *     *     *                                            ]
[          *   *                   *         *              ]
[          * *                     *       * *     * * *    ]
[                                                           ]
[                                    * * *     *            ]

iteration  18 of 20:
[    * *                               *     * * *          ]
[* *     *                                                  ]
[          *                                               *]
[    * *     *                         * * *   *           *]
[* *   * *   * *                       * * * * *           *]
[        *     *                     * * *     *            ]
[        * *   *                           * *       *      ]
[          * *                             * *       *      ]
[                                    * * * * *       *      ]
[                                      *                    ]

iteration  19 of 20:
[  * * *                                       *            ]
[* * * * *                                     *            ]
[  * * * * *                             *                 *]
[  * * *     * *                       *       *         * *]
[* *     *   * *                               * *         *]
[*             * *                   *         *            ]
[        *     *                       *       *            ]
[        * * *                         *       *   * * *    ]
[                                    * *     *              ]
[                                                           ]

iteration  20 of 20:
[*       *                                                  ]
[          *                                                ]
[          * *                                           * *]
[              *                               * *       *  ]
[      *   *                                 * * *       *  ]
[* *       *     *                           * *           *]
[        *     * *                   * *     * *     *      ]
[        * * *                         * *   * * *   *      ]
[          *                         * *             *      ]
[    *                                                      ]
```
