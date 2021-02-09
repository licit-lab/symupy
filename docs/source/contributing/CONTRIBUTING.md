# Contributing to Symupy

If you're reading this section, you're probably interested in contributing to Symupy. Welcome and thanks for your interest in contributing!

## Roadmap plan

A general road plan should be available as a main issue entitled `Roadmap Plan` in the [issues page](https://github.com/licit-lab/symupy/issues). This plan is intended to collect the general plan of activities within the development process. In addition this issue intends to capture the general features that will be present in future releases of the software. In general, the intention of the plan is to keep a list of pending topics to work on. These pending topics could be: new features, bugs, documentation issues. Each one of the topics listed in the general plan should be associated to the corresponding issue 

### Reporting problems or bugs 

When reporting bugs please provide a complete description on the situation and provide information regarding the version of the system you are using, the operative system, and the steps to reproduce the bug. Please attach supporting files to enhance the bug documentation and provide more robust solutions and alternatives.

### Adding new features 

We are always happy to listen about new ideas and features to be introduced. Please open a new issue in the corresponding category to propose new features. 

## How to contribute 

### Methodology 

The development methodology is based on the [git flow](https://danielkummer.github.io/git-flow-cheatsheet/).  For the sake of clarity

- In general all the stable version is preserved in the `main` branch. 
- Development features are preserved in the `dev` branch 

A procedure in general to introduce changes is as follows: 

1. Create the `new feature` or the `hotfix` via the classic commands 
2. Perform the corresponding changes in the local machine 
3. Push the corresponding changes online 
4. Create Pull request integrating changes from the created branch into the `dev` branch. Assign this Pull request to a reviewer just to check that your feature/hotfix is correctly working. 
5. Merge Pull request into the `dev` branch 
6. Create new releases according to the established calendar. 
  

### General guidelines for contributing 

All code is written either in [Python](https://www.python.org) or [C++](https://isocpp.org). 

To contribute to the source code please consider the following guidelines:

- Important when adding new functionalities please document with examples as fast as they are created. 
- When creating a function use [Typing](https://docs.python.org/3/library/typing.html). for providing guidelines about the type of arguments.
- Put the majority of the documentation in the ``docstrings`` of the code. 
- This documentation follows the guidelines of [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). Docstrings may extend over multiple lines. Sections are created with a section header and a colon followed by a block of indented text.

  ```
  def create_object(type:str)-> object:
      """ This functions will create an object of a certain type 

          Args:
            type (str): Type of object to be created 

          Returns: 
            object: Created object 

          Example: 
            An example to use is the following::

              >>> my_object = create_object("type")
      """
      ... code to create object
      return object
  ```

- It is recommended as a good practice to use `CamelCase` notation for meta class or class definitions, and `snake_case` notation for variables and functions. A good way to validate this is via a linter. It is recommended to use [pylint](https://pylint.org) as a linter. 
- Automatic code formatters can be used for this case [black](https://black.readthedocs.io/en/stable/?badge=stable). 
- For C++ code it is recommended to use [Doxygen](https://www.doxygen.nl/manual/docblocks.html) for generating auto documentation, more information is available in this blog [post](https://devblogs.microsoft.com/cppblog/clear-functional-c-documentation-with-sphinx-breathe-doxygen-cmake/)
