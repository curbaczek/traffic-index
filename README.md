# traffic-index
Script to analyse cities' traffic situation over a period of time and calculate an index to allow comparability

# Setup

## Initial Cloning

When cloning the repository for the first time, do not forget to initialize all submodules:

    $ git submodule update --init

## Libraries and Tools

To avoid version conflicts, all tools and libraries used are installed via `pip`.
If your user is not allowed to install system-wide, consider using `virtualenv`.
For this, see the section "Using a Virtual Environment" now.

The following libraries have to be installed using `pip`:

* -

## Using a Virtual Environment

First of all, make sure you have `virtualenv` installed on your system.
Then, create a virtual environment in a location of your choice, say "~/myenv":

    $ virtualenv ~/myenv

After that, you can switch with your current shell into the newly created environment:

    $ source ~/myenv/bin/activate

At this point "(myenv)" should be shown at the beginning of the prompt.
The virtual environment is now active and installations using `pip` should work now.
Remember, for each new shell, the virtual environment has to be activated again.

# Quality Guidelines

Run all automatic tests with detailed error messages with `make check`.
To make sure very commit satisfys the requirements consider using a `pre-commit` hook:

    $ ln -s ../../.quality-checks/pre-commit.sh .git/hooks/pre-commit

## Python Code

All python code has to conform to PEP8.
For further reading see [https://www.python.org/dev/peps/pep-0008/].

The automatic tests applied by `make check` can detect most non-conforming constructs.
Nevertheless, some conventions are not covered by `pep8`.
Naming and import conventions are among those aspects and have to be checked manually.
