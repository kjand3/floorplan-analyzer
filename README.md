

# Setup

To run this tool begin by running the following command:

''' 
make setup

'''

This should install all of your dependencies and activate your environment.


# Running the Tool

There are two ways to run the tool, via the command line and from the streamlit GUI.


## Command Line
The command line version of this tool gives the user more flexibility and control on the model. This form of the tool also exposes a training mode so the user can use their data to continue making improvments on the model. Running the train mode requires the following command:


'''
python main.py 

'''

and making the adjustment in the floorplan_analyzer/config/settings.py to the TRAIN mode.


In order to run the inference mode the same command can be run with the change in the config file to the appropriate mode. 



## Streamlit GUI

To run the streamlit GUI, use the following command:

'''
streamlit run gui.py 

'''

This command will spin up your GUI. From there, you can select files from your local directory to inference your model with. 
