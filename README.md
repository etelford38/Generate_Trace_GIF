# Generate_Trace_GIF
A GUI for creating GIFs that trace along user input data. Written by Evan Telford (ejt2133@columbia.edu).

## To run the included python file, the following packages are required (links to anaconda):
* glob (https://anaconda.org/conda-forge/glob2)
* matplotlib (https://anaconda.org/conda-forge/matplotlib)
* numpy (https://anaconda.org/anaconda/numpy)
* os (https://anaconda.org/jmcmurray/os)
* pandas (https://anaconda.org/anaconda/pandas)
* pathlib (https://anaconda.org/conda-forge/pathlib)
* PIL (https://anaconda.org/anaconda/pillow)
* PyQt5 (https://anaconda.org/anaconda/pyqt)
* re (automatically included)
* sys (automatically included)
* tqdm (https://anaconda.org/conda-forge/tqdm)

## List of GUI functions:
1.	Load Data:
This element of the main GUI allows users to search for and import data using the native file explorer. Simply click "Load Data" to open the file explorer and navigate to the desired file (see section below for data-file constraints).
2.	Available Data:
This section shows the available data columns that were imported from the data file selected by the user in "Load Data". There are two columns denoting the independent (x-axis) and dependent (y-axis) variables that will be plotted.
3.	Plot Data:
This GUI element allows the user to set the plot properties, set the data style, plot the data, and change the plot pixel size. Note that all user input fields (QLineEdits) are cleared when switching independent or dependent variables (under "Available Data"). If no input parameters are given, default parameters are chosen and displayed in the input fields after the user clicks "Plot Data".
4.	Trace Data:
This component is used to set the plot properties and data style for each trace frame, generate the trace frames, set the relevant parameters for the animation GIF, and generate the animation GIF. Note that all user input fields (QLineEdits) are cleared when switching independent or dependent variables (under "Available Data"). If no input parameters are given, default parameters are chosen and displayed in the input fields. "Color/Background before (after)" refers to the color of the data/plot background before (after) the trace marker. The "color marker" and "Marker line color" refer to the color of the trace marker and a vertical line following the trace marker, respectively.

## Data-file constraints:
	
A brief description of the subfunction which loads the data is as follows:
1.	Opens the selected file.
2.	Searches the file for a “[Data]” keyword.
3.	Reads the file start from the line after the one containing “[Data]”. Reading is done assuming comma-delimited text.
4.	The first line after the one containing “[Data]” is set to be the header.
5.	The remaining lines are saved as a data frame.

The python program can therefore load any data file that is formatted in the following way:
- Line X: [Data]
- Line X+1: Comma-delimited names of data columns.
- Line X+2 → end of file: Comma-delimited data in string format.

Note: Any lines before Line X do not matter. Can contain any information in any format. The python code will automatically skip them.
	
Second Note: files generated by MultiVu (Quantum Design's native software) are saved in the appropriate format. If your file is in a different format, you’ll need to convert it using a third-party program.
