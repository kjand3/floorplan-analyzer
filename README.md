

# Setup

To run this tool begin by running the following command:

```
make setup
```

This should install all of your dependencies. To activate your environment, run the
following command:

```
source venv/bin/activate
```


# Running the Library

There are two ways to run the library:
- Command Line
- Streamlit GUI.


## Command Line
The command line version of this tool gives the user more flexibility and control on the model. This form of the tool also exposes a training mode so the user can use their data to continue making improvments on the model. Running the train mode requires the following command:


```
python main.py --mode "train"
```

In order to run the inference mode the following command:

```
python main.py --mode "inference"
```


There is also an additional ```--data_path``` flag that can be passed to ```main.py``` for either mode.



## Streamlit GUI

To run the streamlit GUI, use the following command:

'''
streamlit run gui.py

'''

This command will spin up your GUI. From there, you can select files from your local directory to inference your model with.
