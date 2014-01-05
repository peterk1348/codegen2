# codegen2

Simple code generator framework based on *Python* and *Jinja2*.

## Requirements

Make sure the following packages are installed in your environment.

* argparse
* jinja2

Clone this repository using *git clone*, then make sure the codegen.py file is executable.

    chown +x codegen2.py

## Command Line Use

    ./codegen2.py --workdir=/some/directory --model=some_model.cgmdl

Note that the model file is relative to the *workdir* location. The model file extension is not constrained, however it is good practice to use a distinct extension, for example: **.cgmdl**

### Model file

The model file is essentialy a *Python* source file, which is loaded dynamically during runtime. There are two constraints with this file:

1. It MUST include a dictionary named *generators*
2. It MUST include a dictionary names *variables*

Otherwise the model file could include any other Python code related to code generation. Typically the additional code would programmatically create or alter the *generators* or *variables* variables.

## IDE Use

The main design consideration with the framework was to be able to work with IDE-s by running the generation automatically (similar to compiling CoffeeScript, SASS, and similar files).

### JetBrain

In the JetBrain environments (IntelliJ IDEA, PyCharm, etc) there is a *File Watchers* plug-in that can watch specific files in a project and run any external tool when such file is created, or changed.

1. Setup a new file type
    1. Open **Preferences > IDE Settings > File Types**
    2. Add new File type: **codegen2 Model file**
    3. Register new patterns: ** *.cgmdl **
2. Create a new *File Watcher*
    1. Open **Preferences > Project Settings > File Watchers**
    2. Add a new File Watcher, Name: **codegen2**, check **Immediate file synchroniation**, select File type: **codegen2 Model file**, set Scope to **Project Files**, browse for the **codegen2.py** for Program, Arguments: **--model=$FileName$ --workdir=$FileDir$**

Once a new *.cgmdl* file is created, or modified the code generator runs and generates the files.

### Eclipse

TODO

## Example 1

This is a very-very simple example to show the basic use of the framework and artefacts.

**example1.cgmdl**

    generators = {
	    'test.py.template': 'test.py'
    }
    variables = {
	    'greeting': 'Hello'
    }

**test.py.template**

    #!/usr/bin/python
    print("{{greeting}} World!")

Running the generator produces the **test.py** file

    #!/usr/bin/python
    print("Hello World!")

## Example 2

In this example one of the variables' value is dynamically set.

**example2.cgmdl**

    generators = {
	    'request.py.template': 'request.py',
	    'response.py.template': 'response.py'
    }
    
    def who():
        return 'World'
    
    variables = {
	    'greeting': 'Hello',
	    'subject': who()
    }

**request.py.template**

    #!/usr/bin/python
    print('{{greeting}} {{subject}}!')

**response.py.template**

    #!/usr/bin/python
    print('{{greeting}} back!')


Running the generator produces the **request.py** file

    #!/usr/bin/python
    print("Hello World!")

and **response.py** file.

    #!/usr/bin/python
    print("Hello back!")

Values for the **generators** variable could be set dynamically similarly to the variables element in the example.
