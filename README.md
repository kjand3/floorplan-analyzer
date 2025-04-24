

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
- Streamlit GUI


## Command Line
The command line version of this tool gives the user more flexibility and control on the model. This form of the tool also exposes a training mode so the user can use their data to continue making improvments on the model. Running the train mode requires the following command:


```
python main.py --mode "train" --data_path data/train/floorplans/
```

In order to run the inference mode the following command:

```
python main.py --mode "inference" --data_path data/inference/3D/
```


There is also an additional ```--data_path``` flag that can be passed to ```main.py``` for either mode. If you
would like more control over all of the parameters in the model during ```inference``` and ```train``` modes,
run the following command:

```
python main.py --config "user_config.yaml"
```

Where the ```user_config.yaml``` adjusts each of the parameters in the tool. Note that when using this flag,
all other flags will be ignored if they are used together with the ```--config``` flag.


## Streamlit GUI

To run the streamlit GUI, use the following command:

```
streamlit run gui.py
```


This command will spin up your GUI. From there, you can select files from your local directory to inference your model with.
If you would like the GUI to only display your new image inference, make sure to select ```Cleanup & Reset``` at the end 
of each run.


# Datasets

This library currently supports the following raw formats during inferencing:

- .pdf
- .png
- .jpg

Samples of the type of data that can be used for ```inference``` mode can be found in ```data/inference/```. Note that
we have included 2D and 3D floor plans. Given the lack of detail in the object drawings, the model currently performs best
on 3D floorplan images. Future work will involve dataset generation for 2D floorplans.


Training data is expected to be in the following format:

```
data/
├── floorplans/
│   ├── file1.png
│   └── file2.pdf
└── train.csv
```

With this structure, all of the visual data will be contained in the ```floorplans/``` directory and the accompanying
```.csv``` file will contain the following information:

```
| Filename  |  x1 (px) |  y1 (px) |  x2 (px) |  y2 (px) |  Label   |
|-----------|----------|----------|----------|----------|----------|
| file1.png |   134    |   240    |   154    |    260   |   Table  |
| file1.png |   250    |   200    |   270    |    220   |   Chair  |
| file2.pdf |   400    |   200    |   420    |    220   |   Plant  |

```


# Future Work and Remarks

There is still a lot of work needed around labeled dataset generation and compilation to build a stronger
performing model. We can also add additional features to the model like:

- Increased model support like: YOLO, VisionTransformer(ViT), ...
- Validation data support during training
- Distributed cluster training
- Test Mode or benchmarking model metrics
- Containerization for Kubernetes orchestration

Note, the scripts directory includes some experimental work for synthetically generating data from images
which can be derived from the pdfs. There is an example of image of labeling using ChatGPT. This
will be crucial in improving model performance.
