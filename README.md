<h1 align="center">Lab Scraper</h1>

<p align="left">
This project is a collection of web scrapers for extracting location metadata using various location finder tools on medical clinic websites. It comes with a simple GUI interface. The user can input their <b>zipcode</b>, <b>radial distance to search</b>, and the <b>max number of results</b> they'd like returned for each website.
</p>

## Table of Contents
- [Sites We're Scraping](#sites)
- [Installation](#install)
- [Usage](#usage)
- [Known Issues](#issues)

<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/rbondoc96/lab-scraper/master/imgs/GUI%20v2020-09-13.PNG">
</p>
<br>

## Sites We're Scraping <a name="sites"></a>
<ul>
    <li><a href="https://www.labcorp.com/labs-and-appointments/results">LabCorp PSC Sites</a></li>
    <li><a href="https://appointment.questdiagnostics.com/patient/findlocation">Quest Diagnostics PSC Sites</a></li>
    <li><a href="https://www.concentra.com/urgent-care-centers/#g=&gtext=&glevel=&gstate=">Concentra Urgent Care</a></li>
    <li><a href="https://www.google.com/maps/">Google Maps Nearby Search</a></li>
</ul>

## Installation <a name = "install"></a>

<h4>Python Versions</h4>
<ul>
  <li>Python 3.8.2</li>
  <li>pipenv v2018.11.26</li>
</ul>

<h4>Front End GUI</h4>
<ul>
  <li>PyQt5</li>
  <li>QT Designer (comes with PyQt5-tools)</li>
</ul>

<h4>Back End</h4>
<ul>
  <li>Selenium 3.141.0</li>
  <li>tqdm 4.49.0</li>
  <li>uszipcode 0.2.4</li>
</ul>

<h3>Configuring your Project</h3>

In the repo root directory, create a new virtual environment with <b>pipenv</b> and install the Python project dependencies:

```
pipenv shell    # Initialize the virtual environment
pipenv install  # Install Python dependencies
```

<h3>Recompiling the GUI</h3>

If any changes were made to the GUI, you will need to do the following:
1. Place ALL code following the setupUi() and retranslateUi() functions in gui.py into a temporary file or your clipboard.

2. Place ALL imports in gui.py into a temporary file or your clipboard

3. [1] and [2] ARE IMPORTANT. OTHERWISE, ALL GUI FUNCTIONALITY WILL BE OVERWRITTEN. Unless you know what you're doing, make sure to complete [1] and [2].

4. Run the following command in the /src/ui/ directory:

    ```
    pyuic5 -x gui.ui -o gui.py
    # Usage: 
    # pyuic5 -x [your .ui file from QT Designer] -o [output .py file]
    ```

5. After compilation, replace all code from [1] and imports from [2] back into the recompiled gui.py file.

## Usage <a name = "usage"></a>

<h3>Running the Program</h3>

From the <b>/src/</b> directory, run the following command to start the program and the GUI:

```
python main.py
```

## Known Issues <a name = "issues"></a>
<ul>
    <li>
        <div>Google Maps Search</div>
        <ul>
            <li>Each entry takes ~3.5s to acquire, since Selenium has to click each item on the page and wait for elements to render before clicking.</li>
        </ul>
    </li>
</ul>