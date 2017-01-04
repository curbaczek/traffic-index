# traffic-index
Deutsch:
Studentische Seminararbeit im Rahmen des Seminar Verkehrswesen am Institut für Verkehrswesen, Karlsruher Institut für Technologie. Ziel dieser Arbeit ist es, aus den Verkehrsinformationen von öffentlich zugänglichen Kartendiensten, einen "Stauindex" zu bilden,
um eine zeitliche und räumliche Vergleichbarkeit des Verkhrssituation in verschiedenen Städten herzustellen. Außerdem werden die wesentlichen Bodebedeckungsdaten aus der Karte extrahiert, um Zusammenhänge zwischen der Stadtstruktur und dem berechneten Index zu ermitteln.
Diese Arbeit stellt eine erste "Machbarkeitsstudie" dar und untersucht mögliche Vorgehensweisen und Beschränkungen bei der Umsetzung.      

English:
Student seminar reserach project at the Institute for traffic engineering at Karlsruhe Institute of Technology to analyse traffic information from  publicly available map services and turn them into an index for spatial and chronological comparison.
In addition land cover data will be extracted from the maps to show correlations between city structure and traffic situation.
This project is mainly a feasibility study, to look for limitations and possible solutions.

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
